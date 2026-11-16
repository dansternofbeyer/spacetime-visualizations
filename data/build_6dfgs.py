# /// script
# requires-python = ">=3.11"
# dependencies = ["astropy==7.2.0", "numpy>=1.26", "scipy>=1.13"]
# ///
"""
Builds data/6dfgs-galaxies.js from the 6dFGS Final Redshift Release catalog.

Source file: data/raw/heasarc_sixdfgs.tdat.gz, NASA HEASARC's copy of CDS catalog VII/259
(Jones et al. 2009). Positions are already J2000 (ICRS-compatible at this precision).

Steps:
  1. read name, RA, Dec, b_J magnitude, cz and redshift quality,
  2. keep quality 3 or 4 (6dFGS measurements) and 9 (redshifts taken from other catalogs);
     HEASARC's table contains only these,
  3. drop 6dFGS entries that duplicate a galaxy already in the CfA2 file (same place, same cz),
     keeping the CfA2 entry,
  4. drop internal repeats: a second target within 10" with the same cz (one galaxy split into
     two targets, both given the same borrowed redshift),
  5. write a compact JavaScript file loaded by a plain <script> tag.

Run from the project root, after data/build_cfa2.py:
    uv run data/build_6dfgs.py
"""

import gzip
import json
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord

# ===== Paths =====

DATA_FOLDER = Path(__file__).resolve().parent
RAW_CATALOG = DATA_FOLDER / "raw" / "heasarc_sixdfgs.tdat.gz"
CFA2_FILE = DATA_FOLDER / "cfa2-galaxies.js"
OUTPUT_FILE = DATA_FOLDER / "6dfgs-galaxies.js"

# ===== Matching rules =====

KEPT_QUALITY_FLAGS = {3, 4, 9}
CROSS_MATCH_RADIUS = 20 * u.arcsec          # CfA2 positions are B1950 plate positions, good to ~10"
CROSS_MATCH_VELOCITY_KM_S = 300            # larger than typical redshift errors (tens of km/s)
INTERNAL_REPEAT_RADIUS = 10 * u.arcsec

# Column positions in the HEASARC TDAT "line[1]" format.
COLUMN_NAMES = ("name ra dec lii bii num_total_measures num_highq_measure bj_mag program_id rf_mag "
                "supercosmos_class radial_velocity_compflag radial_velocity radial_velocity_error "
                "ref_radial_velocity radial_velocity_qualflag av original_weight target_id template_code "
                "name_redshift_field specid_values").split()
COLUMN = {name: index for index, name in enumerate(COLUMN_NAMES)}


def read_catalog():
    rows = []
    with gzip.open(RAW_CATALOG, "rt", encoding="latin-1") as file:
        in_data = False
        for line in file:
            if line.startswith("<DATA>"):
                in_data = True
                continue
            if not in_data or line.startswith("<END>"):
                continue
            fields = line.rstrip("\n").split("|")
            quality = int(fields[COLUMN["radial_velocity_qualflag"]])
            if quality not in KEPT_QUALITY_FLAGS:
                continue
            magnitude_text = fields[COLUMN["bj_mag"]].strip()
            rows.append({
                "name": fields[COLUMN["name"]].replace("6dFGS ", "").strip(),
                "ra": float(fields[COLUMN["ra"]]),
                "dec": float(fields[COLUMN["dec"]]),
                "cz": int(fields[COLUMN["radial_velocity"]]),
                "magnitude": float(magnitude_text) if magnitude_text else None,
                "quality": quality,
            })
    return rows


def read_cfa2():
    text = CFA2_FILE.read_text()
    data = json.loads(text[text.index("{"):text.rindex("}") + 1])
    return np.array(data["raDegrees"]), np.array(data["decDegrees"]), np.array(data["czKmPerS"])


def find_cfa2_duplicates(rows):
    """True for each 6dFGS row whose nearest CfA2 galaxy is within the radius and has a similar cz."""
    cfa2_ra, cfa2_dec, cfa2_cz = read_cfa2()
    survey = SkyCoord(ra=[row["ra"] for row in rows] * u.deg, dec=[row["dec"] for row in rows] * u.deg)
    cfa2 = SkyCoord(ra=cfa2_ra * u.deg, dec=cfa2_dec * u.deg)
    nearest_index, separation, _ = survey.match_to_catalog_sky(cfa2)
    velocity_difference = np.abs(np.array([row["cz"] for row in rows]) - cfa2_cz[nearest_index])
    return (separation < CROSS_MATCH_RADIUS) & (velocity_difference < CROSS_MATCH_VELOCITY_KM_S)


def find_internal_repeats(rows):
    """True for the second of any two rows within 10" of each other with identical cz."""
    coordinates = SkyCoord(ra=[row["ra"] for row in rows] * u.deg, dec=[row["dec"] for row in rows] * u.deg)
    first, second, _, _ = coordinates.search_around_sky(coordinates, INTERNAL_REPEAT_RADIUS)
    repeated = np.zeros(len(rows), dtype=bool)
    for index_a, index_b in zip(first, second):
        if index_a < index_b and rows[index_a]["cz"] == rows[index_b]["cz"]:
            repeated[index_b] = True
    return repeated


def write_javascript(rows):
    data = {
        "names": [row["name"] for row in rows],
        "raDegrees": [round(row["ra"], 4) for row in rows],
        "decDegrees": [round(row["dec"], 4) for row in rows],
        "czKmPerS": [row["cz"] for row in rows],
        "magnitude": [row["magnitude"] for row in rows],
    }
    header = (
        "// 6dFGS galaxies, built by data/build_6dfgs.py from data/raw/heasarc_sixdfgs.tdat.gz.\n"
        "// Data from the Final Release of 6dFGS (Jones et al. 2004, MNRAS 355, 747; Jones et al. 2009,\n"
        "// MNRAS 399, 683), via NASA HEASARC (table sixdfgs, from CDS VII/259). J2000 positions.\n"
        "// cz: best combined recession velocity, km/s. magnitude: recalibrated b_J.\n"
        "// Galaxies already in cfa2-galaxies.js have been removed. Do not edit by hand.\n"
    )
    OUTPUT_FILE.write_text(header + "const SIXDFGS_GALAXIES = " + json.dumps(data, separators=(",", ":")) + ";\n")


def main():
    rows = read_catalog()
    cfa2_duplicate = find_cfa2_duplicates(rows)
    internal_repeat = find_internal_repeats(rows)
    keep = ~(cfa2_duplicate | internal_repeat)
    kept_rows = [row for row, keep_row in zip(rows, keep) if keep_row]
    write_javascript(kept_rows)

    velocities = np.array([row["cz"] for row in kept_rows])
    print(f"read {len(rows)} rows (quality 3/4/9)")
    print(f"dropped {cfa2_duplicate.sum()} CfA2 duplicates and {(internal_repeat & ~cfa2_duplicate).sum()} internal repeats")
    print(f"kept {len(kept_rows)}; cz {velocities.min()} .. {velocities.max()} km/s, median {np.median(velocities):.0f}")
    print(f"quality counts kept: { {q: sum(1 for r in kept_rows if r['quality'] == q) for q in sorted(KEPT_QUALITY_FLAGS)} }")
    print(f"wrote {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
