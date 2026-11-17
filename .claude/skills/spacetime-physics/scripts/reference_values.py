# /// script
# requires-python = ">=3.11"
# dependencies = ["astropy==7.2.0", "numpy>=1.26", "scipy>=1.13"]
# ///
"""
Reference values for the Spacetime Visualizations project.

Computes physics values with Astropy (constants, Planck 2018 cosmology) and plain
numerical integration, so a page's JavaScript can be checked against values that
were computed independently of it.

Writes two files at the project root:
    physics/reference-values.json   machine-readable, read by check_physics.mjs
    physics/reference-values.md     the same values as a table, for people

Run from anywhere:
    uv run .claude/skills/spacetime-physics/scripts/reference_values.py

To add a value: write a small function below that returns it, then register it in
build_reference_values(). Never type a result in by hand.
"""

import datetime
import json
import math
from pathlib import Path

import astropy
import astropy.constants as const
import astropy.units as u
import numpy as np
from astropy.cosmology import Planck18

# ===== Paths =====

PROJECT_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_FOLDER = PROJECT_ROOT / "physics"

# ===== Inputs that are not in Astropy (each with its source) =====

# Mercury's orbit: JPL "Keplerian Elements for Approximate Positions of the Major Planets"
# (E. M. Standish), J2000 elements.
MERCURY_SEMI_MAJOR_AXIS = 0.38709927 * u.AU
MERCURY_ECCENTRICITY = 0.20563593

# GPS orbit semi-major axis: N. Ashby, Living Rev. Relativ. 6, 1 (2003).
GPS_SEMI_MAJOR_AXIS = 26561.75 * u.km

# Pound–Rebka tower height: Pound & Rebka, Phys. Rev. Lett. 4, 337 (1960).
POUND_REBKA_HEIGHT = 22.5 * u.m
STANDARD_GRAVITY = 9.80665 * u.m / u.s**2  # exact by definition (CGPM 1901)

# Example neutron star (a model, not a measured object).
NEUTRON_STAR_MASS = 1.4 * const.M_sun
NEUTRON_STAR_RADIUS = 12 * u.km

# Recombination (last scattering) redshift: Planck 2018 results VI (arXiv:1807.06209),
# Table 2, TT,TE,EE+lowE+lensing column. Verify against the paper before relying on it.
RECOMBINATION_REDSHIFT = 1089.92

SECONDS_PER_DAY = 86400.0
DAYS_PER_JULIAN_CENTURY = 36525.0
SPEED_OF_LIGHT = const.c


# ===== Schwarzschild geometry =====

def schwarzschild_radius(gravitational_parameter):
    """r_s = 2GM/c^2."""
    return (2 * gravitational_parameter / SPEED_OF_LIGHT**2).to(u.m)


def redshift_to_infinity(emitter_radius, schwarzschild_radius_value):
    """1 + z = (1 - r_s/r)^(-1/2) for a static emitter, receiver at infinity."""
    ratio = (schwarzschild_radius_value / emitter_radius).to_value(u.one)
    return 1 / math.sqrt(1 - ratio) - 1


def proper_radial_distance_numeric(inner_radius_in_rs, outer_radius_in_rs, steps=200_001):
    """
    Integral of dr / sqrt(1 - r_s/r), in units of r_s, done numerically.

    Substituting r = 1 + s^2 (units of r_s) removes the 1/sqrt singularity at the horizon,
    giving the smooth integrand 2*sqrt(1 + s^2). This is deliberately independent of the
    closed-form expression that pages use, so it can check it.
    """
    s_start = math.sqrt(inner_radius_in_rs - 1)
    s_end = math.sqrt(outer_radius_in_rs - 1)
    s_values = np.linspace(s_start, s_end, steps)
    integrand = 2 * np.sqrt(1 + s_values**2)
    return float(np.trapezoid(integrand, s_values))


def coordinate_light_time_numeric(inner_radius_in_rs, outer_radius_in_rs):
    """
    Schwarzschild coordinate time for radial light, c*dt = dr / (1 - r_s/r), in units of r_s,
    integrated numerically (independent of the closed-form tortoise coordinate pages use).
    """
    from scipy.integrate import quad

    return quad(lambda r: 1 / (1 - 1 / r), inner_radius_in_rs, outer_radius_in_rs, epsabs=0, epsrel=1e-12)[0]


