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


# ===== Two static bodies: Weyl / Israel–Khan double Schwarzschild =====
#
# Independent of the page's closed forms: each Weyl potential U is the Newtonian potential of a
# uniform rod (linear density 1/2 in G = c = 1 units), integrated numerically; the second metric
# function gamma is found by integrating its field equations along a path from the outer axis
# (where gamma = 0); axis integrals use SciPy quad. Lengths in km, m = GM/c^2.
# Sources: Weyl (1917); Bach & Weyl (1922); Israel & Khan (1964); Letelier & Oliveira (1998).

TWO_BODY_STAR_RADIUS_KM = 12.0
TWO_BODY_MASSES_SOLAR = (1.75, 1.2)      # the page's default pair (a model, not a measured binary)
TWO_BODY_CENTRE_SEPARATION_KM = 100.0    # Weyl coordinate distance between the rod centres
TWO_BODY_OFF_AXIS_POINT_KM = (15.0, 40.0)  # (rho, z) with z measured from star 1's centre


def geometric_mass_km(mass_in_solar_masses):
    """m = GM/c^2 in km."""
    return (const.G * mass_in_solar_masses * const.M_sun / SPEED_OF_LIGHT**2).to_value(u.km)


def two_body_rods():
    """[(centre, m), ...]: star 1 at z = 0, star 2 at z = d."""
    mass1, mass2 = (geometric_mass_km(mass) for mass in TWO_BODY_MASSES_SOLAR)
    return [(0.0, mass1), (TWO_BODY_CENTRE_SEPARATION_KM, mass2)]


def rod_potential_numeric(rho, z, centre, half_length):
    """U = -(1/2) * integral over the rod of dz' / distance, by quadrature."""
    from scipy.integrate import quad

    integrand = lambda z_prime: 1.0 / math.hypot(rho, z - z_prime)
    return -0.5 * quad(integrand, centre - half_length, centre + half_length, epsabs=1e-14, epsrel=1e-13, limit=200)[0]


def weyl_potential_numeric(rho, z, rods):
    return sum(rod_potential_numeric(rho, z, centre, half_length) for centre, half_length in rods)


def weyl_potential_gradient(rho, z, rods, step=1e-5):
    """(dU/drho, dU/dz) by central differences of the numerical potential."""
    d_rho = (weyl_potential_numeric(rho + step, z, rods) - weyl_potential_numeric(rho - step, z, rods)) / (2 * step)
    d_z = (weyl_potential_numeric(rho, z + step, rods) - weyl_potential_numeric(rho, z - step, rods)) / (2 * step)
    return d_rho, d_z


def weyl_gamma_numeric(target_rho, target_z, rods):
    """
    gamma at (rho, z) from its field equations, d gamma/d rho = rho (U_rho^2 - U_z^2) and
    d gamma/d z = 2 rho U_rho U_z, integrated from the axis above both rods (gamma = 0 there:
    elementary flatness, no strings outward) out to large rho, down to the target z, then in to the target rho.
    """
    from scipy.integrate import quad

    centres = [centre for centre, _ in rods]
    span = max(centres) - min(centres) + 2 * sum(half for _, half in rods)
    top_z = max(centres) + 3 * span
    far_rho = 3 * span

    def radial_derivative(rho, z):
        u_rho, u_z = weyl_potential_gradient(rho, z, rods)
        return rho * (u_rho**2 - u_z**2)

    def axial_derivative(rho, z):
        u_rho, u_z = weyl_potential_gradient(rho, z, rods)
        return 2 * rho * u_rho * u_z

    gamma = quad(lambda rho: radial_derivative(rho, top_z), 0.0, far_rho, limit=400)[0]
    gamma += quad(lambda z: axial_derivative(far_rho, z), top_z, target_z, limit=400)[0]
    gamma += quad(lambda rho: radial_derivative(rho, target_z), far_rho, target_rho, limit=400)[0]
    return gamma


