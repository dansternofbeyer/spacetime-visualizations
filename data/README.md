# Data

## CfA2 Redshift Survey (`cfa2-galaxies.js`)

- **Source:** CfA Redshift Catalog (ZCAT), J. Huchra et al., Harvard-Smithsonian Center for Astrophysics.
  Page: https://lweb.cfa.harvard.edu/~dfabricant/huchra/zcat/
- **Raw files** (in `raw/`, downloaded 2026-11-15):
  - `cfa2.dat`: the CfA2 survey catalog, 2,164,478 bytes, 18,217 lines, fixed-width ZCAT format
  - `zcom.htm`: the catalog's format and usage description
  - `zcomtablesref.pdf`: the format tables (its embedded fonts don't extract as text)
  These raw files are kept out of git (their license isn't stated). To get them again:
  `curl -o data/raw/cfa2.dat https://lweb.cfa.harvard.edu/~dfabricant/huchra/zcat/cfa2.dat`
- **Built by:** `uv run data/build_cfa2.py`, which converts B1950 (FK4) positions to ICRS (J2000) with Astropy
  and flags the 1986 slice (8h ≤ RA < 17h, 26.5° ≤ Dec < 32.5°, B1950).
- **Checks:** the converted positions of NGC 4486 (M87) and NGC 4874 (Coma) match their published J2000
  positions to within about 1″. 1,095 galaxies fall in the 1986 slice, close to the ~1,100 in de Lapparent,
  Geller & Huchra (1986), ApJ 302, L1.
- **License / terms:** none stated. The site asks that the Smithsonian Astrophysical Observatory and the
  authors be credited, and that people citing the catalog follow its README. **The owner approved publishing this
  data (2026-11-15)** on condition that every page using it credits the Smithsonian Astrophysical Observatory
  and links back to the ZCAT page above. (The ZCAT documentation says velocities with negative source codes
  were private when it was written. The owner judged this not to apply, so no check was made.)
- **Known limits:** positions are in redshift space (peculiar velocities distort them), the survey is limited
  to about magnitude 15.5, and velocities are heliocentric. The page's Physics notes explain each one.
