# Spacetime Visualizations

Interactive 3D pages, built with three.js, that show how space and time behave. Every number they display
is computed from real physics and checked against independent values.

**Live site:** https://dansternofbeyer.github.io/spacetime-visualizations/

To run it locally, open `index.html` by double-clicking it. You need an internet connection for three.js and KaTeX, which load
from a CDN.

## Pages

| Page | What it shows | State |
|---|---|---|
| `galaxy-map.html` | ~158,000 real galaxies from the CfA2 (north), 6dFGS (south) and 2MRS (whole sky) redshift surveys in 3D, placed by redshift. You can switch between ΛCDM and Hubble-law distances, change H₀, colour by survey, and view the famous 1986 "slice of the universe". | Prototype |
| `gravitational-redshift.html` | Light climbing out of a gravity well (Schwarzschild metric, observer at infinity). A star or black hole whose mass you can change, an emitter A and receiver B you can move, a playback-speed control for light, and two ways to draw space: a warped cube grid and Flamm's paraboloid. Everything is at true scale except the drawn size of the light wave. | Prototype |
| `two-body-problem.html` | Two neutron-star-sized stars at a distance you choose, in the exact static Weyl / Israel–Khan solution (held apart by a strut, which the page shows). Light from A to B reddens climbing out of one star's well and blues falling into the other's; clocks along the path and observers you place (or the camera) show how time and redshift differ from spot to spot. Views: a Flamm-style grid like the one-star page's (built from the true-length surface, with five anchors; or two other grid styles), a clock-rate landscape, and a true-length surface (the two-star version of Flamm's paraboloid, computed numerically and checked against an independent solver). | Prototype |
| `milky-way-andromeda.html` | The Milky Way and Andromeda 761 kpc apart, with published mass models (halo, disc, bulge). Light from A to B, clocks, observers, gravitational vs Doppler shift, Shapiro delay, and the one-star page's warped grid built galaxy by galaxy (weak field, so the effects add). Effects are parts per million, drawn exaggerated by a stated factor. | Prototype |
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

The galaxy data is from the CfA Redshift Survey (J. Huchra et al.), **Smithsonian Astrophysical Observatory**,
the Final Release of 6dFGS (Jones et al. 2004, 2009) via NASA HEASARC, and the 2MASS Redshift Survey
(Huchra et al. 2012) via CDS VizieR.
Cosmological parameters come from the Planck Collaboration. Calculations and checks use Astropy, NumPy and SciPy;
the pages use three.js and KaTeX. See [CREDITS.md](CREDITS.md) for the full list with citations.

## License

The code is open source under the [MIT License](LICENSE), © 2026 Dan Sternof Beyer.
Data and third-party software keep their own licenses (see [CREDITS.md](CREDITS.md) and [data/README.md](data/README.md)).
