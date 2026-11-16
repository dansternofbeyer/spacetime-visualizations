# /// script
# requires-python = ">=3.11"
# dependencies = ["astropy==7.2.0", "numpy>=1.26", "scipy>=1.13"]
# ///
"""
Builds data/2mrs-galaxies.js and data/2mrs-redshift-sources.md from the 2MASS Redshift Survey.

Source: the journal-published 2MRS catalog, Huchra et al. 2012, ApJS 199, 26, as distributed by
CDS VizieR (J/ApJS/199/26, doi:10.26093/cds/vizier.21990026). Downloaded from the VizieR mirror at
vizier.idia.ac.za because the main CDS server was unreachable on 2026-11-15:
    data/raw/2mrs_table3.tsv   main catalog (table3), columns ID RAJ2000 DEJ2000 Kcmag cz e_cz n_cz r_cz CAT
    data/raw/2mrs_table4.tsv   references (table4): bibcode → authors (year)

Steps:
  1. keep catalog rows that have a redshift (43,532 of 44,599),
  2. drop galaxies already in the CfA2 or 6dFGS files (within 20" and 300 km/s), keeping the earlier entry,
  3. write a compact JavaScript file for the map,
  4. write a list of every paper whose redshifts appear in the kept galaxies, as the 2MRS team asks
     ("all other entries must be cited using their respective bibliographic codes").

Run from the project root, after data/build_cfa2.py and data/build_6dfgs.py:
    uv run data/build_2mrs.py
"""

import json
from collections import Counter
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord

# ===== Paths =====

DATA_FOLDER = Path(__file__).resolve().parent
MAIN_TABLE = DATA_FOLDER / "raw" / "2mrs_table3.tsv"
REFERENCE_TABLE = DATA_FOLDER / "raw" / "2mrs_table4.tsv"
EARLIER_SURVEY_FILES = [DATA_FOLDER / "cfa2-galaxies.js", DATA_FOLDER / "6dfgs-galaxies.js"]
OUTPUT_FILE = DATA_FOLDER / "2mrs-galaxies.js"
SOURCES_FILE = DATA_FOLDER / "2mrs-redshift-sources.md"

CROSS_MATCH_RADIUS = 20 * u.arcsec
CROSS_MATCH_VELOCITY_KM_S = 300

# Meaning of the n_cz source codes, from the 2MRS README (http://tdc-www.harvard.edu/2mrs/2mrs_readme.html).
SOURCE_CODE_NAMES = {
    "6": "6dF Galaxy Survey DR3",
    "C": "2MRS observations, CTIO 1.5 m",
    "D": "2MRS observations, McDonald Observatory",
    "F": "2MRS observations, FLWO 1.5 m",
    "M": "NED, non-default value",
    "N": "NED default value (previously published)",
    "O": "ZCAT (CfA Redshift Catalog)",
    "S": "Sloan Digital Sky Survey DR8",
}


def read_pipe_table(path):
    """VizieR ASU '|' output: comment lines start with '#', then a header, units and dashes."""
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line and not line.startswith("#")]
    header = [name.strip() for name in lines[0].split("|")]
    return [dict(zip(header, (value.strip() for value in line.split("|")))) for line in lines[3:]]


def read_catalog():
    rows = []
    for record in read_pipe_table(MAIN_TABLE):
        if not record["cz"]:
            continue
        rows.append({
            "name": record["ID"],
            "ra": float(record["RAJ2000"]),
            "dec": float(record["DEJ2000"]),
            "cz": int(record["cz"]),
            "magnitude": float(record["Kcmag"]) if record["Kcmag"] else None,
            "source_code": record["n_cz"],
            "bibcode": record["r_cz"],
        })
    return rows


def read_earlier_surveys():
    ra, dec, cz = [], [], []
    for path in EARLIER_SURVEY_FILES:
        text = path.read_text()
        data = json.loads(text[text.index("{"):text.rindex("}") + 1])
        ra += data["raDegrees"]
        dec += data["decDegrees"]
        cz += data["czKmPerS"]
    return np.array(ra), np.array(dec), np.array(cz)