def flamm_height_numeric(inner_radius_in_rs, outer_radius_in_rs):
    """
    Height gained on Flamm's paraboloid, integrating the embedding condition
    dw/dr = sqrt(1/(1 - r_s/r) - 1) numerically, in units of r_s.
    """
    from scipy.integrate import quad

    return quad(lambda r: math.sqrt(1 / (1 - 1 / r) - 1), inner_radius_in_rs, outer_radius_in_rs, epsabs=0, epsrel=1e-12)[0]


def overhead_angle_ratio_numeric(observer_radius_in_rs, source_distance_in_rs=1e7, source_angle=1e-5):
    """
    How much smaller a distant object near the zenith looks to a static observer at r_O than it would
    with no mass, found by tracing light rays numerically (independent of the closed form sqrt(1 - r_s/r_O)).

    A ray with impact parameter b sweeps dphi/dr = b / (r^2 sqrt(1 - (1 - r_s/r) b^2 / r^2)) (units of r_s).
    Find the b whose ray from the observer reaches the source's angular position, then convert to the angle a
    static observer measures, sin(alpha) = b sqrt(1 - r_s/r) / r. Repeat with no mass and take the ratio.
    """
    from scipy.integrate import quad
    from scipy.optimize import brentq

    def swept_angle(impact_parameter, mass_factor):
        integrand = lambda r: impact_parameter / (r * r * math.sqrt(1 - (1 - mass_factor / r) * impact_parameter**2 / r**2))
        breakpoints = [observer_radius_in_rs, 10 * observer_radius_in_rs, 1e3, 1e5, source_distance_in_rs]
        breakpoints = sorted(set(point for point in breakpoints if observer_radius_in_rs <= point <= source_distance_in_rs))
        return sum(quad(integrand, low, high, epsabs=0, epsrel=1e-12, limit=200)[0] for low, high in zip(breakpoints, breakpoints[1:]))

    def observed_angle(mass_factor):
        impact_parameter = brentq(lambda b: swept_angle(b, mass_factor) - source_angle, 1e-15, 1.0, xtol=1e-22, rtol=1e-14)
        return math.asin(impact_parameter * math.sqrt(1 - mass_factor / observer_radius_in_rs) / observer_radius_in_rs)

    return observed_angle(1.0) / observed_angle(0.0)


def shadow_radius_numeric():
    """Smallest impact parameter b = r / sqrt(1 - r_s/r) of a circular light orbit, by numerical minimisation (units of r_s)."""
    from scipy.optimize import minimize_scalar

    result = minimize_scalar(lambda r: r / math.sqrt(1 - 1 / r), bounds=(1.01, 10), method="bounded", options={"xatol": 1e-12})
    return float(result.fun)


def light_deflection_arcsec(gravitational_parameter, impact_parameter):
    """alpha = 4GM / (c^2 b), weak field."""
    angle = 4 * gravitational_parameter / (SPEED_OF_LIGHT**2 * impact_parameter)
    return (angle.to(u.one) * u.rad).to_value(u.arcsec)


def perihelion_advance_arcsec_per_century(gravitational_parameter, semi_major_axis, eccentricity):
    """6 pi GM / (c^2 a (1 - e^2)) per orbit, times orbits per Julian century."""
    per_orbit_rad = 6 * math.pi * gravitational_parameter / (SPEED_OF_LIGHT**2 * semi_major_axis * (1 - eccentricity**2))
    orbital_period = 2 * math.pi * np.sqrt(semi_major_axis**3 / gravitational_parameter)
    orbits_per_century = (DAYS_PER_JULIAN_CENTURY * u.day / orbital_period).to_value(u.one)
    return (per_orbit_rad.to(u.one) * u.rad).to_value(u.arcsec) * orbits_per_century


def gps_clock_rates_microseconds_per_day():
    """
    Weak-field clock rate of a GPS satellite relative to a clock on the ground.
    Simplified model: spherical non-rotating Earth, circular orbit. Earth's rotation and
    oblateness are left out (together a few tenths of a microsecond per day).
    """
    gm = const.GM_earth
    ground_radius = const.R_earth
    gravitational = (gm / SPEED_OF_LIGHT**2 * (1 / ground_radius - 1 / GPS_SEMI_MAJOR_AXIS)).to_value(u.one)
    orbital_speed_squared = gm / GPS_SEMI_MAJOR_AXIS
    velocity = -(orbital_speed_squared / (2 * SPEED_OF_LIGHT**2)).to_value(u.one)
    to_microseconds_per_day = SECONDS_PER_DAY * 1e6
    return gravitational * to_microseconds_per_day, velocity * to_microseconds_per_day


