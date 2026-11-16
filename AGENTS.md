# Spacetime Visualizations — notes for AI agents

Shared rules for all projects are in `../AGENTS.md`. This file adds project-specific ones.

## What this is

Interactive three.js pages showing spacetime physics: gravitational redshift (Schwarzschild),
warped-space visualizations, the observable universe, and real galaxy maps. The owner's top priority is
**mathematical rigor and scientific accuracy**. The owner's ideas and links are in `Goals and Links/`.

## Current state (2026-11-15)

- `galaxy-map.html`: working prototype, a 3D map of ~158,500 galaxies (CfA2 north + 6dFGS south + 2MRS whole sky). All 13 physics self-tests pass.
- `index.html`: a landing page that links to each diagram.
- Planned next: gravitational redshift (Schwarzschild, observer at infinity, warped grid and embedding views),
  and the observable-universe sphere (centre = now, edge = recombination).

## Files that matter

| Path | Purpose |
|---|---|
| `index.html` | Landing page |
| `galaxy-map.html` | CfA2 galaxy map (physics core + three.js view) |
| `data/cfa2-galaxies.js` | CfA2 galaxy data, generated; don't edit by hand |
| `data/2mrs-galaxies.js` | 2MRS galaxy data (journal/VizieR copy), CfA2 and 6dFGS duplicates removed; built by `data/build_2mrs.py` (run last) |
| `data/2mrs-redshift-sources.md` | Generated list of every paper behind the 2MRS redshifts shown (required citation) |
| `data/6dfgs-galaxies.js` | 6dFGS galaxy data, CfA2 duplicates removed; built by `data/build_6dfgs.py` (run after `build_cfa2.py`) |
| `data/build_cfa2.py` | Builds it from `data/raw/cfa2.dat` (`uv run data/build_cfa2.py`) |
| `data/README.md` | Data source, checks, terms |
| `physics/reference-values.{json,md}` | Astropy-computed reference values; generated, don't edit |
| `.claude/skills/spacetime-physics/` | **Read this skill before any physics work**: rules, equations, pitfalls, tools |
| `.claude/skills/{astropy,uncertainty-and-units,citation-verification}/` | Vendored Kalaris Labs skills (MIT) |
| `CREDITS.md` | Every data source, paper and tool used. **Update it when you add one.** |

## Rules for this project

1. Follow the `spacetime-physics` skill: equations with sources, a pure physics core between the
   `PHYSICS CORE START/END` markers, self-tests against independent values, honest labelling of exaggerations.
2. Run `node .claude/skills/spacetime-physics/scripts/check_physics.mjs <page>.html` after any physics change.
3. Never type a reference value by hand: add it to `reference_values.py` and regenerate.
4. Credit everything: add each new data set, paper, library or skill to `CREDITS.md`, and data sources
   to the page footer too. Any page using 6dFGS data must say it is from the Final Release of 6dFGS and cite Jones et al. 2004 and 2009.
   Any page using 2MRS data must cite Huchra et al. 2012 and link to `data/2mrs-redshift-sources.md`; use the
   journal/VizieR copy, not the files from the 2MRS site (they ask not to be redistributed).
   Any page using CfA data must credit the **Smithsonian Astrophysical Observatory**
   and link to https://lweb.cfa.harvard.edu/~dfabricant/huchra/zcat/ . That was the owner's condition
   for publishing it.
5. Third-party files of unknown license stay out of git (see `.gitignore`), e.g. `docs/Spacetime_warp_3D_grid.png`
   and `data/raw/`.
6. The owner has approved publishing the CfA data (with the credit and link above). Still ask before every `git push`.

## Viewing

- Live: https://dansternofbeyer.github.io/spacetime-visualizations/ (GitHub Pages from `main`, root). Every push
  to `main` updates it. Footer license and credits links point to the GitHub-rendered files, because Pages
  serves `.md` and `LICENSE` raw.

- Double-click any page. The data loads with a plain `<script>` tag, so it works without a server.
- The Claude desktop app's browser pane opens local files as snapshots without their data files. To preview there,
  use the `spacetime-static` server in `../.claude/launch.json` (http://localhost:8737).

## Known issues and open questions

- The recombination redshift (1089.92) comes from Planck 2018 VI Table 2. Verify it with `citation-verification`
  before using it on a page.
- `README.md` has no screenshot yet.
