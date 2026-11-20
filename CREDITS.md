# Credits

This project stands on other people's data, science and software. Thank you to all of them.
The project's own code is MIT licensed (see `LICENSE`); everything listed here keeps its own license and terms.

## Data

- **CfA Redshift Survey / CfA Redshift Catalog (ZCAT)**, John P. Huchra and collaborators,
  **Smithsonian Astrophysical Observatory** / Harvard-Smithsonian Center for Astrophysics.
  https://lweb.cfa.harvard.edu/~dfabricant/huchra/zcat/
  Used in `galaxy-map.html` (via `data/cfa2-galaxies.js`, built from the CfA2 catalog file `cfa2.dat`).
  The ZCAT pages ask users to credit the Smithsonian Astrophysical Observatory and the appropriate authors.
  - Huchra, Davis, Latham & Tonry (1983), "A survey of galaxy redshifts. IV. The data", ApJS 52, 89. First CfA survey.
  - de Lapparent, Geller & Huchra (1986), "A slice of the universe", ApJ 302, L1. The 1986 slice shown in the map.
  - Geller & Huchra (1989), "Mapping the Universe", Science 246, 897. The Great Wall.

- **6dF Galaxy Survey (6dFGS), Final Release**, D. H. Jones et al. Used in `galaxy-map.html`
  (via `data/6dfgs-galaxies.js`), obtained from **NASA's HEASARC** (table `sixdfgs`, from CDS catalog VII/259):
  https://heasarc.gsfc.nasa.gov/W3Browse/galaxy-catalog/sixdfgs.html
  As the survey requests, these data come from the Final Release of 6dFGS and we cite:
  - Jones, D. H. et al. (2004), "The 6dF Galaxy Survey: samples, observational techniques and the first data release",
    MNRAS 355, 747.
  - Jones, D. H. et al. (2009), "The 6dF Galaxy Survey: final redshift release (DR3) and southern large-scale structures",
    MNRAS 399, 683.
  - The **High Energy Astrophysics Science Archive Research Center (HEASARC)**, NASA Goddard Space Flight Center,
    hosts the copy we used. The table is derived from CDS (Strasbourg) catalog VII/259.

- **2MASS Redshift Survey (2MRS)**, J. P. Huchra, L. M. Macri et al. (2012), "The 2MASS Redshift Survey—Description and
  Data Release", ApJS 199, 26. Used in `galaxy-map.html` (via `data/2mrs-galaxies.js`). We use the catalog **as
  published with the paper** and distributed by **CDS VizieR** (J/ApJS/199/26, doi:10.26093/cds/vizier.21990026),
  retrieved from the VizieR mirror at IDIA (vizier.idia.ac.za). 2MRS home page: http://tdc-www.harvard.edu/2mrs/
  - As the 2MRS team asks, redshifts measured by 2MRS are cited as Huchra et al. (2012), and every other redshift
    is cited by its own bibliographic code. All 411 source papers behind the redshifts we show are listed in
    [`data/2mrs-redshift-sources.md`](data/2mrs-redshift-sources.md).
  - 2MRS is built on the **Two Micron All Sky Survey (2MASS)**, a joint project of the University of Massachusetts
    and the Infrared Processing and Analysis Center/California Institute of Technology, funded by NASA and the NSF.
  - VizieR acknowledgement: this research has made use of the VizieR catalogue access tool, CDS, Strasbourg, France
    (doi:10.26093/cds/vizier). The original description of the VizieR service was published in
    Ochsenbein, Bauer & Marcout (2000), A&AS 143, 23.

## Science (equations and parameter values)

- **Planck Collaboration** (2020), "Planck 2018 results. VI. Cosmological parameters", A&A 641, A6,
  arXiv:1807.06209. Cosmological parameters (H₀, Ωₘ, Ω_Λ, recombination redshift), used via Astropy's `Planck18`.
- **D. W. Hogg** (1999), "Distance measures in cosmology", arXiv:astro-ph/9905116. Comoving distance and lookback time.
- **A. G. Riess et al.** (2022), "A Comprehensive Measurement of the Local Value of the Hubble Constant…" (SH0ES),
  ApJL 934, L7. The H₀ = 73.04 preset.
- **C. M. Will** (2014), "The Confrontation between General Relativity and Experiment", Living Rev. Relativ. 17, 4.
  Benchmarks for light deflection and Mercury's perihelion.
- **N. Ashby** (2003), "Relativity in the Global Positioning System", Living Rev. Relativ. 6, 1. GPS orbit and clock rates.
- **R. V. Pound & G. A. Rebka** (1960), Phys. Rev. Lett. 4, 337. Gravitational redshift on Earth.
- **E. M. Standish**, "Keplerian Elements for Approximate Positions of the Major Planets", JPL Solar System Dynamics.
  Mercury's orbit.
