# Spacetime Visualizations — notes for AI agents

Shared rules for all projects are in `../AGENTS.md`. This file adds project-specific ones.

## What this is

Interactive three.js pages showing spacetime physics: gravitational redshift (Schwarzschild),
warped-space visualizations, the observable universe, and real galaxy maps. The owner's top priority is
**mathematical rigor and scientific accuracy**. The owner's ideas and links are in `Goals and Links/`.

## Current state (2026-11-15)

- `galaxy-map.html`: working prototype, a 3D map of ~158,500 galaxies (CfA2 north + 6dFGS south + 2MRS whole sky). All 13 physics self-tests pass.
- `gravitational-redshift.html` (added 2026-11-16): working prototype. Radial light from A to B around a 12 km
  star or, above Buchdahl's limit (~3.6 M☉), a black hole. Views: warped cube grid and Flamm's paraboloid. All 16 physics self-tests pass.
  The owner asked to see this first version before more controls are added.
- `index.html`: a landing page that links to each diagram.
- Planned next: the observable-universe sphere (centre = now, edge = recombination).

## Files that matter

| Path | Purpose |
|---|---|
| `index.html` | Landing page |
| `galaxy-map.html` | CfA2 galaxy map (physics core + three.js view) |
| `gravitational-redshift.html` | Schwarzschild gravitational redshift: warped grid, Flamm's paraboloid, animated wave |
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

## Decisions made: gravitational redshift page

- Units are real: km and solar masses (IAU 2015 nominal GM☉). The body radius is fixed at 12 km.
- The animation clock is the distant observer's coordinate time t. The wave is sampled evenly in the tortoise
  coordinate r*, and its colour is the wavelength a static observer measures locally.
- The "speed of light" slider is **playback speed only**. Changing c physically is the same as changing the mass,
  since only r_s = 2GM/c² appears. This is explained on the page.
- Warped grid: laid out evenly in the ruler coordinate ρ = R + ℓ(R, r), anchored at the body's surface (or the horizon),
  drawn at areal r. A selector (owner's choice, 2026-11-16) switches the anchor to "far away" (r_a = where z = 0.01),
  which pulls lines toward the mass (the look of the reference image) but leaves a hole around heavy black holes.
  A third option, "at the observer", anchors at the reference frame's observer (follows the camera in the camera
  frame, rebuilding when it moves by more than 1%; equals "far away" in the far-away frame). A fourth, "at the camera",
  anchors at the camera's distance in any frame.
  The grid is nested (owner asked for no maximum distance, 2026-11-16): 20 km spacing out to 160 km, then spacing
  and reach double per level until z falls to 0.01 (`visibleExtentKm`, capped at 5000 km). Lines unique to a level
  fade out over the outer half of its reach. ρ → r is inverted with a lookup table.
- Layout (2026-11-17, owner's request): everything sits in the Flamm line's plane (z = 0). The beam (A → B), O and the
  radar scale run along +x (O shares the beam's radial line), the rulers along −x. In the grid view they are drawn
  0.4 km toward +z so they don't sit on the grid's x-axis line. Clocks skip the x axis (grid row k = 0; Flamm spokes are
  offset by half a step).
- 2026-11-17 tweaks: clock rate labels are percentages; a labelled clock line runs along −z (right angles to the cut,
  6 clocks per side, out to 240 km in the grid view, 140 km on Flamm's surface). Grid-view rulers lie flat (sideways
  rulers along z), and with the Flamm line on, a copy of each ruler is laid along the curve (full length) with faint
  links up to the 3D ones. A camera readout line (radius, clock %, sky factor) shows in the camera frame. A and B reach 200 km.
- Section cut (2026-11-17): optional; drops grid lines, flat-grid lines and grid clocks on the z > 0 side of the
  Flamm line's plane (z = 0), so the default camera looks at the cut face. Beam, rulers, O and labels are not cut.
- Optional Flamm embedding line in the grid view: the paraboloid's profile in the x–y plane at the same areal r,
  with markers under the x-axis grid vertices; arc length between markers equals their ρ spacing.
- Line brightness (owner's request, 2026-11-16), for the grid and Flamm's paraboloid: lines are invisible where space
  is nearly flat (z ≤ 0.01) and fully bright at the z the user picks with a slider (0.02–2, default 0.2, log scale),
  and nothing else cuts them off: grid and Flamm's surface both reach out to where z = 0.01. Faded lines are darkened, not alpha-blended:
  LineMaterial has no per-vertex alpha, and additive blending made a glowing wall.
- Measuring sticks (2026-11-16): 5 km rulers end to end from the surface, opposite the beam, out to r = 100 km, each
  with a sideways ruler at its middle. Grid view: radial ones are drawn shorter by ~sqrt(1 − r_s/r), sideways ones keep
  their length. Flamm view: all keep their length. Drawn without depth test (renderOrder 900) so the grid can't hide them.
- Reference frame (2026-11-16): far away (∞), a static observer O at a chosen radius (marker + its own clock), or a
  static observer at the camera (its distance from the centre; from the axis in the Flamm view). Clock labels and rim
  colours are relative to that observer (warm = slower, cool = faster), playback follows its clock, and readouts add
  "Redshift A → observer". Lengths and wave colours are deliberately unchanged: static observers share the same
  space slices, and the wave colours are local measurements. Built for static observers only.
- Radar distance and "what observers see" (2026-11-16): in observer frames a double scale along O's radial line
  (cyan = radar every 10 km on the observer's clock, orange = rulers every 10 km). Readouts: the body's apparent
  radius from far away (R/sqrt(1 − r_s/R), or the 2.598 r_s shadow when R < 1.5 r_s), the sky overhead seen by the
  observer (×sqrt(1 − r_s/r_O), small-angle, static observer only), and rulers vs radar down to the surface.
  The sky factor and shadow are checked against numerical ray tracing / minimisation in reference_values.py, but
  still need a published citation before the page is promoted. The owner may want a ray-traced view next.
  Remaining ideas, in the suggested order: a fog hemisphere
  (density = 1/sqrt(1 − r_s/r) − 1, which equals z), then a free-fall (Gullstrand–Painlevé "river") view.
- Proper-time clocks: at every second grid vertex in the plane through the centre (Flamm view: rings × 8 spokes),
  plus larger clocks at A and B. Hands turn at dτ/dt; a far clock turns once per 100 µs of t, on the light's playback.
  Clocks are drawn last with depthTest off and per-frame back-to-front renderOrder, and are hidden by a ray test when
  behind the central body. With depth testing they flickered (z-fighting at ~300 km, and grid lines through each vertex).
  The camera's near plane is 1 km for the same reason.
  This is one stated choice among several (see pitfalls.md); the alternatives are Gullstrand–Painlevé flow lines
  or drawing in proper distance.
- Wave length on screen is exaggerated by about 1.3 × 10¹⁰ (stated on the page); everything else is true scale.

## Known issues and open questions

- The recombination redshift (1089.92) comes from Planck 2018 VI Table 2. Verify it with `citation-verification`
  before using it on a page.
- `README.md` has no screenshot yet.
