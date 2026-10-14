# 🧬⚛️ Quantum Chemistry to Robotic Wet-Lab Automation Framework
### A Developer & Scientist Guide for Bridging Quantum Electronic Structure with Opentrons OT-2 Liquid Handling

---

## 1. Executive Summary

In contemporary computational drug discovery, quantum computing algorithms (Variational Quantum Eigensolvers [VQE], quantum phase estimation, and dynamic circuits) are increasingly applied to active-space electronic structure problems—such as mapping multi-target catalytic enzyme mechanisms, transition-state barrier heights, and non-covalent synergistic inhibitor binding.

However, a severe **translational gap** separates in silico quantum chemistry predictions from empirical wet-lab validation. A computed ground-state energy or optimal stoichiometric ratio is clinically and biochemically useless until translated into a physical assay: buffer conditioning, enzyme dilution, ligand titration, and spectrophotometric or fluorescent readout.

**Text2WetLab** provides the missing bridge: an open, layered robotics verification benchmark that evaluates whether LLM agents and computational chemistry pipelines can generate syntactically valid, collision-free, and biologically sound **Opentrons OT-2 Python (API v2.14+)** automation protocols from quantum chemistry outputs.

---

## 2. End-to-End Pipeline Architecture

```
[ PDB / AlphaFold Biomolecular Complex ]
                   │
                   ▼
[ Active Space Selection: CASSCF via PySCF / OpenFermion ]
                   │
                   ▼
[ Second-Quantized Hamiltonian: Jordan-Wigner / Bravyi-Kitaev ]
                   │
                   ▼
[ Quantum Compilation & Routing: pytket 2.18+ / Guppy 1.0 ]
       ├── Rebase to Trapped-Ion Native Gates: {PhasedX, Rz, ZZPhase}
       └── Mid-Circuit Measurement & Reset (MCMR) Active Parity Filtering (ASPS)
                   │
                   ▼
[ Cloud Execution / Emulation ]
       ├── Quantinuum Nexus (`Helios-1E-lite` / `H2-Emulator`)
       ├── Aqora Platform (`nexus:H2-Emulator`)
       └── Classical Supremacy Flooring (NumPy exact solve: 3.04 µs CPU floor)
                   │
                   ▼
[ Biochemical Assay Parameter Serialization (JSON) ]
       ├── Optimal Stoichiometric Ratios (e.g. 1:1, 2:1 titration matrix)
       ├── Reagent Stock Concentrations & Target Microplate Layout
       └── Volume Bounds (P20: 1–20 µL, P300: 20–300 µL)
                   │
                   ▼
[ Opentrons OT-2 Protocol Synthesis (`/app/protocol.py`) ]
                   │
                   ▼
[ Text2WetLab 6-Point Layered Robotic Verification ]
       ├── Criterion 1: AST Syntax Parsing
       ├── Criterion 2: API Metadata Structure (`apiLevel: '2.14'`)
       ├── Criterion 3: Deck Slot Bounds & Collision Avoidance (Slots 1–11)
       ├── Criterion 4: Pipette Mount Instrumentation (P20 Left, P300 Right)
       ├── Criterion 5: Tip Lifecycle Discipline (`pick_up_tip` == `drop_tip`)
       └── Criterion 6: Liquid Class Capacity & Volume Boundary Guards
```

---

## 3. Recommended Software Stack & Repositories

Life science developers and computational teams should assemble the following vetted open-source software stack:

