---
name: spacetime-physics
description: Rules and tools for keeping this project's three.js spacetime visualizations mathematically rigorous and scientifically accurate. Use whenever writing or changing physics in a page (Schwarzschild geometry, gravitational redshift, time dilation, light bending, embedding diagrams, warped grids, FLRW cosmology, cosmological redshift, the observable universe, recombination and the CMB), when choosing how to draw a physical quantity, when a number on screen needs a source, or when asked "is this right?" about anything a page shows.
---

# Spacetime physics: accuracy rules for this project

Every page here is a single standalone `index.html` (or one page per diagram) built on
three.js. These rules make sure what it shows is real physics and that anyone can check it.

## The five rules

1. **Every formula has a source.** Before coding, write the equation, its symbols with units,
   its assumptions (vacuum, static observer, weak field, flat universe…), and a citation into
   the page's *Physics notes* (see below). Take equations from `references/equations.md` or
   from a textbook or paper you can name. If you can't name a source, say so and ask.
   Never cite a paper from memory: check it with the `citation-verification` skill.
2. **Physics lives in one pure block.** All physics goes between the markers
   `// ===== PHYSICS CORE START =====` and `// ===== PHYSICS CORE END =====` inside the page.
   No three.js, no DOM, no globals except `Math`. It defines `PhysicsCore` (the functions) and
   `PhysicsSelfTests` (the checks). Rendering code calls `PhysicsCore` and never computes physics itself.
3. **Numbers are checked against independent values.** Each `PhysicsCore` function gets at least one
   self-test against a value computed independently: an experimental result, or Astropy
   via `scripts/reference_values.py`. Run `scripts/check_physics.mjs` after every physics change.
   Never mark a test as passing by copying the page's own output into `expected`.
4. **Honest drawing.** Keep what is *physical* separate from what is a *visual choice*:
   - Exaggeration factors, log scales, color maps and "rubber sheet" style pictures are allowed,
     but the page must label them on screen (e.g. "vertical scale ×1000", "log radius").
   - Readouts (redshift, time-dilation factor, distance, age) always show the true, unexaggerated value
     with units.
   - Say which observer a number belongs to (e.g. "as measured by a static observer at infinity").
5. **State limits instead of hiding them.** If a model breaks down (inside the horizon, at strong fields
   for a weak-field formula, non-flat cosmologies), clamp or disable the control at that point and
   say why on the page.

## Workflow for a new diagram

1. Read `references/equations.md` and `references/pitfalls.md` for the topic.
2. Write the *Physics notes* (equations, assumptions, sources, visual choices) before coding.
3. Run `uv run .claude/skills/spacetime-physics/scripts/reference_values.py` to (re)generate
   `physics/reference-values.json` and `physics/reference-values.md` at the project root.
   For a value that isn't there yet, add it to the script rather than computing it by hand.
4. Write `PhysicsCore` and `PhysicsSelfTests`, following `references/selftest-pattern.md`.
5. Run `node .claude/skills/spacetime-physics/scripts/check_physics.mjs index.html`.
   It runs every self-test and confirms that each `refKey` still matches the JSON.
6. Build the three.js view on top. Open the page with `?selftest` and confirm the on-page panel shows all tests passing.
7. When reporting to the user, list what was checked, against what, and any open uncertainty.

## Physics notes section (required in every page)

A collapsible panel (and a matching comment block at the top of the physics core) with:

- **Model**: e.g. "Schwarzschild vacuum exterior, non-rotating, uncharged mass M".
- **Equations**: each one written out, with symbols and units.
- **Assumptions and limits**: observers, approximations, valid ranges.
- **Visual choices**: what is exaggerated or metaphorical and by how much.
- **Sources**: textbook or paper with section/equation number, or a verified DOI/arXiv id.
- **Constants**: which values (CODATA 2018 via Astropy, IAU 2015 nominal solar values, Planck 2018 cosmology).

## Showing equations and using real data

- Show equations on the page with KaTeX loaded from a CDN at a pinned version, so the Physics notes
  read like math rather than code.
- Real survey data (e.g. the CfA Redshift Survey, ZCAT) keeps its own terms: credit the
  source in the page and in `README.md`, and ask the owner before publishing. A position
  computed from redshift is in *redshift space*. Peculiar velocities stretch clusters along the
  line of sight ("fingers of God"), so say so wherever a catalog is drawn in 3D.
  Convert redshift to distance with Astropy's Planck18 comoving distance, not with d = cz/H₀
  beyond z ≈ 0.05.

## Tools in this skill

| File | What it does |
|---|---|
| `references/equations.md` | The vetted equations for this project's topics, with sources |
| `references/pitfalls.md` | Common physics and visualization mistakes for these topics |
| `references/selftest-pattern.md` | How to write `PhysicsCore` / `PhysicsSelfTests` and the on-page test panel |
| `scripts/reference_values.py` | Astropy-based independent values (uv installs Astropy itself) |
| `scripts/check_physics.mjs` | Runs a page's physics self-tests in Node, no browser needed |

## Related skills in this project

- `astropy`: how to use Astropy for anything the reference script doesn't cover yet.
- `uncertainty-and-units`: unit audits and plausibility checks on new numbers.
- `citation-verification`: confirms that every cited paper exists and says what we claim.