def find_duplicates(rows):
    earlier_ra, earlier_dec, earlier_cz = read_earlier_surveys()
    survey = SkyCoord(ra=[row["ra"] for row in rows] * u.deg, dec=[row["dec"] for row in rows] * u.deg)
    earlier = SkyCoord(ra=earlier_ra * u.deg, dec=earlier_dec * u.deg)
    nearest_index, separation, _ = survey.match_to_catalog_sky(earlier)
    velocity_difference = np.abs(np.array([row["cz"] for row in rows]) - earlier_cz[nearest_index])
    return (separation < CROSS_MATCH_RADIUS) & (velocity_difference < CROSS_MATCH_VELOCITY_KM_S)


def write_javascript(rows):
    data = {
        "names": [row["name"] for row in rows],
        "raDegrees": [round(row["ra"], 5) for row in rows],
        "decDegrees": [round(row["dec"], 5) for row in rows],
        "czKmPerS": [row["cz"] for row in rows],
        "magnitude": [row["magnitude"] for row in rows],
    }
    header = (
        "// 2MASS Redshift Survey galaxies, built by data/build_2mrs.py.\n"
        "// Data: Huchra et al. 2012, ApJS 199, 26 (2MRS), via CDS VizieR J/ApJS/199/26\n"
        "// (doi:10.26093/cds/vizier.21990026). Redshift sources for each galaxy: data/2mrs-redshift-sources.md.\n"
        "// J2000 positions. cz: barycentric velocity, km/s. magnitude: extinction-corrected 2MASS Ks (isophotal).\n"
        "// Galaxies already in cfa2-galaxies.js or 6dfgs-galaxies.js have been removed. Do not edit by hand.\n"
    )
    OUTPUT_FILE.write_text(header + "const TWOMRS_GALAXIES = " + json.dumps(data, separators=(",", ":")) + ";\n")


def write_source_list(rows):
    authors_by_bibcode = {record["Bibcode"]: record["Aut"] for record in read_pipe_table(REFERENCE_TABLE)}
    counts = Counter(row["bibcode"] for row in rows)
    lines = [
        "# 2MRS redshift sources",
        "",
        "The 2MASS Redshift Survey (Huchra et al. 2012, ApJS 199, 26) asks that every redshift it compiled",
        "from earlier work be cited by its own bibliographic code. These are all the sources of the redshifts",
        f"shown in the map for the {len(rows):,} 2MRS galaxies that aren't also in CfA2 or 6dFGS.",
        "Codes are ADS bibcodes (https://ui.adsabs.harvard.edu/abs/<bibcode>). Generated by `data/build_2mrs.py`.",
        "",
        "| Bibcode | Authors (year) | Galaxies |",
        "|---|---|---|",
    ]
    for bibcode, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| [`{bibcode}`](https://ui.adsabs.harvard.edu/abs/{bibcode}) | {authors_by_bibcode.get(bibcode, '—')} | {count:,} |")
    SOURCES_FILE.write_text("\n".join(lines) + "\n")
    return counts, authors_by_bibcode


def main():
    rows = read_catalog()
    duplicate = find_duplicates(rows)
    kept_rows = [row for row, is_duplicate in zip(rows, duplicate) if not is_duplicate]
    write_javascript(kept_rows)
    counts, authors_by_bibcode = write_source_list(kept_rows)

    velocities = np.array([row["cz"] for row in kept_rows])
    print(f"read {len(rows)} galaxies with redshifts; dropped {duplicate.sum()} already in CfA2/6dFGS; kept {len(kept_rows)}")
    print(f"cz {velocities.min()} .. {velocities.max()} km/s, median {np.median(velocities):.0f}")
    print("kept by source:", dict(Counter(SOURCE_CODE_NAMES.get(row['source_code'], row['source_code']) for row in kept_rows)))
    missing = [bibcode for bibcode in counts if bibcode not in authors_by_bibcode]
    print(f"{len(counts)} distinct source papers; {len(missing)} not in table4: {missing[:5]}")
    print(f"wrote {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size / 1e6:.2f} MB) and {SOURCES_FILE}")


if __name__ == "__main__":
    main()
