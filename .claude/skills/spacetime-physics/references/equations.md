# Vetted equations for this project

Units are SI unless stated otherwise. `G` is the gravitational constant, `c` the speed of light,
`M` the mass. Sources are listed at the bottom: run each through `citation-verification` before
it appears on a page.

---

## 1. Schwarzschild geometry (non-rotating, uncharged mass, vacuum outside it)

**Metric** (Schwarzschild coordinates t, r, θ, φ):

    ds² = −(1 − r_s/r) c² dt² + (1 − r_s/r)⁻¹ dr² + r² (dθ² + sin²θ dφ²)

**Schwarzschild radius**: `r_s = 2GM/c²`  [m]. Sun ≈ 2.95 km, Earth ≈ 8.87 mm.

`r` is the *areal* radius: a sphere at r has area 4πr². It is **not** the distance from the centre.

Valid only outside the mass and outside the horizon (r > r_s, and r > the body's surface for stars/planets).

### Gravitational time dilation (static clock)

    dτ/dt = √(1 − r_s/r)

τ is the static clock's proper time, t the time of a static observer at infinity.

### Gravitational redshift

Static emitter at r_e, static receiver at r_r:

    1 + z = ν_e / ν_r = λ_r / λ_e = √( (1 − r_s/r_r) / (1 − r_s/r_e) )

Receiver at infinity (this project's default frame):

    1 + z = (1 − r_s/r_e)^(−1/2)

Weak-field limit (r ≫ r_s): `z ≈ GM/(r c²) = r_s/(2r)`. Near Earth's surface, for a height difference h:
`Δν/ν ≈ g h / c²` (Pound–Rebka).

The result depends only on where the emitter and receiver sit, not on the path the light takes in between.

### Proper radial distance (what a ruler measures, at fixed t)

    ℓ(r₁, r₂) = ∫ dr / √(1 − r_s/r)
             = [ √(r(r − r_s)) + r_s · ln( √r + √(r − r_s) ) ] evaluated from r₁ to r₂    (r₁, r₂ ≥ r_s)

Always larger than r₂ − r₁. This is the stretching that a "warped grid" should show radially.

### Flamm's paraboloid (embedding diagram of the equatorial plane at fixed t)

    w(r) = 2 √( r_s (r − r_s) )

Rotating this curve about the vertical axis gives a surface in flat 3D whose intrinsic geometry
equals the equatorial slice (θ = π/2, t = const). The vertical axis w has **no physical meaning**:
it is an extra dimension added only for the embedding. Real geometry; no exaggeration needed, but
for the Sun at true scale the surface is almost flat (see pitfalls).

### Characteristic radii

| Radius | Value | Meaning |
|---|---|---|
| Event horizon | r = r_s | Static observers impossible inside |
| Photon sphere | r = 1.5 r_s | Unstable circular light orbits |
| ISCO | r = 3 r_s | Innermost stable circular orbit, massive particles |

### Light deflection (weak field)

    α = 4GM / (c² b) = 2 r_s / b       [radians], b = impact parameter

Sun, grazing the limb: ≈ 1.75″ (the 1919 eclipse test).

### Perihelion advance (weak field), per orbit

    Δφ = 6π GM / ( c² a (1 − e²) )

Mercury: ≈ 43″ per century.

### Shapiro delay (round trip, weak field, Sun between Earth and target)

    Δt ≈ (2 r_s / c) · ln( 4 r_E r_P / b² )       (r_E, r_P ≫ b)

---

## 2. Special relativity (for observers in motion)

    γ = 1 / √(1 − v²/c²)
    Time dilation:   Δτ = Δt / γ
    Length contraction:   L = L₀ / γ
    Relativistic Doppler (radial, source receding at v):   1 + z = √( (1 + β) / (1 − β) ),  β = v/c
    Transverse Doppler (motion ⟂ line of sight, in the receiver frame):   1 + z = γ

Combined clock rate for a circular orbit in weak field (e.g. GPS), relative to a clock at infinity:

    dτ/dt ≈ 1 − GM/(r c²) − v²/(2c²)

---

## 3. FLRW cosmology (homogeneous, isotropic expanding universe)

**Metric** (flat case, k = 0, comoving coordinates):

    ds² = −c² dt² + a(t)² [ dχ² + χ² dΩ² ]

a(t) is the scale factor, a(t₀) = 1 today. χ is comoving distance.

**Cosmological redshift**: `1 + z = a(t_observed) / a(t_emitted)`. It depends only on the ratio of the
scale factors at emission and reception, not on anything else along the path.

**Friedmann equation** (as H(z)):

    H(z) = H₀ · √( Ω_r (1+z)⁴ + Ω_m (1+z)³ + Ω_k (1+z)² + Ω_Λ )
    E(z) = H(z) / H₀

**Distances** (Hogg 1999 notation, flat universe):

    Comoving (line-of-sight) distance:   D_C(z) = c ∫₀^z dz' / H(z')
    Proper distance today:               D_C(z)          (where the source is *now*)
    Proper distance at emission:         D_C(z) / (1 + z)
    Luminosity distance:                 D_L = (1 + z) D_C
    Angular-diameter distance:           D_A = D_C / (1 + z)

**Times**:

    Age at redshift z:   t(z) = ∫_z^∞ dz' / ( (1 + z') H(z') )
    Lookback time:       t_L(z) = t(0) − t(z)

**Particle horizon** (radius of the observable universe, comoving): `D_C(z → ∞)` ≈ 46 billion light-years
(about 14.3 Gpc) for Planck 2018 values. Light-travel distance is the lookback time × c and is a different number.

**Recombination / last scattering**: z* ≈ 1090 (Planck 2018 gives z* to ±0.25). Age then ≈ 380,000 years.
Take the exact value and its uncertainty from Planck 2018 VI, Table 2, and compute the age with Astropy;
don't hard-code a value from memory.

Use `astropy.cosmology.Planck18` for all numbers. It includes radiation and neutrinos, which matter at high z.

---

## Sources (verify before citing on a page)

- S. Carroll, *Spacetime and Geometry* (2004), ch. 5: Schwarzschild solution, ch. 8: cosmology.
- J. Hartle, *Gravity: An Introduction to Einstein's General Relativity* (2003), ch. 9–10, 18–19.
- C. Misner, K. Thorne, J. Wheeler, *Gravitation* (1973): embedding diagrams, Schwarzschild geometry.
- D. Hogg, "Distance measures in cosmology", arXiv:astro-ph/9905116.
- C. Will, "The Confrontation between General Relativity and Experiment", Living Rev. Relativ. 17, 4 (2014), arXiv:1403.7377.
- N. Ashby, "Relativity in the Global Positioning System", Living Rev. Relativ. 6, 1 (2003).
- R. Pound & G. Rebka, Phys. Rev. Lett. 4, 337 (1960).
- Planck Collaboration, "Planck 2018 results. VI. Cosmological parameters", arXiv:1807.06209.
