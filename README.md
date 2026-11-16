# Spacetime Visualizations

Interactive 3D pages, built with three.js, that show how space and time behave. Every number they display
is computed from real physics and checked against independent values.

Open `index.html` by double-clicking it. You need an internet connection for three.js and KaTeX, which load
from a CDN.

## Pages

| Page | What it shows | State |
|---|---|---|
| `galaxy-map.html` | ~18,000 real galaxies from the CfA2 Redshift Survey in 3D, placed by redshift. You can switch between ΛCDM and Hubble-law distances, change H₀, and view the famous 1986 "slice of the universe". | Prototype |
| Gravitational redshift (Schwarzschild) | Light climbing out of a gravity well, with warped-grid and embedding views | Planned |
| Observable universe sphere | Our past light cone, from today back to recombination (the CMB) | Planned |

## How accuracy is kept

- All physics in a page sits in one marked block, separate from the drawing code.
- Each physics function has self-tests against values computed separately with Astropy
  (`physics/reference-values.md`), or against experiments.
- Run the tests in a browser by adding `?selftest` to the page address, or from the command line:

  ```bash
  node .claude/skills/spacetime-physics/scripts/check_physics.mjs galaxy-map.html
  ```

- Regenerate the reference values (needs [uv](https://docs.astral.sh/uv/)):

  ```bash
  uv run .claude/skills/spacetime-physics/scripts/reference_values.py
  ```

- Each page has a *Physics notes* panel listing its equations, assumptions, sources, and anything drawn
  exaggerated or simplified.

## Credits

The galaxy data is from the CfA Redshift Survey (J. Huchra et al.), **Smithsonian Astrophysical Observatory**.
Cosmological parameters come from the Planck Collaboration. Calculations and checks use Astropy, NumPy and SciPy;
the pages use three.js and KaTeX. See [CREDITS.md](CREDITS.md) for the full list with citations.

## License

The code is open source under the [MIT License](LICENSE), © 2026 Dan Sternof Beyer.
Data and third-party software keep their own licenses (see [CREDITS.md](CREDITS.md) and [data/README.md](data/README.md)).
