# Reference values

Generated 2026-11-16 by `.claude/skills/spacetime-physics/scripts/reference_values.py` (Astropy 7.2.0). Do not edit by hand.

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
