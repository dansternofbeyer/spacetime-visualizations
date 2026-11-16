# Pitfalls: common mistakes for this project's topics

## Drawing curved spacetime

- **The rubber-sheet picture is a metaphor.** A ball rolling on a dented sheet "falls" because of
  the sheet's gravity, which is circular reasoning. Flamm's paraboloid is a real embedding of
  *space* at one instant, but it shows only spatial curvature. Ordinary falling (apples, orbits) is
  mostly time curvature (gravitational time dilation), which an embedding can't show.
  Label the picture for what it is.
- **The vertical axis of an embedding diagram means nothing physical.** Don't label it "depth" or "gravity".
- **True scale is almost flat.** For the Sun, the paraboloid's slope at the surface is
  dw/dr = √(r_s/(R − r_s)) ≈ 0.002 (about 0.12°), so any visible dent is exaggerated: say by how much.
  (`reference_values.py` computes this as `sun.embedding_slope_at_surface`.)
- **A warped 3D cubic grid has no single "correct" form.** Picking one means choosing coordinates.
  Defensible options:
  (a) radial grid spacing in *proper distance* (stretching from equations.md §1),
  (b) grid lines pulled along infalling geodesics (Gullstrand–Painlevé "river" picture),
  (c) color or density showing the time-dilation factor.
  Name the choice on screen. Don't invent a displacement formula that looks right.
- **Don't extrapolate r to the centre.** Inside a star the exterior metric doesn't apply. Inside r_s, static
  quantities (redshift of a static emitter, proper time of a static clock) have no meaning: clamp the control.

## Redshift

- **Three kinds of redshift, each with its own formula**: Doppler (relative motion), gravitational
  (different potentials), cosmological (scale-factor ratio). Don't mix them, and say which one is shown.
- **Gravitational redshift needs a receiver.** Default here: static observer at infinity. If the receiver
  moves or sits somewhere else, use the two-radius formula.
- **Wavelength → color.** A redshifted visible photon can leave the visible range. Map wavelength to RGB
  with a stated method (e.g. CIE 1931 colour-matching functions), and show the wavelength numerically
  when it's outside 380–750 nm.

## Cosmology

- **"Distance" is ambiguous.** Comoving, proper-at-emission, luminosity, angular-diameter and light-travel
  distance all differ. Always name which one is shown.
- **The observable universe isn't 13.8 billion light-years in radius.** That's the lookback time.
  The comoving radius is ≈ 46 billion light-years.
- **A sphere whose radius is lookback time** (centre = now, edge = recombination) is a legitimate
  diagram of our past light cone, but it isn't a spatial map. Label the radial axis
  "time before now", and show the comoving distance of each shell separately if needed.
- **The past light cone in comoving coordinates is not a straight cone.** The proper distance at emission peaks
  at z ≈ 1.6 and then *shrinks*. Objects we see at high z were *closer* to us when the light left.
- **Expansion isn't motion through space.** Redshifts can exceed what any velocity < c would give
  through the SR Doppler formula. Don't convert z to "recession velocity" with special relativity.
- **Bound systems don't expand.** Galaxies, the Solar System and atoms stay the same size.

## The "expanding fog" question (from the project ideas)

- If the *space* the light travels through expands, the light redshifts by
  `a(received)/a(emitted)` whatever the fog's density is.
- If the fog only *thins out* because its particles move apart through static space, the light passing
  through gets no redshift from that (apart from tiny Doppler shifts from scattering off moving particles).
  Density alone doesn't change frequency.
- If matter collapses into clumps *elsewhere* (not where the light is), the light is affected
  only if it crosses those changing gravitational potentials. That is the integrated Sachs–Wolfe /
  Rees–Sciama effect, a small effect that can be computed.
- Answer this on a page with the scale-factor model, and say plainly which of these three cases is shown.

## Numerics

- Use `1 − r_s/r` carefully near r ≈ r_s: guard with a small epsilon and clamp. Don't return NaN to the renderer.
- Cosmology integrals at high z: integrate in ln(1+z) or use Astropy-precomputed tables embedded in
  the page. Check them with a self-test against Astropy at z = 0.5, 2, 10, 1090.
- JavaScript numbers are doubles (~15–16 digits). Weak-field values such as 1 − 2×10⁻⁶ are fine,
  but compute small differences directly (e.g. use `-Math.expm1(0.5*Math.log1p(-x))`-style forms) when
  they matter.
