# Reference values

Generated 2026-11-20 by `.claude/skills/spacetime-physics/scripts/reference_values.py` (Astropy 7.2.0). Do not edit by hand.

| Key | Value | Unit | Description | Source |
|---|---|---|---|---|
| `sun.schwarzschild_radius_m` | 2953.2501 | m | Schwarzschild radius of the Sun, 2GM/c^2 | Astropy constants (CODATA 2018, IAU 2015 nominal values) |
| `earth.schwarzschild_radius_m` | 0.0088700551 | m | Schwarzschild radius of the Earth | Astropy constants (CODATA 2018, IAU 2015 nominal values) |
| `sun.surface_redshift` | 2.1225093e-06 |  | Gravitational redshift z from the solar surface to infinity | Astropy constants (CODATA 2018, IAU 2015 nominal values) |
| `sun.surface_redshift_velocity_equivalent_m_s` | 636.31229 | m/s | c*z for the solar surface redshift (about 636 m/s) | Astropy constants (CODATA 2018, IAU 2015 nominal values) |
| `sun.embedding_slope_at_surface` | 0.0020603454 |  | Slope dw/dr of Flamm's paraboloid at the solar surface | Astropy constants (CODATA 2018, IAU 2015 nominal values) |
| `neutron_star_example.surface_redshift` | 0.23517598 |  | Surface redshift of a 1.4 solar-mass, 12 km neutron star (model) | Astropy constants (CODATA 2018, IAU 2015 nominal values) |
| `schwarzschild.redshift_at_3rs` | 0.22474487 |  | z from r = 3 r_s (ISCO) to infinity | Exact from the formula |
| `schwarzschild.proper_distance_rs_to_3rs_in_rs` | 3.5957056 | r_s | Proper radial distance from r_s to 3 r_s | Numerical integration (trapezoid, 200001 points) |
| `schwarzschild.proper_distance_2rs_to_10rs_in_rs` | 9.0096923 | r_s | Proper radial distance from 2 r_s to 10 r_s | Numerical integration (trapezoid, 200001 points) |
| `schwarzschild.coordinate_light_time_2rs_to_10rs_in_rs` | 10.197225 | r_s/c | Coordinate time (observer at infinity) for radial light from 2 r_s to 10 r_s, times c | Numerical integration (SciPy quad) |
| `schwarzschild.flamm_height_2rs_to_10rs_in_rs` | 4 | r_s | Rise of Flamm's paraboloid from 2 r_s to 10 r_s (embedding condition integrated) | Numerical integration (SciPy quad) |
| `schwarzschild.radar_distance_from_2rs_to_10rs_in_rs` | 7.2105266 | r_s | Radar distance from a static observer at 2 r_s to 10 r_s (half the round-trip time on the observer's clock, times c) | Numerical integration (SciPy quad) |
| `schwarzschild.overhead_angle_ratio_at_2rs` | 0.70710678 |  | Angular size of a distant object overhead, seen by a static observer at 2 r_s, relative to no mass | Numerical ray tracing (SciPy quad + brentq) |
| `schwarzschild.shadow_radius_in_rs` | 2.5980762 | r_s | Apparent radius of a black hole's shadow seen from far away (critical impact parameter) | Numerical minimisation (SciPy) |
| `neutron_star_example.apparent_radius_km` | 14.822112 | km | Apparent radius of a 1.4 solar-mass, 12 km neutron star seen from far away (largest impact parameter of light leaving its surface) | Astropy constants (CODATA 2018, IAU 2015 nominal values) |
| `sun.limb_light_deflection_arcsec` | 1.7511903 | arcsec | Light deflection grazing the solar limb (observed: 1.75 arcsec class) | Astropy constants (CODATA 2018, IAU 2015 nominal values) |
| `mercury.perihelion_advance_arcsec_per_century` | 42.980475 | arcsec/century | GR perihelion advance of Mercury (Will 2014 quotes 42.98) | Astropy constants (CODATA 2018, IAU 2015 nominal values); JPL orbital elements |
| `gps.gravitational_rate_us_per_day` | 45.652206 | us/day | GPS clock gain from weaker gravity (simplified model) | Astropy constants (CODATA 2018, IAU 2015 nominal values); Ashby 2003 orbit |
| `gps.velocity_rate_us_per_day` | -7.2131238 | us/day | GPS clock loss from orbital speed (simplified model) | Astropy constants (CODATA 2018, IAU 2015 nominal values); Ashby 2003 orbit |
| `gps.net_rate_us_per_day` | 38.439082 | us/day | Net GPS clock gain per day (simplified; published figure is about 38 us/day) | Astropy constants (CODATA 2018, IAU 2015 nominal values); Ashby 2003 orbit |
| `pound_rebka.fractional_shift` | 2.4550582e-15 |  | Predicted fractional frequency shift g h / c^2 over 22.5 m | Pound & Rebka 1960 geometry |
| `cosmology.hubble_constant_km_s_mpc` | 67.66 | km/s/Mpc | Hubble constant H0 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.age_now_gyr` | 13.786885 | Gyr | Age of the universe today | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.recombination_redshift` | 1089.92 |  | Redshift of last scattering z* (verify against Planck 2018 VI Table 2) | Planck 2018 VI, arXiv:1807.06209 |
| `cosmology.age_at_recombination_kyr` | 372.24649 | kyr | Age of the universe at z* | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.comoving_distance_to_recombination_gly` | 45.284873 | Gly | Comoving distance to the last-scattering surface | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.particle_horizon_comoving_gly` | 46.200596 | Gly | Comoving radius of the observable universe (integrated to z = 1e10) | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.hubble_distance_gly` | 14.451555 | Gly | Hubble distance c/H0 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.redshift_of_max_emission_distance` | 1.5921 |  | z where proper distance at emission (D_A) is largest | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.matter_density_om0` | 0.30966 |  | Matter density parameter Omega_m today | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.dark_energy_density_ode0` | 0.68884631 |  | Dark-energy density parameter Omega_Lambda today | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `units.million_light_years_per_megaparsec` | 3.2615638 | Mly/Mpc | Megaparsec in millions of light-years (IAU parsec, Julian-year light-year) | Astropy units |
| `cosmology.comoving_distance_z0p01_mpc` | 44.205056 | Mpc | Comoving distance to z = 0.01 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.lookback_time_z0p01_myr` | 143.46205 | Myr | Lookback time to z = 0.01 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.comoving_distance_z0p023_mpc` | 101.36046 | Mpc | Comoving distance to z = 0.023 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.lookback_time_z0p023_myr` | 326.85582 | Myr | Lookback time to z = 0.023 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.comoving_distance_z0p05_mpc` | 218.93393 | Mpc | Comoving distance to z = 0.05 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.lookback_time_z0p05_myr` | 696.85673 | Myr | Lookback time to z = 0.05 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.comoving_distance_z0p5_gly` | 6.348362 | Gly | Comoving distance to z = 0.5 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.lookback_time_z0p5_gyr` | 5.1962395 | Gyr | Lookback time to z = 0.5 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.comoving_distance_z2_gly` | 17.312997 | Gly | Comoving distance to z = 2 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.lookback_time_z2_gyr` | 10.510055 | Gyr | Lookback time to z = 2 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.comoving_distance_z10_gly` | 31.429358 | Gly | Comoving distance to z = 10 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `cosmology.lookback_time_z10_gyr` | 13.315471 | Gyr | Lookback time to z = 10 | Astropy Planck18 (Planck 2018 VI, arXiv:1807.06209) |
| `two_body.example_redshift_surface1_to_surface2` | 0.10232311 |  | Redshift from star 1's facing surface point to star 2's (negative = blueshift); 1.75 + 1.2 M_sun, R = 12 km, Weyl centre separation 100 km | Numerical rod potentials and gamma field equations (SciPy quad) in reference_values.py |
| `two_body.example_redshift_surface1_to_infinity` | 0.35150962 |  | Redshift from star 1's facing surface point to infinity; 1.75 + 1.2 M_sun, R = 12 km, Weyl centre separation 100 km | Numerical rod potentials and gamma field equations (SciPy quad) in reference_values.py |
| `two_body.example_strut_gamma` | -0.0018333544 |  | gamma on the axis between the bodies (the strut); 1.75 + 1.2 M_sun, R = 12 km, Weyl centre separation 100 km | Numerical rod potentials and gamma field equations (SciPy quad) in reference_values.py |
| `two_body.example_strut_force_newtons` | 5.5521565e+40 | N | Strut force (1/4)(exp(-gamma) - 1) c^4/G; 1.75 + 1.2 M_sun, R = 12 km, Weyl centre separation 100 km | Numerical rod potentials and gamma field equations (SciPy quad) in reference_values.py; Astropy constants |
| `two_body.newton_force_at_1e6km_newtons` | 5.5416212e+32 | N | Newtonian force G M1 M2 / d^2 for the default pair at d = 10^6 km | Astropy constants (CODATA 2018, IAU 2015 nominal values) |
| `two_body.example_ruler_gap_km` | 90.624481 | km | Ruler distance along the axis between the facing surfaces; 1.75 + 1.2 M_sun, R = 12 km, Weyl centre separation 100 km | Numerical rod potentials and gamma field equations (SciPy quad) in reference_values.py |
| `two_body.example_light_time_gap_us` | 342.23798 | us | Light time along the axis between the facing surfaces, distant observer's clock; 1.75 + 1.2 M_sun, R = 12 km, Weyl centre separation 100 km | Numerical rod potentials and gamma field equations (SciPy quad) in reference_values.py |
| `two_body.example_reddest_point_offset_km` | 54.710931 | km | Weyl z of the reddest (highest-potential) point between the bodies, from star 1's centre; 1.75 + 1.2 M_sun, R = 12 km, Weyl centre separation 100 km | Numerical rod potentials and gamma field equations (SciPy quad) in reference_values.py + minimize_scalar |
| `two_body.example_reddest_point_redshift_to_infinity` | 0.090255696 |  | Redshift to infinity from that point; 1.75 + 1.2 M_sun, R = 12 km, Weyl centre separation 100 km | Numerical rod potentials and gamma field equations (SciPy quad) in reference_values.py + minimize_scalar |
| `two_body.example_clock_rate_off_axis` | 0.91465608 |  | Static clock rate dtau/dt at rho = 15.0 km, z = 40.0 km from star 1's centre; 1.75 + 1.2 M_sun, R = 12 km, Weyl centre separation 100 km | Numerical rod potentials and gamma field equations (SciPy quad) in reference_values.py |
| `two_body.example_gamma_off_axis` | -0.0019218899 |  | gamma at rho = 15.0 km, z = 40.0 km from star 1's centre; 1.75 + 1.2 M_sun, R = 12 km, Weyl centre separation 100 km | Numerical rod potentials and gamma field equations (SciPy quad) in reference_values.py |
| `schwarzschild.spatial_geodesic_end_radius_in_rs` | 9.1240092 | r_s | End radius of a spatial geodesic from r = 5.0 r_s on the axis, 60.0 deg from outward, 6.0 r_s long | SciPy solve_ivp in Schwarzschild coordinates |
| `schwarzschild.spatial_geodesic_end_angle_rad` | 0.60286262 | rad | End polar angle of a spatial geodesic from r = 5.0 r_s on the axis, 60.0 deg from outward, 6.0 r_s long | SciPy solve_ivp in Schwarzschild coordinates |
| `two_body.example_geodesic_end_z_from_star1_km` | 70.866851 | km | Weyl z (from star 1's centre) at the end of a spatial geodesic from the reddest point, 70.0 deg from +z, 50.0 km long; 1.75 + 1.2 M_sun, Weyl centre separation 100 km | SciPy solve_ivp with numerical rod potentials, gamma carried by its field equations |
| `two_body.example_geodesic_end_rho_km` | 43.393925 | km | Weyl rho at the end of a spatial geodesic from the reddest point, 70.0 deg from +z, 50.0 km long; 1.75 + 1.2 M_sun, Weyl centre separation 100 km | SciPy solve_ivp with numerical rod potentials, gamma carried by its field equations |
| `two_body.surface_probe_seen_from_above_x_km` | -63.895234 | km | True-length surface seen from above: X of the probe point; 1.75 + 1.2 M_sun, Weyl centre separation 100 km; mesh {'near_star_km': 4.0, 'far': 0.12, 'growth': 0.6}, outer edge 1000 km; probe at Weyl rho = 30.0 km, z = -60.0 km | Independent Python rebuild of the page's true-length surface, solved with SciPy's sparse direct solver |
| `two_body.surface_probe_seen_from_above_y_km` | 33.98549 | km | True-length surface seen from above: Y (distance from the line) of the probe point; 1.75 + 1.2 M_sun, Weyl centre separation 100 km; mesh {'near_star_km': 4.0, 'far': 0.12, 'growth': 0.6}, outer edge 1000 km; probe at Weyl rho = 30.0 km, z = -60.0 km | Independent Python rebuild of the page's true-length surface, solved with SciPy's sparse direct solver |