# ===== Cosmology (Planck 2018 via Astropy) =====

def comoving_distance_gly(redshift):
    return Planck18.comoving_distance(redshift).to_value(u.lyr) / 1e9


def particle_horizon_comoving_gly(effective_infinity_redshift=1e10):
    """
    Comoving radius of the observable universe, c * integral_0^inf dz / H(z).

    Astropy's own integral fails to converge for z ~ 1e8 (it silently returned about
    half the right answer), so integrate in x = ln(1 + z), where the integrand
    (1 + z) / E(z) is smooth and falls off like (1 + z)^-1 in the radiation era.
    """
    from scipy.integrate import quad

    def integrand(log_one_plus_z):
        one_plus_z = math.exp(log_one_plus_z)
        return Planck18.inv_efunc(one_plus_z - 1) * one_plus_z

    upper_limit = math.log1p(effective_infinity_redshift)
    breakpoints = [0.0, math.log1p(1), math.log1p(10), math.log1p(1e3), math.log1p(1e5), upper_limit]
    integral = sum(
        quad(integrand, low, high, epsabs=0, epsrel=1e-10, limit=200)[0]
        for low, high in zip(breakpoints, breakpoints[1:])
    )
    hubble_distance = (SPEED_OF_LIGHT / Planck18.H0).to(u.lyr)
    return (integral * hubble_distance).to_value(u.lyr) / 1e9


def redshift_of_max_angular_diameter_distance():
    """The redshift where proper distance at emission (= D_A in a flat universe) peaks."""
    redshifts = np.linspace(0.5, 3.0, 25_001)
    distances = Planck18.angular_diameter_distance(redshifts).to_value(u.Mpc)
    return float(redshifts[np.argmax(distances)])


# ===== Assemble =====

def entry(value, unit, description, source):
    return {"value": float(value), "unit": unit, "description": description, "source": source}