def two_body_reference_values():
    """Values for two-body-problem.html (default pair, Weyl centre separation 100 km)."""
    from scipy.integrate import quad
    from scipy.optimize import minimize_scalar

    rods = two_body_rods()
    (centre1, mass1), (centre2, mass2) = rods
    radius = TWO_BODY_STAR_RADIUS_KM
    # Facing surface points on the axis: where the isolated-star radius (R+ + R-)/2 + m equals R.
    surface1 = centre1 + (radius - mass1)
    surface2 = centre2 - (radius - mass2)
    middle = 0.5 * (surface1 + surface2)
    gamma_strut = weyl_gamma_numeric(1e-7, middle, rods)

    axis_potential = lambda z: weyl_potential_numeric(0.0, z, rods)
    ruler_gap = quad(lambda z: math.exp(gamma_strut - axis_potential(z)), surface1, surface2, epsrel=1e-11, limit=200)[0]
    light_length = quad(lambda z: math.exp(gamma_strut - 2 * axis_potential(z)), surface1, surface2, epsrel=1e-11, limit=200)[0]
    light_time_us = light_length / SPEED_OF_LIGHT.to_value(u.km / u.s) * 1e6

    reddest = minimize_scalar(lambda z: -axis_potential(z), bounds=(surface1, surface2), method="bounded",
                              options={"xatol": 1e-9})
    off_rho, off_z = TWO_BODY_OFF_AXIS_POINT_KM

    force_unit = (SPEED_OF_LIGHT**4 / const.G).to_value(u.N)   # c^4/G, the unit of force in G = c = 1
    strut_force = 0.25 * (math.exp(-gamma_strut) - 1) * force_unit
    newton_distance_km = 1e6
    newton_force = (const.G * TWO_BODY_MASSES_SOLAR[0] * const.M_sun * TWO_BODY_MASSES_SOLAR[1] * const.M_sun
                    / (newton_distance_km * u.km) ** 2).to_value(u.N)

    source = "Numerical rod potentials and gamma field equations (SciPy quad) in reference_values.py"
    setup = "1.75 + 1.2 M_sun, R = 12 km, Weyl centre separation 100 km"
    return {
        "two_body.example_redshift_surface1_to_surface2": entry(
            math.expm1(axis_potential(surface2) - axis_potential(surface1)), "",
            f"Redshift from star 1's facing surface point to star 2's (negative = blueshift); {setup}", source),
        "two_body.example_redshift_surface1_to_infinity": entry(
            math.expm1(-axis_potential(surface1)), "", f"Redshift from star 1's facing surface point to infinity; {setup}", source),
        "two_body.example_strut_gamma": entry(gamma_strut, "", f"gamma on the axis between the bodies (the strut); {setup}", source),
        "two_body.example_strut_force_newtons": entry(strut_force, "N",
            f"Strut force (1/4)(exp(-gamma) - 1) c^4/G; {setup}", source + "; Astropy constants"),
        "two_body.newton_force_at_1e6km_newtons": entry(newton_force, "N",
            "Newtonian force G M1 M2 / d^2 for the default pair at d = 10^6 km", astropy_constants_label()),
        "two_body.example_ruler_gap_km": entry(ruler_gap, "km", f"Ruler distance along the axis between the facing surfaces; {setup}", source),
        "two_body.example_light_time_gap_us": entry(light_time_us, "us",
            f"Light time along the axis between the facing surfaces, distant observer's clock; {setup}", source),
        "two_body.example_reddest_point_offset_km": entry(reddest.x - centre1, "km",
            f"Weyl z of the reddest (highest-potential) point between the bodies, from star 1's centre; {setup}", source + " + minimize_scalar"),
        "two_body.example_reddest_point_redshift_to_infinity": entry(math.expm1(-axis_potential(reddest.x)), "",
            f"Redshift to infinity from that point; {setup}", source + " + minimize_scalar"),
        "two_body.example_clock_rate_off_axis": entry(math.exp(weyl_potential_numeric(off_rho, off_z, rods)), "",
            f"Static clock rate dtau/dt at rho = {off_rho} km, z = {off_z} km from star 1's centre; {setup}", source),
        "two_body.example_gamma_off_axis": entry(weyl_gamma_numeric(off_rho, off_z, rods), "",
            f"gamma at rho = {off_rho} km, z = {off_z} km from star 1's centre; {setup}", source),
    }


# ----- Geodesics of space (for the anchored grid in two-body-problem.html) -----

GEODESIC_SINGLE_START_RADIUS_IN_RS = 5.0
GEODESIC_SINGLE_HEADING_DEG = 60.0
GEODESIC_SINGLE_LENGTH_IN_RS = 6.0
GEODESIC_TWO_BODY_HEADING_DEG = 70.0
GEODESIC_TWO_BODY_LENGTH_KM = 50.0


def schwarzschild_spatial_geodesic(start_radius, heading, length):
    """
    A geodesic of the Schwarzschild spatial metric dr^2/(1 - 1/r) + r^2 dtheta^2 (units of r_s), in a plane, by its
    Hamiltonian: dr/ds = (1 - 1/r) p_r, dp_r/ds = -(p_r^2/r^2 - 2 L^2/r^3)/2, dtheta/ds = L/r^2. Starts at theta = 0,
    heading at `heading` from the outward radial direction. Returns (r, theta) after true length `length`.
    """
    from scipy.integrate import solve_ivp

    angular_momentum = start_radius * math.sin(heading)

    def derivative(_, state):
        radius, radial_momentum, _angle = state
        return [(1 - 1 / radius) * radial_momentum,
                -0.5 * (radial_momentum**2 / radius**2 - 2 * angular_momentum**2 / radius**3),
                angular_momentum / radius**2]

    start = [start_radius, math.cos(heading) / math.sqrt(1 - 1 / start_radius), 0.0]
    solution = solve_ivp(derivative, (0, length), start, rtol=1e-12, atol=1e-14, method="DOP853")
    return solution.y[0, -1], solution.y[2, -1]


