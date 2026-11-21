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
- `two-body-problem.html` (added 2026-11-20): working prototype. Two 12 km stars on a line, exact static Weyl /
  Israel–Khan solution. Light A → B along the line, clocks along the path, reference frames. Three views, including a
  rigorous true-length surface (two-star Flamm); the default grid is Flamm-style (the one-star page's grid built from
  that surface) with five anchors. All 32 physics self-tests pass (the checker takes ~10 s: it solves two surfaces).
- `milky-way-andromeda.html` (added 2026-11-20, owner's request after the two-star grid kept breaking): working
  prototype. Weak-field two-galaxy page. 12 physics self-tests pass.
- `index.html`: a landing page that links to each diagram.
- Planned next: the observable-universe sphere (centre = now, edge = recombination).

## Files that matter

| Path | Purpose |
|---|---|
| `index.html` | Landing page |
| `galaxy-map.html` | CfA2 galaxy map (physics core + three.js view) |
| `milky-way-andromeda.html` | Milky Way and Andromeda in weak-field gravity: light, clocks, observers, warped grid |
| `two-body-problem.html` | Two static stars (Weyl / Israel–Khan double Schwarzschild): light between them, clocks, observer frames |
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

## Decisions made: two body problem page

- Physics (owner's choice, 2026-11-20, from four options: weak-field sum, Weyl/Israel–Khan, Majumdar–Papapetrou,
  numerical relativity): the **exact static Weyl / Israel–Khan double Schwarzschild solution**. U = U₁ + U₂ exactly
  (rod potentials); γ has a closed form, checked against a numerical integration of its field equations. The bodies
  are held apart by a strut (conical singularity on the axis between them, γ = γ₀ there). The page draws it, gives its
  force next to Newton's, and says plainly that nothing real holds the stars still.
- Owner's goals for the page: (1) light reddens climbing out of star 1's well and blues falling into star 2's;
  (2) proper clocks along the path from A to B; (3) observers at different spots see time and redshift differently.
  Built for these: the "Along the beam" plot (clock rate and wavelength are one curve), a labelled row of clocks
  above the path, the reddest point (maximum of U on the axis), "Who measures what" table, O presets.
- Each star's outside is a Schwarzschild rod of its mass (exact for one star alone and for two black holes; tidal
  deformation of stars left out). Surface = where the star's own isolated Schwarzschild radius ½(R⁺+R⁻)+m equals 12 km.
  Masses 0.2–3.5 M☉ (below Buchdahl for one star). No black holes yet: in Weyl coordinates a horizon is a line segment.
- Distance control is the **ruler gap** between the facing surfaces along the axis (includes e^γ₀); the Weyl centre
  distance d is solved by bisection. A and B are fractions of that gap.
- Drawing is in Weyl coordinates (scene x = Weyl z, origin halfway between the rod centres; rho = distance from the
  x axis). A 12 km star appears as a spheroid with semi-axes R − m (along) and sqrt(R(R − 2m)) (across); heavier stars
  look smaller. Labels give the true radius.
