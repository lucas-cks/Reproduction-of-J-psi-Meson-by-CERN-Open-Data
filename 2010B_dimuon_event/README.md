# Broad-Spectrum Dimuon Invariant Mass Analysis: From Charmonia to the $Z$ Boson (Run2010B)

## Invariant Mass Spectrum Analysis: Multi-Generation Particle Reconstruction

This repository contains production Python workflows designed to analyze high-energy dimuon ($\mu^+\mu^-$) invariant mass distributions utilizing open particle collision datasets from CERN. By evaluating a wide-range energy domain ($2.0\text{ GeV}$ to $110.0\text{ GeV}$), this project reproduces the spectroscopic signatures of multiple critical milestones in the history of the Standard Model:

* **The Second Matter Generation:** The $J/\psi$ meson ($c\bar{c}$ charmonium state).
* **The Third Matter Generation:** The $\Upsilon$ meson ($\text{b}\bar{\text{b}}$ bottomonium state).
* **The Electroweak Force Carrier:** The $Z$ Gauge Boson (mediator of the weak neutral current).

## Physics Context & Project Scope

When colliding protons at relativistic velocities, quarks can annihilate or interact to produce unstable, short-lived parent states. Due to color confinement, quarks immediately fragment into hadronic jets or decay via fundamental interactions into clean lepton pairs, such as a muon ($\mu^-$) and an antimuon ($\mu^+$).

By extracting the energy ($E$) and three-momenta ($\vec{p}$) vectors of detected daughter leptons from raw collider telemetry, the invariant rest mass ($M_{\mu\mu}$) of the short-lived parent state can be structurally isolated mathematically via the relativistic energy-momentum invariant link:

$$M_{\mu\mu} = \sqrt{(E_1 + E_2)^2 - \left[(\mathbf{p}_{x1} + \mathbf{p}_{x2})^2 + (\mathbf{p}_{y1} + \mathbf{p}_{y2})^2 + (\mathbf{p}_{z1} + \mathbf{p}_{z2})^2\right]}$$

This codebase scans a highly broad mass scale dynamically, normalizing Kernel Density Estimations (KDE) to map absolute single-event tracking counts across multiple orders of magnitude.

### Targeted Resonances

* **$J/\psi$ Meson:** Rest mass $\approx 3.097\text{ GeV/c}^2$ (Discovered 1974, proving the existence of the Charm Quark).
* **$\Upsilon$ (Upsilon) Meson:** Rest mass $\approx 9.460\text{ GeV/c}^2$ (Discovered 1977, proving the existence of the Bottom Quark).
* **$Z$ Boson:** Rest mass $\approx 91.188\text{ GeV/c}^2$ (Discovered 1983, confirming Electroweak Unification).

---

## Technical Features

* **Multi-Column Column Vectorization:** Leverages `NumPy` multi-column vector structures to slice raw data parameters instantly, bypassing explicit nested iterations to evaluate high-volume array elements simultaneously.
* **Logarithmic Metric Scaling:** Standardizes an explicit $X$-axis log transformation and custom $Y$-axis symmetric log projection (`symlog`), allowing the visualization of massive $Z$-boson resonance peaks alongside micro-structures across multiple magnitudes within a single unified view.
* **Dynamic Event Count Normalization:** Translates continuous density curves back into empirical data boundaries by scaling the KDE distribution by total active data rows and bin step-sizes ($\text{Density} \times N_{\text{total}} \times dx$).
* **Sequential Spectral Topological Mapping:** Utilizes `scipy.signal.find_peaks` alongside localized peak masking. The algorithm locates the absolute global maximum ($J/\psi$) and iteratively evaluates subsequent coordinate domains along the positive horizontal axis ($x_{i+1} > x_i$) to target the heavier $\Upsilon$ and $Z$ masses without relying on hardcoded parameter windows.
* **Multi-Line Structural Annotation:** Interlocks dynamic text generation with custom canvas plotting, printing custom event counts explicitly onto the $Y$-axis tick array next to vertical tracking indicators.

---

## Repository Structure

```text
├── MuRun2010B.csv                        # Raw dimuon data file
├── jpsi_z_reconstruction.py              # Production Python script executing physics pipe
└── dimuon_invariant_mass_spectrum.png    # Spectroscopic readout

```

---

## Project Execution & Workflow

### 1. Prerequisites

Deploy the complete scientific computing and statistical visualization package dependencies:

```bash
pip install pandas numpy matplotlib seaborn scipy

```

### 2. Execution Pipeline

Ensure your raw data asset is placed in the active project folder named as `MuRun2010B.csv`, then trigger the runtime script:

```bash
python jpsi_z_reconstruction.py

```

---

## Plot Result

The output diagram will automatically log-scale across a domain stretching from $2.0\text{ GeV}$ up to $110.0\text{ GeV}$.
![Dimuon Invariant Mass Spectrum](dimuon_invariant_mass_spectrum.png)

---

## Dataset Reference

* **Source:** CERN Open Data Portal (Record 700)
* **Title:** Dimuon event information derived from the Run2010B public Mu dataset
* **Collector:** Thomas McCauley (Data recorded in 2010 and published in 2014)
* **Characteristics:** 100,000 recorded opposite-sign dimuon events filtered between $2\text{ GeV} < M_{\mu\mu} < 100\text{ GeV}$.
* **URL:** [https://opendata.cern.ch/record/700](https://opendata.cern.ch/record/700)