def weyl_meridian_geodesic_numeric(rods, start_z, heading, length, start_gamma):
    """
    A geodesic of dl^2 = e^(2(gamma - U))(drho^2 + dz^2) from the axis point start_z, with U from numerical rod
    integrals and gamma carried along the path by its field equations (starting from start_gamma). Returns (z, rho).
    """
    from scipy.integrate import solve_ivp

    def derivative(_, state):
        z, rho, direction, gamma = state
        potential = weyl_potential_numeric(rho, z, rods)
        u_rho, u_z = weyl_potential_gradient(rho, z, rods)
        gamma_rho = rho * (u_rho**2 - u_z**2)
        gamma_z = 2 * rho * u_rho * u_z
        scale = math.exp(potential - gamma)
        dz = scale * math.cos(direction)
        drho = scale * math.sin(direction)
        turn = scale * ((gamma_rho - u_rho) * math.cos(direction) - (gamma_z - u_z) * math.sin(direction))
        return [dz, drho, turn, gamma_rho * drho + gamma_z * dz]

    solution = solve_ivp(derivative, (0, length), [start_z, 0.0, heading, start_gamma], rtol=1e-10, atol=1e-12, method="DOP853")
    return solution.y[0, -1], solution.y[1, -1]


def geodesic_reference_values():
    from scipy.optimize import minimize_scalar

    radius, angle = schwarzschild_spatial_geodesic(GEODESIC_SINGLE_START_RADIUS_IN_RS,
                                                   math.radians(GEODESIC_SINGLE_HEADING_DEG), GEODESIC_SINGLE_LENGTH_IN_RS)
    rods = two_body_rods()
    (centre1, mass1), (centre2, mass2) = rods
    surface1 = centre1 + (TWO_BODY_STAR_RADIUS_KM - mass1)
    surface2 = centre2 - (TWO_BODY_STAR_RADIUS_KM - mass2)
    reddest = minimize_scalar(lambda z: -weyl_potential_numeric(0.0, z, rods), bounds=(surface1, surface2),
                              method="bounded", options={"xatol": 1e-9}).x
    gamma_strut = weyl_gamma_numeric(1e-7, reddest, rods)
    end_z, end_rho = weyl_meridian_geodesic_numeric(rods, reddest, math.radians(GEODESIC_TWO_BODY_HEADING_DEG),
                                                    GEODESIC_TWO_BODY_LENGTH_KM, gamma_strut)
    single = (f"from r = {GEODESIC_SINGLE_START_RADIUS_IN_RS} r_s on the axis, {GEODESIC_SINGLE_HEADING_DEG} deg from outward, "
              f"{GEODESIC_SINGLE_LENGTH_IN_RS} r_s long")
    two = (f"from the reddest point, {GEODESIC_TWO_BODY_HEADING_DEG} deg from +z, {GEODESIC_TWO_BODY_LENGTH_KM} km long; "
           "1.75 + 1.2 M_sun, Weyl centre separation 100 km")
    return {
        "schwarzschild.spatial_geodesic_end_radius_in_rs": entry(radius, "r_s", f"End radius of a spatial geodesic {single}",
                                                                 "SciPy solve_ivp in Schwarzschild coordinates"),
        "schwarzschild.spatial_geodesic_end_angle_rad": entry(angle, "rad", f"End polar angle of a spatial geodesic {single}",
                                                              "SciPy solve_ivp in Schwarzschild coordinates"),
        "two_body.example_geodesic_end_z_from_star1_km": entry(end_z - centre1, "km", f"Weyl z (from star 1's centre) at the end of a spatial geodesic {two}",
                                                               "SciPy solve_ivp with numerical rod potentials, gamma carried by its field equations"),
        "two_body.example_geodesic_end_rho_km": entry(end_rho, "km", f"Weyl rho at the end of a spatial geodesic {two}",
                                                      "SciPy solve_ivp with numerical rod potentials, gamma carried by its field equations"),
    }