def build_reference_values():
    sun_rs = schwarzschild_radius(const.GM_sun)
    earth_rs = schwarzschild_radius(const.GM_earth)
    sun_surface_z = redshift_to_infinity(const.R_sun, sun_rs)
    neutron_star_rs = schwarzschild_radius(const.G * NEUTRON_STAR_MASS)
    gps_gravitational, gps_velocity = gps_clock_rates_microseconds_per_day()
    astropy_constants = "Astropy constants (CODATA 2018, IAU 2015 nominal values)"
    planck = "Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209)"

    values = {
        # --- Schwarzschild radii and redshift ---
        "sun.schwarzschild_radius_m": entry(sun_rs.to_value(u.m), "m", "Schwarzschild radius of the Sun, 2GM/c^2", astropy_constants),
        "earth.schwarzschild_radius_m": entry(earth_rs.to_value(u.m), "m", "Schwarzschild radius of the Earth", astropy_constants),
        "sun.surface_redshift": entry(sun_surface_z, "", "Gravitational redshift z from the solar surface to infinity", astropy_constants),
        "sun.surface_redshift_velocity_equivalent_m_s": entry(sun_surface_z * SPEED_OF_LIGHT.to_value(u.m / u.s), "m/s", "c*z for the solar surface redshift (about 636 m/s)", astropy_constants),
        "sun.embedding_slope_at_surface": entry(math.sqrt((sun_rs / (const.R_sun - sun_rs)).to_value(u.one)), "", "Slope dw/dr of Flamm's paraboloid at the solar surface", astropy_constants),
        "neutron_star_example.surface_redshift": entry(redshift_to_infinity(NEUTRON_STAR_RADIUS, neutron_star_rs), "", "Surface redshift of a 1.4 solar-mass, 12 km neutron star (model)", astropy_constants),
        "schwarzschild.redshift_at_3rs": entry(1 / math.sqrt(1 - 1 / 3) - 1, "", "z from r = 3 r_s (ISCO) to infinity", "Exact from the formula"),
        # --- Proper distance (numerical, independent of the closed form) ---
        "schwarzschild.proper_distance_rs_to_3rs_in_rs": entry(proper_radial_distance_numeric(1.0, 3.0), "r_s", "Proper radial distance from r_s to 3 r_s", "Numerical integration (trapezoid, 200001 points)"),
        "schwarzschild.proper_distance_2rs_to_10rs_in_rs": entry(proper_radial_distance_numeric(2.0, 10.0), "r_s", "Proper radial distance from 2 r_s to 10 r_s", "Numerical integration (trapezoid, 200001 points)"),
        "schwarzschild.coordinate_light_time_2rs_to_10rs_in_rs": entry(coordinate_light_time_numeric(2.0, 10.0), "r_s/c", "Coordinate time (observer at infinity) for radial light from 2 r_s to 10 r_s, times c", "Numerical integration (SciPy quad)"),
        "schwarzschild.flamm_height_2rs_to_10rs_in_rs": entry(flamm_height_numeric(2.0, 10.0), "r_s", "Rise of Flamm's paraboloid from 2 r_s to 10 r_s (embedding condition integrated)", "Numerical integration (SciPy quad)"),
        "schwarzschild.radar_distance_from_2rs_to_10rs_in_rs": entry(math.sqrt(1 - 1 / 2) * coordinate_light_time_numeric(2.0, 10.0), "r_s", "Radar distance from a static observer at 2 r_s to 10 r_s (half the round-trip time on the observer's clock, times c)", "Numerical integration (SciPy quad)"),
        "schwarzschild.overhead_angle_ratio_at_2rs": entry(overhead_angle_ratio_numeric(2.0), "", "Angular size of a distant object overhead, seen by a static observer at 2 r_s, relative to no mass", "Numerical ray tracing (SciPy quad + brentq)"),
        "schwarzschild.shadow_radius_in_rs": entry(shadow_radius_numeric(), "r_s", "Apparent radius of a black hole's shadow seen from far away (critical impact parameter)", "Numerical minimisation (SciPy)"),
        "neutron_star_example.apparent_radius_km": entry((NEUTRON_STAR_RADIUS / math.sqrt(1 - (neutron_star_rs / NEUTRON_STAR_RADIUS).to_value(u.one))).to_value(u.km), "km", "Apparent radius of a 1.4 solar-mass, 12 km neutron star seen from far away (largest impact parameter of light leaving its surface)", astropy_constants),
        # --- Classic weak-field tests ---
        "sun.limb_light_deflection_arcsec": entry(light_deflection_arcsec(const.GM_sun, const.R_sun), "arcsec", "Light deflection grazing the solar limb (observed: 1.75 arcsec class)", astropy_constants),
        "mercury.perihelion_advance_arcsec_per_century": entry(perihelion_advance_arcsec_per_century(const.GM_sun, MERCURY_SEMI_MAJOR_AXIS, MERCURY_ECCENTRICITY), "arcsec/century", "GR perihelion advance of Mercury (Will 2014 quotes 42.98)", astropy_constants + "; JPL orbital elements"),
        "gps.gravitational_rate_us_per_day": entry(gps_gravitational, "us/day", "GPS clock gain from weaker gravity (simplified model)", astropy_constants + "; Ashby 2003 orbit"),
        "gps.velocity_rate_us_per_day": entry(gps_velocity, "us/day", "GPS clock loss from orbital speed (simplified model)", astropy_constants + "; Ashby 2003 orbit"),
        "gps.net_rate_us_per_day": entry(gps_gravitational + gps_velocity, "us/day", "Net GPS clock gain per day (simplified; published figure is about 38 us/day)", astropy_constants + "; Ashby 2003 orbit"),
        "pound_rebka.fractional_shift": entry((STANDARD_GRAVITY * POUND_REBKA_HEIGHT / SPEED_OF_LIGHT**2).to_value(u.one), "", "Predicted fractional frequency shift g h / c^2 over 22.5 m", "Pound & Rebka 1960 geometry"),
        # --- Cosmology ---
        "cosmology.hubble_constant_km_s_mpc": entry(Planck18.H0.to_value(u.km / u.s / u.Mpc), "km/s/Mpc", "Hubble constant H0", planck),
        "cosmology.age_now_gyr": entry(Planck18.age(0).to_value(u.Gyr), "Gyr", "Age of the universe today", planck),
        "cosmology.recombination_redshift": entry(RECOMBINATION_REDSHIFT, "", "Redshift of last scattering z* (verify against Planck 2018 VI Table 2)", "Planck 2018 VI, arXiv:1807.06209"),
        "cosmology.age_at_recombination_kyr": entry(Planck18.age(RECOMBINATION_REDSHIFT).to_value(u.kyr), "kyr", "Age of the universe at z*", planck),
        "cosmology.comoving_distance_to_recombination_gly": entry(comoving_distance_gly(RECOMBINATION_REDSHIFT), "Gly", "Comoving distance to the last-scattering surface", planck),
        "cosmology.particle_horizon_comoving_gly": entry(particle_horizon_comoving_gly(), "Gly", "Comoving radius of the observable universe (integrated to z = 1e10)", planck),
        "cosmology.hubble_distance_gly": entry((SPEED_OF_LIGHT / Planck18.H0).to_value(u.lyr) / 1e9, "Gly", "Hubble distance c/H0", planck),
        "cosmology.redshift_of_max_emission_distance": entry(redshift_of_max_angular_diameter_distance(), "", "z where proper distance at emission (D_A) is largest", planck),
    }
    # --- Low-redshift values for galaxy-survey maps (CfA2 reaches z ~ 0.05) ---
    values["cosmology.matter_density_om0"] = entry(Planck18.Om0, "", "Matter density parameter Omega_m today", planck)
    values["cosmology.dark_energy_density_ode0"] = entry(Planck18.Ode0, "", "Dark-energy density parameter Omega_Lambda today", planck)
    values["units.million_light_years_per_megaparsec"] = entry((1 * u.Mpc).to_value(u.lyr) / 1e6, "Mly/Mpc", "Megaparsec in millions of light-years (IAU parsec, Julian-year light-year)", "Astropy units")
    for redshift in (0.01, 0.023, 0.05):
        label = str(redshift).replace(".", "p")
        values[f"cosmology.comoving_distance_z{label}_mpc"] = entry(Planck18.comoving_distance(redshift).to_value(u.Mpc), "Mpc", f"Comoving distance to z = {redshift}", planck)
        values[f"cosmology.lookback_time_z{label}_myr"] = entry(Planck18.lookback_time(redshift).to_value(u.Myr), "Myr", f"Lookback time to z = {redshift}", planck)
    for redshift in (0.5, 2, 10):
        label = str(redshift).replace(".", "p")
        values[f"cosmology.comoving_distance_z{label}_gly"] = entry(comoving_distance_gly(redshift), "Gly", f"Comoving distance to z = {redshift}", planck)
        values[f"cosmology.lookback_time_z{label}_gyr"] = entry(Planck18.lookback_time(redshift).to_value(u.Gyr), "Gyr", f"Lookback time to z = {redshift}", planck)
    return values