### 3.1 Quantum Chemistry & Circuit Compilation
* **`pytket` & Plugins** ([`github.com/CQCL/tket`](https://github.com/CQCL/tket)):
  - *Purpose:* High-performance quantum circuit compiler developed by Cambridge Quantum / Quantinuum.
  - *Key Feature:* Hardware-agnostic synthesis, peephole optimization, and automated rebasing into trapped-ion native two-qubit $ZZ(\theta)$ phase gates.
  - *Plugins:* `pytket-qiskit`, `pytket-quantinuum`.
* **`openfermion` & `pyscf`** ([`github.com/quantumlib/OpenFermion`](https://github.com/quantumlib/OpenFermion) & [`github.com/pyscf/pyscf`](https://github.com/pyscf/pyscf)):
  - *Purpose:* Electronic structure calculations, molecular orbital integrals, Complete Active Space Self-Consistent Field (CASSCF) selection, and fermion-to-qubit mappings.
* **`guppy-lang` & `hugr`** ([`github.com/CQCL/guppy`](https://github.com/CQCL/guppy) & [`github.com/CQCL/hugr`](https://github.com/CQCL/hugr)):
  - *Purpose:* Quantinuum's statically typed quantum programming language and graph intermediate representation, enabling mid-circuit dynamic measurements and branching logic.
* **`praqtice` & `QUOPS`** ([`github.com/sandialabs/praqtice`](https://github.com/sandialabs/praqtice)):
  - *Purpose:* Sandia National Laboratories' Quantum Universal Operations Performance System (arXiv:2609.12146) for measuring volumetric capability ($Q = 2 \times w \times d$) and execution speed ($\Omega$, ops/sec).

### 3.2 Robotic Lab Automation & Benchmarking
* **`opentrons` Python API** ([`github.com/Opentrons/opentrons`](https://github.com/Opentrons/opentrons)):
  - *Purpose:* Official library for defining and simulating liquid handling on the Opentrons OT-2 and Flex robots.
  - *CLI Simulator:* `opentrons_simulate protocol.py`.
* **`Text2WetLab`** ([`github.com/arunnadarasa/Text2WetLab`](https://github.com/arunnadarasa/Text2WetLab)):
  - *Purpose:* Rigorous physical AI benchmark for verifying generated liquid handling code against real wet-lab failure modes (tip balance, volume overdraw, cross-contamination).

---

## 4. Applying for Quantum Hardware & Cloud Access

To execute or emulate quantum chemistry circuits, life science teams should leverage the following cloud platforms:

### 4.1 Quantinuum Nexus (`nexus.quantinuum.com`)
* **What It Offers:** Cloud interface to Quantinuum's commercial H-Series trapped-ion processors (including H1-1, H2-1) and managed emulator tiers (`Helios-1E-lite`, `H2-Emulator`).
* **Application Pathway:**
  1. Register for an account on the [Quantinuum Nexus Portal](https://nexus.quantinuum.com).
  2. Academic groups and research institutes can apply via Quantinuum's Academic Access Program for research compute grants.
  3. Commercial and biotech developers can request enterprise trials through the Quantinuum Partner Network.
* **SDK Configuration:**
  ```bash
  export QUANTINUUM_API_KEY="your-nexus-api-token"
  ```

### 4.2 Aqora Quantum Platform (`aqora.io`)
* **What It Offers:** Competitive benchmarking platform with pre-allocated credits for Quantinuum trapped-ion emulators and superconducting backends.
* **Application Pathway:**
  1. Join active challenge tracks (e.g. the Quantinuum Singapore Grand Challenge or Open Innovation Tracks).
  2. Access managed provider jobs (`nexus:H2-Emulator`, `nexus:Helios-1E-lite`) directly via the Aqora CLI (`aqora`) or GraphQL API.

### 4.3 Cloud Hyperscalers (AWS Braket & Azure Quantum)
* **AWS Braket:** Offers Quantinuum and IonQ trapped-ion QPUs. Research groups can apply for the **AWS Cloud Credit for Research** grant ($10,000–$50,000 compute credits).
* **Azure Quantum:** Offers access to Quantinuum trapped-ion backends with Azure Quantum Credits programs for computational chemistry projects.

---

## 5. Scientific Rigor & Classical Flooring Discipline

When publishing or deploying quantum chemistry workflows, scientists and developers must uphold strict epistemic standards:

1. **The Classical Supremacy Floor ($3.04\,\mu\text{s}$ CPU Baseline):**
   - For small active spaces ($N \le 16$ qubits), exact classical state vector contraction (using NumPy, SciPy, or PyTorch on modern x86/ARM CPUs) executes in microseconds ($\approx 3.04\,\mu\text{s}$), achieving $>10^8\text{ ops/sec}$.
   - Never claim premature "quantum supremacy" for problems where classical matrix mechanics strictly dominates. Clearly explain that quantum emulation serves to validate state fidelity, multi-qubit phase interference, and error mitigation algorithms (e.g. ASPS parity filtering).
2. **Transparent Hardware Tier Demarcation:**
   - Clearly delineate physical QPU execution from cloud emulator execution.
   - If 0 physical hardware shots were run, state: *"100% of execution was conducted on trapped-ion cloud emulators; 0 physical QPU hardware shots claimed."*
3. **The Fault-Tolerant Scientific Utility Gap:**
   - As established by Sandia National Laboratories (arXiv:2609.12146), practical scientific utility for full molecular dynamics requires circuit volumes $Q_{\text{utility}} \ge 2.0 \times 10^6$ (100 qubits at depth $10^4$).
   - Report the quantitative gap between your current NISQ/emulator capability boundary and fault-tolerant scale ($3,900\times$ to $100,000\times$) to maintain credibility with peer reviewers and clinicians.

---

## 6. Hands-On Tutorial: Building and Verifying a Quantum-WetLab Assay

### Step 1: Serialize Quantum Eigensolver Output
Create an assay definition JSON (`data/quantum_catalytic_parameters.json`) storing the computed active-space ground state, target inhibitor stoichiometry, stock concentrations, and well volumes.

### Step 2: Implement the Opentrons OT-2 Protocol
Write `/app/protocol.py` adhering to OT-2 Python API v2.14+:
* Load `opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap` on Slot 1 (`tuberack`).
* Load `corning_96_wellplate_360ul_flat` on Slot 2 (`plate`).
* Load tipracks on Slots 10 (P20) and 11 (P300).
* Dispense buffer, cofactors, enzymes, and titrated inhibitor volumes according to the quantum prediction.
* Enforce **Tip Lifecycle Discipline**: Always drop tips after transferring reactive reagents to prevent stock tube contamination.

### Step 3: Run the Text2WetLab 6-Point Verifier
Run the automated verification suite:
```bash
python scripts/verify_quantum_chemistry_assay.py tasks/quantum-chemistry-assay/solution/protocol.py
```

Expected output:
```json
{
  "score": 1.0,
  "pass": true,
  "passed_criteria": "6/6",
  "criteria": {
    "criterion_1_ast_syntax": {"pass": true, "details": "Valid Python 3 syntax"},
    "criterion_2_protocol_api_structure": {"pass": true, "details": "metadata=True, apiLevel='2.14', run=True"},
    "criterion_3_deck_layout_validity": {"pass": true, "details": "Slots 1, 2, 10, 11 within bounds"},
    "criterion_4_pipette_management": {"pass": true, "details": "P20 left, P300 right"},
    "criterion_5_tip_lifecycle_discipline": {"pass": true, "details": "pick_ups == drop_tips, balanced"},
    "criterion_6_volume_boundary_guards": {"pass": true, "details": "Quantum doses verified: [2.5, 5.0, 7.5, 10.0, 70.0, 80.0, 85.0, 95.0] uL"}
  }
}
```