# ----- True-length surface (two-body-problem.html): an independent re-implementation -----
#
# The page embeds the plane through both stars in flat 3D with true edge lengths, with the line through the stars
# pinned to cos(tilt) = clock rate and a small "least bent" preference. This rebuilds the same mesh and
# conditions in Python (closed-form Weyl functions, written separately from the page), solves them with SciPy's sparse
# direct solver, and reports where one surface point lands seen from above.

SURFACE_TEST_SPACING = {"near_star_km": 4.0, "far": 0.12, "growth": 0.6}   # the page's test mesh
SURFACE_TEST_OUTER_KM = 1000.0
SURFACE_TEST_PROBE = (30.0, -60.0)   # Weyl (rho, z) in km, z from the midpoint of the rod centres
SURFACE_LINK_WEIGHT = 10.0
SURFACE_SMOOTHNESS = 1e-3


def rod_potential_closed(rho, z, centre, half):
    upper = math.hypot(rho, z - centre - half); lower = math.hypot(rho, z - centre + half)
    return 0.5 * math.log1p(-4 * half / (upper + lower + 2 * half))


def weyl_gamma_closed(rho, z, rods):
    def pair_term(k, l):
        dk = math.hypot(rho, z - k); dl = math.hypot(rho, z - l); product = (z - k) * (z - l)
        if product >= 0: return dk * dl + product + rho * rho
        return rho * rho * (rho * rho + (z - k) ** 2 + (z - l) ** 2) / (dk * dl - product) + rho * rho
    if rho < 1e-9:
        (c1, m1), (c2, m2) = sorted(rods)
        if c1 + m1 < z < c2 - m2:
            d = c2 - c1
            return math.log1p(-4 * m1 * m2 / (d * d - (m1 - m2) ** 2))
        return 0.0
    total = 0.0
    for ci, mi in rods:
        for cj, mj in rods:
            total += 0.25 * math.log(pair_term(ci - mi, cj + mj) * pair_term(ci + mi, cj - mj) / (pair_term(ci - mi, cj - mj) * pair_term(ci + mi, cj + mj)))
    return total


