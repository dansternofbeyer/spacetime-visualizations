# Self-test pattern

Each page keeps its physics in one pure block that both the browser and Node can run.

## In the page

```html
<script>
// ===== PHYSICS CORE START =====
// Physics notes: Schwarzschild exterior, static observer at infinity.
// Sources: Carroll (2004) ch. 5; Hartle (2003) ch. 9. Constants: CODATA 2018 / IAU 2015 via Astropy.

const PhysicsConstants = {
  speedOfLight: 299792458,              // m/s, exact
  gravitationalConstant: 6.67430e-11,   // m^3 kg^-1 s^-2, CODATA 2018
  solarGM: 1.3271244e20,                // m^3 s^-2, IAU 2015 nominal
};

const PhysicsCore = {
  /** Schwarzschild radius r_s = 2GM/c^2, in metres, from GM in m^3/s^2. */
  schwarzschildRadius(gravitationalParameter) {
    return 2 * gravitationalParameter / PhysicsConstants.speedOfLight ** 2;
  },

  /** Redshift z of light from a static emitter at radius r, received at infinity. */
  gravitationalRedshiftToInfinity(emitterRadius, schwarzschildRadius) {
    if (emitterRadius <= schwarzschildRadius) return Infinity;   // no static emitters inside the horizon
    return 1 / Math.sqrt(1 - schwarzschildRadius / emitterRadius) - 1;
  },
};

// Each test: name, actual() computes with PhysicsCore, expected is a literal value,
// tolerance is relative, refKey (optional) names the matching entry in
// physics/reference-values.json so Node can confirm the literal is still current.
const PhysicsSelfTests = [
  {
    name: "Schwarzschild radius of the Sun",
    actual: () => PhysicsCore.schwarzschildRadius(PhysicsConstants.solarGM),
    expected: 2953.25,
    relativeTolerance: 1e-5,
    refKey: "sun.schwarzschild_radius_m",
    source: "Astropy 7.2 constants (IAU 2015 nominal GM_sun)",
  },
];
// ===== PHYSICS CORE END =====
</script>
```

Rules:
- Inside the markers: only `const` declarations and plain functions. No `document`, `window`, `THREE`, `import`.
- `expected` must come from `physics/reference-values.json`, an experiment, or a cited paper,
  never from running `actual()`.
- Add tests at the edges too: limits (r → ∞ gives z → 0), the weak-field approximation agreeing with the full
  formula at r = 10⁶ r_s, clamping at the horizon.

## On-page panel (shown when the URL contains `?selftest`)

```js
// ===== Self-test panel =====
function runPhysicsSelfTests() {
  return PhysicsSelfTests.map((test) => {
    const actualValue = test.actual();
    const relativeError = Math.abs(actualValue - test.expected) / Math.abs(test.expected);
    return { ...test, actualValue, relativeError, passed: relativeError <= test.relativeTolerance };
  });
}

function showSelfTestPanel() {
  const results = runPhysicsSelfTests();
  const panel = document.createElement("pre");
  panel.className = "selftest-panel";
  panel.textContent = results
    .map((r) => `${r.passed ? "PASS" : "FAIL"}  ${r.name}: ${r.actualValue.toPrecision(8)} vs ${r.expected} (rel. err ${r.relativeError.toExponential(2)})`)
    .join("\n");
  document.body.appendChild(panel);
}

if (new URLSearchParams(location.search).has("selftest")) showSelfTestPanel();
```

## From the command line

```bash
node .claude/skills/spacetime-physics/scripts/check_physics.mjs index.html
node .claude/skills/spacetime-physics/scripts/check_physics.mjs index.html --reference physics/reference-values.json
```

Exit status is 0 if every test passes and every `refKey` matches, 1 otherwise.