- Anchored (geodesic) grid (owner's request, 2026-11-20; one of three grid styles): the one-star page's anchor options,
  generalised. Anchor = a point on the line (star 1's facing surface, the reddest point, star 2's facing surface, O's
  spot on the line, or far out = the grid's left end). Grid points keep their flat direction from the anchor and are
  placed at their flat distance in ruler length along spatial geodesics (Riemann normal coordinates). Geodesics from an
  axis point stay in a meridian plane, so `PhysicsCore.geodesicFan` (241 headings, 1 km steps, RK4 of
  dz/ds = e^(−f)cosψ, dρ/ds = e^(−f)sinψ, dψ/ds = e^(−f)(f_ρ cosψ − f_z sinψ), f = γ − U, γ' from its field
  equations) covers all space by rotation; ~0.1–0.2 s per rebuild. Paths stop at a star, so each star casts a shadow
  (left empty); with the far anchor the shadow behind star 1 is large. Grid clocks ride on the moved vertices.
  Checked against SciPy geodesics in Schwarzschild coordinates (one star) and with numerical potentials (two stars).
  Not the same picture as the one-star page with one star (that one is anchored on a sphere). Anchors between the stars
  sit on the strut (0.2% excess angle). Not built yet: anchors off the line (O anywhere, camera), which need 3D geodesics.
- Views: "Grid with ruler bands" (straight Weyl-coordinate lines, 20 km apart, with alternating bands every 5 km of true
  length, counted from the grid's middle planes; replaces the one-star page's warped ruler-coordinate grid, which has no
  unique two-body version) and "Clock-rate landscape" (plane through both stars sunk by 100 km × (1 − dτ/dt): a graph,
  not an embedding; Flamm's paraboloid has no exact two-body version). In an observer frame the landscape shows O's level.
- True-length surface (rebuilt 2026-11-20; conventions revised the same day after the owner reported holes and
  wiggles with widely separated stars): the plane through both stars embedded in flat 3D with true edge lengths.
  Lengths fix the curvature (static vacuum: R_ij = ∇_i∇_j N / N, plane curvature K = −∇N·∇ln c / N) but not the
  bending in the extra direction. Conventions now: (1) along the whole line, cos(tilt) = clock rate vs the fastest
  clock on that piece (far clock beyond the stars, reddest point's clock between them) — the owner's proper-time idea;
  (2) the least bent shape (smoothness weight SURFACE_SMOOTHNESS = 1e-3). Both exact Flamm for one star. One node on
  the line is held (gauge). The earlier pinned far edge (total-mass Flamm at 1000 km) was dropped: it fought the line
  rule when the stars were far apart, leaving domes and 1–3% length errors. Without (2), nearly flat regions (between
  far-apart stars) bent freely into 1–2 km bumps, which wrecked the downhill directions (holes, wiggles).
  Mesh: prolate spheroidal, graded to ~3 km next to the stars (SURFACE_MESH_SPACING), ~2,000–3,000 nodes. Solver:
  Levenberg–Marquardt, PCG with a banded Cholesky preconditioner (smoothness rows: diagonal only, to stay positive
  definite — keeping their in-band part broke CG), ~5–11 s, run a 30 ms slice per frame. Accuracy: lengths 0.014%
  RMS (default) / 0.03% (0.53 + 3.5 M☉, 300 km); agrees with an independent Python/SciPy rebuild to 0.04 km
  (self-tests); convergence: 0.25 km (default) to 0.4–0.8 km (300 km gap, far corners). Things tried and rejected
  (numbers in the session history): free edge + staged smoothing with L-BFGS (too slow, inexact), pinning a point
  (L1 = reddest point), height = function of the potential (2–3% length errors; needs each star's own mass near it),
  "always tilt toward faster clocks" (~10% of edges violate it), pinned far edge (see above).
- Flamm-style grid (owner's request, 2026-11-20; now the default grid): the one-star page's construction on the true-
  length surface. Drawing coordinates = the surface seen from above, turned about the line; each grid point slides
  along its downhill line until its true distance from the anchor equals its drawn distance (exactly ρ = r_a + ℓ(r_a, r)
  for one star; self-tests). Anchors: far (z∞ = 0.01 level, capped 900 km), each star's surface, the reddest point's
  level, O's level, the camera's level (redone when the camera moves 5%). `rasterizeSurface` (1 km, with a smooth slope
  field), `flammGridPoint`, map on a 2 km raster filled a few rows per frame (~1 s). Stars are drawn as their rims
  turned about the line; beam, strut, clocks in the same coordinates. Known: a crease where downhill lines part between
  the stars (the plane through the reddest point), and a tear there with the "stars' surfaces" anchor; slight
  unevenness right next to the stars (mesh scale ~3 km). Points exactly on the line start 0.2 km off it so they pass
  the reddest point's flat saddle. Starting camera steps back for wide gaps. While the surface is computing, the
  straight ruler-band grid stands in.
- Other grid styles kept: straightest paths (geodesics) from a point on the line, and straight with ruler bands.
- Light runs only along the axis (straight by symmetry): c dt = e^(γ₀−2U) dz, ruler dℓ = e^(γ₀−U) dz. Wave sampled evenly in
  L = ∫e^(γ₀−2U)dz. Same wave exaggeration and colour method as the one-star page.
- Not carried over from the one-star page (possible next steps): measuring sticks, radar distances, sky/apparent-size
  readouts, grid anchors, the Flamm line, black holes, light off the axis. Possible extra: exact Flamm-style surfaces of
  revolution for slices across the line (they show the strut as a region near the line that can't be embedded).

## Decisions made: Milky Way and Andromeda page

- Owner's direction (2026-11-20): use the two-body idea at galaxy scale (relationships between massive, distant
  objects), on a new page; keep the two-star page as the strong-field case.
- Physics: weak-field metric ds² = −(1+2Φ/c²)c²dt² + (1−2Φ/c²)dx², Φ = Φ_MW + Φ_M31 (|Φ|/c² ≤ ~3×10⁻⁶, so errors
  ~10⁻¹²). Still snapshot: during the 2.5 Myr crossing the galaxies close by ~0.3 kpc. No strut, no embedding problem.
- Mass models: Patel, Besla & Sohn 2017 Table 2 (MWa/MWb 1.0/1.5e12, M31a/M31b 1.5/2.0e12): NFW halo truncated at R_vir
  (halo mass = M_vir − disc − bulge, r_s = R_vir/c), Miyamoto–Nagai disc, Hernquist bulge. Their adiabatic contraction
  is NOT included: MWa then gives v_c(8.29 kpc) = 200 km/s vs measured ~239 (stated on the page). Discs in the plane of
  the line (orientations simplified). Distance default 761 kpc (Li et al. 2021).
- Grid: the one-star page's construction per galaxy (areal-gauge radial stretch, dℓ = (1 + G m(r)/(r c²)) dr with m the
  spherically averaged mass, disc monopole by Gauss–Legendre), moves added (linear). Anchors: far (2 Mpc), galaxies'
  centres, observer, camera. Moves are ~0.01–0.2 pc, drawn × the exaggeration slider (default 3×10⁵; at 10⁵ the bending
  is only ~3%, since halo mass is spread out). The same factor exaggerates the light's colour change, clock hand speed
  differences and the landscape depth; readouts are true.
- Redshift: gravitational (−3.75e-7 A→B by default) shown separately from Andromeda's Doppler (−109.3 km/s,
  van der Marel 2012), which is ~1000× larger. Shapiro delay ~2.4 yr, extra ruler length ~0.37 pc (isotropic coords).
- Not included: cosmic expansion (Local Group is bound), central black holes, galaxies' real orientations, M33/LMC.

## Known issues and open questions

- The recombination redshift (1089.92) comes from Planck 2018 VI Table 2. Verify it with `citation-verification`
  before using it on a page.
- `README.md` has no screenshot yet.