def surface_reference_values():
    import numpy as np
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla
    from scipy.optimize import minimize_scalar

    (c1, m1), (c2, m2) = two_body_rods()
    middle = 0.5 * (c1 + c2); c1, c2 = c1 - middle, c2 - middle   # the page's star pair is centred on 0
    rods = [(c1, m1), (c2, m2)]; radius = TWO_BODY_STAR_RADIUS_KM
    U = lambda rho, z: sum(rod_potential_closed(rho, z, c, h) for c, h in rods)
    metric = lambda rho, z: math.exp(weyl_gamma_closed(rho, z, rods) - U(rho, z))
    own_radius = lambda rho, z, c, h: 0.5 * (math.hypot(rho, z - c - h) + math.hypot(rho, z - c + h)) + h
    focus = (c2 - c1) / 2; mu_max = math.acosh(SURFACE_TEST_OUTER_KM / focus)
    spacing = SURFACE_TEST_SPACING
    star_reach = math.sqrt(2 * (radius + 4) / focus)
    near_step = min(spacing["far"], spacing["near_star_km"] / (focus * math.sinh(star_reach)))
    step_at = lambda u: min(spacing["far"], near_step * max(1.0, 1 + spacing["growth"] * (u - 1.5 * star_reach) / star_reach))
    def graded(start, end):
        values = [start]
        while values[-1] < end - 1e-12: values.append(min(values[-1] + step_at(values[-1]), end))
        if len(values) > 2 and values[-1] - values[-2] < 0.5 * step_at(values[-2]): values.pop(-2)
        return values
    mus = graded(0.0, mu_max); half_nus = graded(0.0, math.pi / 2)
    nus = half_nus + [math.pi - nu for nu in reversed(half_nus[:-1])]
    n_mu, n_nu = len(mus), len(nus)
    count = n_mu * n_nu
    z_of = np.zeros(count); rho_of = np.zeros(count); alive = np.zeros(count, bool); rim = -np.ones(count, int)
    star_at = lambda rho, z: next((i for i, (c, h) in enumerate(rods) if own_radius(rho, z, c, h) < radius), -1)
    for j in range(n_nu):
        for i in range(n_mu):
            n = j * n_mu + i; mu = mus[i]; nu = nus[j]
            z_of[n] = focus * math.cosh(mu) * math.cos(nu)
            rho_of[n] = 0.0 if (i == 0 or j == 0 or j == n_nu - 1) else focus * math.sinh(mu) * math.sin(nu)
            alive[n] = star_at(rho_of[n], z_of[n]) < 0
    grid_z = z_of.copy(); grid_rho = rho_of.copy()
    for j in range(n_nu):
        for i in range(n_mu):
            n = j * n_mu + i
            if not alive[n]: continue
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ii, jj = i + di, j + dj
                if not (0 <= ii < n_mu and 0 <= jj < n_nu): continue
                nn = jj * n_mu + ii
                if alive[nn]: continue
                s = star_at(grid_rho[nn], grid_z[nn]); c, h = rods[s]
                along = radius - h; across = math.sqrt(radius * (radius - 2 * h)); offset = grid_z[n] - c
                scale = 1 / math.hypot(offset / along, grid_rho[n] / across)
                z_of[n] = c + offset * scale; rho_of[n] = grid_rho[n] * scale; rim[n] = s
                break
    edges = set()
    for j in range(n_nu - 1):
        for i in range(n_mu - 1):
            a = j * n_mu + i; b, c, d = a + 1, a + n_mu + 1, a + n_mu
            live = [k for k in (a, b, c, d) if alive[k]]
            if len(live) == 4:
                for p, q in ((a, b), (b, c), (c, d), (d, a), (a, c), (b, d)): edges.add((min(p, q), max(p, q)))
            elif len(live) == 3:
                for p, q in ((live[0], live[1]), (live[1], live[2]), (live[2], live[0])): edges.add((min(p, q), max(p, q)))
    edges = sorted(edges)
    target = []
    for p, q in edges:
        length = math.hypot(z_of[q] - z_of[p], rho_of[q] - rho_of[p])
        target.append(length / 6 * (metric(rho_of[p], z_of[p]) + 4 * metric(0.5 * (rho_of[p] + rho_of[q]), 0.5 * (z_of[p] + z_of[q])) + metric(rho_of[q], z_of[q])))
    target = np.array(target); E = np.array(edges)
    # Line rule along the axis.
    surface1 = c1 + (radius - m1); surface2 = c2 - (radius - m2)
    reddest = minimize_scalar(lambda z: -U(0.0, z), bounds=(surface1, surface2), method="bounded", options={"xatol": 1e-10}).x
    u_reddest = U(0.0, reddest)
    def slopes(z):
        between = surface1 - 1e-9 < z < surface2 + 1e-9
        u = U(0.0, z); true_length = math.exp(weyl_gamma_closed(0.0, z, rods) - u)
        drawn = true_length * math.exp(u - (u_reddest if between else 0.0))
        return drawn, math.sqrt(max(true_length ** 2 - drawn ** 2, 0.0)), between
    def uphill(z):
        if surface1 < z < surface2: return math.copysign(1, reddest - z)
        nearest = c1 if abs(z - c1) < abs(z - c2) else c2
        return math.copysign(1, z - nearest)
    axis = sorted((n for n in range(count) if alive[n] and rho_of[n] == 0), key=lambda n: z_of[n])
    links = []
    for a, b in zip(axis, axis[1:]):
        z1, z2 = z_of[a], z_of[b]
        if any(z1 < c < z2 for c, _ in rods): continue
        pieces = 40; step = (z2 - z1) / pieces; rise = height = 0.0
        for k in range(pieces):
            za = z1 + k * step; s0, s1, s2 = slopes(za), slopes(za + step / 2), slopes(za + step)
            rise += step / 6 * (s0[0] + 4 * s1[0] + s2[0])
            height += step / 6 * (s0[1] + 4 * s1[1] + s2[1]) * uphill(za + step / 2)
        links.append((a, b, rise, height, max(z2 - z1, 1e-9)))
    # Pinned far edge (outermost ring) and starting shape.
    total_mass = m1 + m2; total_centre = (m1 * c1 + m2 * c2) / total_mass
    def flamm_map(c, h, rho, z):
        upper = math.hypot(rho, z - c - h); lower = math.hypot(rho, z - c + h); r = 0.5 * (upper + lower) + h
        cosine = min(max((lower - upper) / (2 * h), -1), 1)
        return np.array([c + r * cosine, r * math.sqrt(1 - cosine * cosine), 2 * math.sqrt(2 * h * max(r - 2 * h, 0))])
    held = min((n for n in range(count) if alive[n] and rho_of[n] == 0), key=lambda n: abs(z_of[n] - reddest))
    pinned = np.zeros(count, bool); pinned[held] = True
    x = np.zeros((count, 3))
    for n in range(count):
        tot = flamm_map(total_centre, total_mass, rho_of[n], z_of[n])
        X, Y, W = z_of[n], rho_of[n], tot[2]
        for c, h in rods:
            own = flamm_map(c, h, rho_of[n], z_of[n]); X += own[0] - z_of[n]; Y += own[1] - rho_of[n]
            W += own[2] - flamm_map(total_centre, h, rho_of[n], z_of[n])[2]
        x[n] = (X, 0.0 if rho_of[n] == 0 else Y, W)
    # Smoothness triples along mesh rows and columns: bend of the middle node from its neighbours' interpolation.
    triples = []
    def add_triple(l, c, r):
        if not (alive[l] and alive[c] and alive[r]): return
        d1 = math.hypot(z_of[c] - z_of[l], rho_of[c] - rho_of[l]); d2 = math.hypot(z_of[r] - z_of[c], rho_of[r] - rho_of[c])
        if d1 + d2 < 1e-9: return
        triples.append((l, c, r, d2 / (d1 + d2), d1 / (d1 + d2), 1 / (0.5 * (d1 + d2))))
    for j in range(n_nu):
        for i in range(1, n_mu - 1): n = j * n_mu + i; add_triple(n - 1, n, n + 1)
    for j in range(1, n_nu - 1):
        for i in range(n_mu): n = j * n_mu + i; add_triple(n - n_mu, n, n + n_mu)
    tl, tc, tr = (np.array([t[k] for t in triples]) for k in range(3))
    twl = np.array([t[3] for t in triples]); twr = np.array([t[4] for t in triples]); tsc = np.array([t[5] for t in triples])
    sb = math.sqrt(SURFACE_SMOOTHNESS)
    index = -np.ones((count, 3), int); unknowns = 0
    for n in range(count):
        if not alive[n] or pinned[n]: continue
        for k in range(3):
            if k == 1 and rho_of[n] == 0: continue
            index[n, k] = unknowns; unknowns += 1
    w = math.sqrt(SURFACE_LINK_WEIGHT)
    la = np.array([l[0] for l in links]); lb = np.array([l[1] for l in links]); lrise = np.array([l[2] for l in links])
    lheight = np.array([l[3] for l in links]); llen = np.array([l[4] for l in links])
    def residuals(x):
        D = x[E[:, 0]] - x[E[:, 1]]; length = np.linalg.norm(D, axis=1)
        B = x[tc] - twl[:, None] * x[tl] - twr[:, None] * x[tr]
        return np.concatenate([length / target - 1, w * (x[lb, 0] - x[la, 0] - lrise) / llen, w * (x[lb, 2] - x[la, 2] - lheight) / llen]
                              + [sb * tsc * B[:, k] for k in range(3)]), D, length
    def jacobian(D, length):
        rows, cols, vals = [], [], []
        g = D / (target * length)[:, None]
        for side, sign in ((0, 1.0), (1, -1.0)):
            for k in range(3):
                col = index[E[:, side], k]; mask = col >= 0
                rows.append(np.nonzero(mask)[0]); cols.append(col[mask]); vals.append(sign * g[mask, k])
        base = len(target)
        for block, k in ((0, 0), (1, 2)):
            for node, sign in ((lb, 1.0), (la, -1.0)):
                col = index[node, k]; mask = col >= 0
                rows.append(base + block * len(links) + np.nonzero(mask)[0]); cols.append(col[mask]); vals.append(sign * w / llen[mask])
        base += 2 * len(links)
        for k in range(3):
            for node, coefficient in ((tc, np.ones(len(triples))), (tl, -twl), (tr, -twr)):
                col = index[node, k]; mask = col >= 0
                rows.append(base + k * len(triples) + np.nonzero(mask)[0]); cols.append(col[mask]); vals.append((sb * tsc * coefficient)[mask])
        return sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(len(target) + 2 * len(links) + 3 * len(triples), unknowns))
    r, D, length = residuals(x); cost = r @ r; damping = 1e-3
    for _ in range(60):
        J = jacobian(D, length); A = (J.T @ J).tocsc(); g = J.T @ r; accepted = False
        for _ in range(12):
            step = spla.spsolve(A + damping * sp.diags(A.diagonal()), -g)
            trial = x.copy(); mask = index >= 0; trial[mask] += step[index[mask]]
            rt, Dt, lt = residuals(trial); ct = rt @ rt
            if ct < cost: x, r, D, length, cost = trial, rt, Dt, lt, ct; damping = max(damping / 3, 1e-12); accepted = True; break
            damping *= 4
        if not accepted: break
    # Where the probe point lands, seen from above (bilinear in its mesh cell, as the page does).
    rho, z = SURFACE_TEST_PROBE
    to_left = math.hypot(z + focus, rho); to_right = math.hypot(z - focus, rho)
    mu = math.acosh(max((to_left + to_right) / (2 * focus), 1)); nu = math.acos(min(max((to_left - to_right) / (2 * focus), -1), 1))
    import bisect
    i = min(max(bisect.bisect_right(mus, mu) - 1, 0), n_mu - 2); j = min(max(bisect.bisect_right(nus, nu) - 1, 0), n_nu - 2)
    ti = (mu - mus[i]) / (mus[i + 1] - mus[i]); tj = (nu - nus[j]) / (nus[j + 1] - nus[j])
    point = sum(weight * x[node] for node, weight in ((j * n_mu + i, (1 - ti) * (1 - tj)), (j * n_mu + i + 1, ti * (1 - tj)),
                                                    ((j + 1) * n_mu + i, (1 - ti) * tj), ((j + 1) * n_mu + i + 1, ti * tj)))
    setup = (f"1.75 + 1.2 M_sun, Weyl centre separation 100 km; mesh {SURFACE_TEST_SPACING}, outer edge {SURFACE_TEST_OUTER_KM:.0f} km; "
             f"probe at Weyl rho = {rho} km, z = {z} km")
    source = "Independent Python rebuild of the page's true-length surface, solved with SciPy's sparse direct solver"
    return {
        "two_body.surface_probe_seen_from_above_x_km": entry(point[0], "km", f"True-length surface seen from above: X of the probe point; {setup}", source),
        "two_body.surface_probe_seen_from_above_y_km": entry(point[1], "km", f"True-length surface seen from above: Y (distance from the line) of the probe point; {setup}", source),
    }