def write_outputs(values):
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    metadata = {
        "generated": datetime.date.today().isoformat(),
        "astropy_version": astropy.__version__,
        "numpy_version": np.__version__,
        "generator": ".claude/skills/spacetime-physics/scripts/reference_values.py",
    }
    json_path = OUTPUT_FOLDER / "reference-values.json"
    json_path.write_text(json.dumps({"_meta": metadata, "values": values}, indent=2) + "\n")

    lines = [
        "# Reference values",
        "",
        f"Generated {metadata['generated']} by `{metadata['generator']}` "
        f"(Astropy {metadata['astropy_version']}). Do not edit by hand.",
        "",
        "| Key | Value | Unit | Description | Source |",
        "|---|---|---|---|---|",
    ]
    for key, item in values.items():
        lines.append(f"| `{key}` | {item['value']:.8g} | {item['unit']} | {item['description']} | {item['source']} |")
    markdown_path = OUTPUT_FOLDER / "reference-values.md"
    markdown_path.write_text("\n".join(lines) + "\n")
    return json_path, markdown_path


if __name__ == "__main__":
    reference_values = build_reference_values()
    for written_path in write_outputs(reference_values):
        print(f"wrote {written_path}")
    for key, item in reference_values.items():
        print(f"{key:55s} {item['value']:.8g} {item['unit']}")