- Textbooks used for the Schwarzschild and FLRW equations: S. Carroll, *Spacetime and Geometry* (2004);
  J. Hartle, *Gravity* (2003); C. Misner, K. Thorne & J. Wheeler, *Gravitation* (1973).
- **L. Flamm** (1916), "Beiträge zur Einsteinschen Gravitationstheorie", Physikalische Zeitschrift 17, 448;
  English translation in Gen. Relativ. Gravit. (2015), doi:10.1007/s10714-015-1908-2. Flamm's paraboloid in
  `gravitational-redshift.html`, and the one-star check of the true-length surface in `two-body-problem.html`. (The 1916 original isn't indexed online; the translation's DOI was verified.)
- **H. A. Buchdahl** (1959), "General Relativistic Fluid Spheres", Phys. Rev. 116, 1027, doi:10.1103/PhysRev.116.1027.
  The R > 9/8 r_s limit where `gravitational-redshift.html` switches from a star to a black hole.
- **H. Weyl** (1917), "Zur Gravitationstheorie", Ann. Phys. 54, 117, doi:10.1002/andp.19173591804
  (English translation in Gen. Relativ. Gravit. 44, 779 (2012)). Static axisymmetric (Weyl) metrics, `two-body-problem.html`.
- **R. Bach & H. Weyl** (1922), "Neue Lösungen der Einsteinschen Gravitationsgleichungen", Math. Z. 13
  (EuDML 167694), with Weyl's addendum "Das statische Zweikörperproblem". The first static two-body solution.
  (Page ranges differ between catalogues; no DOI was found.)
- **W. Israel & K. A. Khan** (1964), "Collinear particles and Bondi dipoles in general relativity", Nuovo Cimento 33, 331,
  doi:10.1007/BF02750196. The double Schwarzschild solution used in `two-body-problem.html`.
- **P. S. Letelier & S. R. Oliveira** (1998), "Superposition of Weyl solutions: the equilibrium forces",
  Class. Quantum Grav. 15, 421, arXiv:gr-qc/9710122. The strut and its force.
- **J. B. Griffiths & J. Podolský** (2009), *Exact Space-Times in Einstein's General Relativity*, Cambridge University Press,
  ch. 10 (static axially symmetric space-times).
- **J. Nocedal & S. J. Wright** (2006), *Numerical Optimization*, 2nd ed., Springer, ch. 7. The L-BFGS method that
  relaxes the true-length surface in `two-body-problem.html`.
- **C. Wyman, P.-P. Sloan & P. Shirley** (2013), "Simple Analytic Approximations to the CIE XYZ Color Matching
  Functions", Journal of Computer Graphics Techniques 2(2), https://jcgt.org/published/0002/02/01/.
  Turns wavelengths into on-screen colours in `gravitational-redshift.html` and `two-body-problem.html`.
- Physical constants: CODATA 2018 and IAU 2015 nominal values, via Astropy.

## Software used in the pages

- **three.js** r160 (MIT), https://threejs.org. 3D rendering, OrbitControls, CSS2DRenderer, and the fat-line
  add-ons (Line2, LineSegments2, LineMaterial).
- **KaTeX** 0.16.11 (MIT), https://katex.org. Equation typesetting.
- Both are loaded from the **jsDelivr** CDN.

## Software used to compute and check values (not shipped in the pages)

- **Astropy** 7.2 (BSD-3-Clause), https://www.astropy.org. Coordinate conversion (B1950 → ICRS), constants,
  units and cosmology. Astropy asks to be cited as:
  Astropy Collaboration (2013), A&A 558, A33; (2018), AJ 156, 123; (2022), ApJ 935, 167.
- **NumPy** (BSD-3-Clause): Harris et al. (2020), Nature 585, 357.
- **SciPy** (BSD-3-Clause): Virtanen et al. (2020), Nature Methods 17, 261.
- **uv** by Astral (MIT/Apache-2.0). Runs the Python scripts with pinned dependencies.
- **Node.js**. Runs the physics self-test checker.

## Agent skills

- **Kalaris Labs, research-agent-skills** (MIT), https://github.com/KalarisLabs/research-agent-skills.
  The `astropy`, `uncertainty-and-units` and `citation-verification` skills in `.claude/skills/`
  (copied unchanged; see `.claude/skills/VENDORED.md`).

## Built with

- Code written with **Claude Code** (Anthropic), working with Dan Sternof Beyer.

## Reference material kept locally (not published)

- `docs/Spacetime_warp_3D_grid.png`: reference image of a warped 3D grid. Its source is unknown, so it's left
  out of git until its origin and license are known.
- Inspiration links in `Goals and Links/` (Sketchfab "gravity warping space-time" model, the abyssal-garden
  project, 3Blue1Brown's manim). Nothing from them is used in the code.