# ----- Milky Way and Andromeda (milky-way-andromeda.html): weak-field values -----
#
# Mass models from Patel, Besla & Sohn 2017 (MNRAS 464, 3825), Table 2: NFW halo (mass M_vir − M_disc − M_bulge,
# truncated at R_vir, scale radius R_vir / c_vir), Miyamoto–Nagai disc, Hernquist bulge. (Their halos are also
# adiabatically contracted; neither the page nor these values include that.) The spherical parts' potentials are found
# here by integrating their densities numerically (Poisson's equation), independently of the page's closed forms.
# Distance 761 kpc: Li et al. 2021 (ApJ 920, 84). Geometry: centres on the x axis, both discs in the plane y = 0.

GALAXY_MODELS = {   # M_vir, c_vir, R_vir [kpc], M_disc, R_disc, z_disc [kpc], M_bulge, R_bulge [kpc]  (masses in M_sun)
    "MWa": (1.0e12, 9.86, 261.0, 6.5e10, 3.5, 0.53, 1.0e10, 0.7),
    "M31a": (1.5e12, 9.56, 299.0, 8.5e10, 5.0, 1.0, 1.9e10, 1.0),
}
GALAXY_SEPARATION_KPC = 761.0
GALAXY_EMITTER_FROM_MW_KPC = 8.29     # A: on the line toward M31, at the Sun's distance from the Galactic centre (McMillan 2011)
GALAXY_RECEIVER_FROM_M31_KPC = 8.0    # B: on the line, 8 kpc short of M31's centre


