# /// script
# requires-python = ">=3.11"
# dependencies = ["astropy==7.2.0", "numpy>=1.26", "scipy>=1.13"]
# ///
"""
Builds data/cfa2-galaxies.js from the raw CfA2 Redshift Survey catalog (data/raw/cfa2.dat).

The raw file is fixed-width text in the ZCAT format (Huchra et al.). Coordinates are
B1950 (FK4). This script:
  1. reads name, B1950 RA/Dec, magnitude and cz (heliocentric velocity, km/s),
  2. keeps entries with a measured velocity,
  3. converts positions to ICRS (J2000) with Astropy,
  4. flags the galaxies in the original 1986 "slice of the universe"
     (de Lapparent, Geller & Huchra 1986: 8h <= RA < 17h, 26.5 <= Dec < 32.5, B1950),
  5. writes a compact JavaScript file the page loads with a plain <script> tag
     (so it works when index pages are opened by double-clicking, without a server).

Run from the project root:
    uv run data/build_cfa2.py
"""

import json
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import FK4, SkyCoord

# ===== Paths =====

DATA_FOLDER = Path(__file__).resolve().parent
RAW_CATALOG = DATA_FOLDER / "raw" / "cfa2.dat"
OUTPUT_FILE = DATA_FOLDER / "cfa2-galaxies.js"

# ===== Column layout (1-based, inclusive), worked out from the file itself =====
# Checked against known galaxies, e.g. NGC 4486 = M87 and NGC 4874 in the Coma cluster.
NAME_COLUMNS = (1, 10)
RA_COLUMNS = (12, 19)          # hhmmss.s, B1950
DEC_SIGN_COLUMN = 20           # '-' or blank/'+'
DEC_COLUMNS = (21, 26)         # ddmmss, B1950
MAGNITUDE_COLUMNS = (27, 31)   # B(0)-Zwicky system, as given
VELOCITY_COLUMNS = (32, 36)    # cz in km/s, heliocentric

# Original 1986 slice limits, in B1950 coordinates.
SLICE_RA_HOURS = (8.0, 17.0)
SLICE_DEC_DEGREES = (26.5, 32.5)


def field(line, columns):
    start, end = columns
    return line[start - 1:end].strip()


def parse_ra_hours(text):
    hours, minutes, seconds = float(text[0:2]), float(text[2:4]), float(text[4:])
    return hours + minutes / 60 + seconds / 3600


def parse_dec_degrees(sign_text, text):
    degrees, minutes, seconds = float(text[0:2]), float(text[2:4]), float(text[4:6])
    value = degrees + minutes / 60 + seconds / 3600
    return -value if sign_text == "-" else value


def read_catalog():
    """Returns a list of dicts for every row that has a position and a velocity."""
    rows, skipped = [], 0
    for line in RAW_CATALOG.read_text(encoding="latin-1").splitlines():
        if len(line) < VELOCITY_COLUMNS[1]:
            skipped += 1
            continue
        try:
            velocity_text = field(line, VELOCITY_COLUMNS)
            ra_text, dec_text = field(line, RA_COLUMNS), line[DEC_COLUMNS[0] - 1:DEC_COLUMNS[1]]
            if not velocity_text or not ra_text or not dec_text.strip():
                skipped += 1
                continue
            magnitude_text = field(line, MAGNITUDE_COLUMNS)
            rows.append({
                "name": field(line, NAME_COLUMNS),
                "ra_hours_b1950": parse_ra_hours(ra_text),
                "dec_degrees_b1950": parse_dec_degrees(line[DEC_SIGN_COLUMN - 1], dec_text.replace(" ", "0")),
                "magnitude": float(magnitude_text) if magnitude_text else None,
                "cz": int(velocity_text),
            })
        except ValueError:
            skipped += 1
    return rows, skipped


def convert_to_icrs(rows):
    """B1950 FK4 -> ICRS. Galaxies have no measurable proper motion, so only the frame changes."""
    coordinates = SkyCoord(
        ra=[row["ra_hours_b1950"] for row in rows] * u.hourangle,
        dec=[row["dec_degrees_b1950"] for row in rows] * u.deg,
        frame=FK4(equinox="B1950", obstime="B1950"),
    ).icrs
    return coordinates.ra.deg, coordinates.dec.deg


def in_1986_slice(row):
    return (SLICE_RA_HOURS[0] <= row["ra_hours_b1950"] < SLICE_RA_HOURS[1]
            and SLICE_DEC_DEGREES[0] <= row["dec_degrees_b1950"] < SLICE_DEC_DEGREES[1])


def write_javascript(rows, ra_icrs, dec_icrs):
    # Flat arrays keep the file small; the page rebuilds objects as needed.
    data = {
        "names": [row["name"] for row in rows],
        "raDegrees": [round(float(value), 4) for value in ra_icrs],
        "decDegrees": [round(float(value), 4) for value in dec_icrs],
        "czKmPerS": [row["cz"] for row in rows],
        "magnitude": [row["magnitude"] for row in rows],
        "in1986Slice": [1 if in_1986_slice(row) else 0 for row in rows],
    }
    header = (
        "// CfA2 Redshift Survey galaxies, built by data/build_cfa2.py from data/raw/cfa2.dat.\n"
        "// Source: CfA Redshift Catalog (ZCAT), J. Huchra et al., Smithsonian Astrophysical Observatory,\n"
        "// https://lweb.cfa.harvard.edu/~dfabricant/huchra/zcat/ . Positions converted B1950 FK4 -> ICRS.\n"
        "// cz is heliocentric velocity in km/s, defined by the catalog as c*z with c = 299792.5 km/s.\n"
        "// Do not edit by hand.\n"
    )
    OUTPUT_FILE.write_text(header + "const CFA2_GALAXIES = " + json.dumps(data, separators=(",", ":")) + ";\n")


def main():
    rows, skipped = read_catalog()
    ra_icrs, dec_icrs = convert_to_icrs(rows)
    write_javascript(rows, ra_icrs, dec_icrs)
    velocities = np.array([row["cz"] for row in rows])
    print(f"kept {len(rows)} rows, skipped {skipped}")
    print(f"cz range {velocities.min()} .. {velocities.max()} km/s; median {np.median(velocities):.0f}")
    print(f"in 1986 slice: {sum(in_1986_slice(row) for row in rows)}")
    for check_name in ("N4486", "N4874", "N0224"):
        for row, ra, dec in zip(rows, ra_icrs, dec_icrs):
            if row["name"] == check_name:
                print(f"{check_name}: ICRS RA {ra:.4f} deg, Dec {dec:.4f} deg, cz {row['cz']}, mag {row['magnitude']}")
    print(f"wrote {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