def galaxy_reference_values():
    from scipy.integrate import quad

    G = const.G.to_value(u.kpc * u.km**2 / u.s**2 / u.M_sun)
    c = SPEED_OF_LIGHT.to_value(u.km / u.s)

    def spherical_parts(model):
        m_vir, conc, r_vir, m_disc, r_disc, z_disc, m_bulge, r_bulge = model
        m_halo = m_vir - m_disc - m_bulge; r_s = r_vir / conc
        mu = lambda x: math.log1p(x) - x / (1 + x)
        rho_s = m_halo / (4 * math.pi * r_s**3 * mu(conc))
        halo_density = lambda r: rho_s / ((r / r_s) * (1 + r / r_s) ** 2) if r < r_vir else 0.0
        bulge_density = lambda r: m_bulge * r_bulge / (2 * math.pi * r * (r + r_bulge) ** 3)
        return [(halo_density, r_vir), (bulge_density, math.inf)]

    def spherical_potential(density, edge, r):
        inner = quad(lambda s: 4 * math.pi * s * s * density(s), 0, min(r, edge), limit=400, epsrel=1e-11)[0]
        outer = quad(lambda s: 4 * math.pi * s * density(s), min(r, edge), edge, limit=400, epsrel=1e-11)[0] if r < edge else 0.0
        return -G * (inner / r + outer)

    def disc_potential(model, radius_in_plane, height):
        _, _, _, m_disc, r_disc, z_disc, _, _ = model
        return -G * m_disc / math.sqrt(radius_in_plane**2 + (r_disc + math.sqrt(height**2 + z_disc**2)) ** 2)

    def galaxy_potential(model, dx, dy, dz):
        r = math.sqrt(dx * dx + dy * dy + dz * dz)
        return sum(spherical_potential(density, edge, r) for density, edge in spherical_parts(model)) + disc_potential(model, math.hypot(dx, dz), dy)

    centres = {"MWa": -GALAXY_SEPARATION_KPC / 2, "M31a": GALAXY_SEPARATION_KPC / 2}
    def total_potential(x):   # on the line (y = z = 0)
        return sum(galaxy_potential(GALAXY_MODELS[name], x - centre, 0.0, 0.0) for name, centre in centres.items())

    x_a = centres["MWa"] + GALAXY_EMITTER_FROM_MW_KPC
    x_b = centres["M31a"] - GALAXY_RECEIVER_FROM_M31_KPC
    phi_a = total_potential(x_a) / c**2; phi_b = total_potential(x_b) / c**2
    redshift = math.expm1(phi_b - phi_a)
    line_integral = quad(lambda x: total_potential(x), x_a, x_b, limit=400, epsrel=1e-10)[0]   # (km/s)^2 kpc
    kpc_km = (1 * u.kpc).to_value(u.km); year_s = (1 * u.yr).to_value(u.s)
    shapiro_years = -2 * line_integral / c**3 * kpc_km / year_s
    extra_ruler_pc = -line_integral / c**2 * 1000.0
    # Milky Way alone: circular speed at 8.29 kpc in the disc plane, and its spherically averaged mass inside 10 kpc.
    mw = GALAXY_MODELS["MWa"]
    step = 1e-4
    dphi = (galaxy_potential(mw, 8.29 + step, 0, 0) - galaxy_potential(mw, 8.29 - step, 0, 0)) / (2 * step)
    circular_speed = math.sqrt(8.29 * dphi)
    def averaged_disc_potential(r):
        return 0.5 * quad(lambda t: disc_potential(mw, r * math.sin(t), r * math.cos(t)) * math.sin(t), 0, math.pi, limit=200, epsrel=1e-11)[0]
    disc_mass_10 = 10.0**2 * (averaged_disc_potential(10 + step) - averaged_disc_potential(10 - step)) / (2 * step) / G
    # Milky Way alone, one-star-page stretch in the areal gauge: extra ruler length from 10 to 300 kpc, ∫ G m(r) / (r c^2) dr.
    def enclosed_mass(r):
        spherical = sum(quad(lambda s: 4 * math.pi * s * s * density(s), 0, min(r, edge), limit=400, epsrel=1e-11)[0] for density, edge in spherical_parts(mw))
        disc = r**2 * (averaged_disc_potential(r + step) - averaged_disc_potential(r - step)) / (2 * step) / G
        return spherical + disc
    excess_pc = quad(lambda r: G * enclosed_mass(r) / (r * c**2), 10.0, 300.0, limit=200, epsrel=1e-9)[0] * 1000.0

    setup = "Patel et al. 2017 models MWa and M31a, separation 761 kpc, discs in the plane of the line"
    source = "Numerical Poisson integrals (SciPy quad) in reference_values.py"
    return {
        "galaxies.potential_at_A_over_c2": entry(phi_a, "", f"Φ/c² at A (8.29 kpc from the Milky Way's centre, on the line); {setup}", source),
        "galaxies.potential_at_B_over_c2": entry(phi_b, "", f"Φ/c² at B (8 kpc from M31's centre, on the line); {setup}", source),
        "galaxies.gravitational_redshift_A_to_B": entry(redshift, "", f"Gravitational redshift of light from A to B (static observers); {setup}", source),
        "galaxies.shapiro_delay_A_to_B_years": entry(shapiro_years, "yr", f"Shapiro delay along the line A to B, −(2/c³)∫Φ dl (isotropic coordinates); {setup}", source),
        "galaxies.extra_ruler_length_A_to_B_pc": entry(extra_ruler_pc, "pc", f"Ruler length minus coordinate length A to B, −∫Φ/c² dl (isotropic coordinates); {setup}", source),
        "galaxies.mw_circular_speed_8p29_km_s": entry(circular_speed, "km/s", "Milky Way (MWa) circular speed at 8.29 kpc in the disc plane", source),
        "galaxies.mw_disc_monopole_mass_10kpc_msun": entry(disc_mass_10, "M_sun", "Spherically averaged (monopole) mass of the MWa disc inside 10 kpc", source),
        "galaxies.mw_extra_ruler_10_to_300kpc_pc": entry(excess_pc, "pc", "Milky Way (MWa) alone: extra ruler length from 10 to 300 kpc, ∫ G m(r)/(r c²) dr (areal gauge, monopole mass)", source),
    }


def astropy_constants_label():
    return "Astropy constants (CODATA 2018, IAU 2015 nominal values)"


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
    # --- Two static bodies (Weyl / Israel–Khan), for two-body-problem.html ---
    values.update(two_body_reference_values())
    values.update(geodesic_reference_values())
    values.update(surface_reference_values())
    values.update(galaxy_reference_values())
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
