# Quantum-Guided Synergistic Catalytic Assay Setup

Translate a quantum electronic structure prediction into an automated biochemical assay on an Opentrons OT-2 liquid handler.

A 4-qubit active space Hamiltonian calculation (modeled via variational quantum eigensolvers and trapped-ion native Pauli interaction operators) has determined the optimal stoichiometric ratio and dose-response titration curve for two synergistic inhibitors (Compound Alpha and Compound Beta) targeting an enzymatic catalytic pocket. Your task is to automate the preparation of this 6-condition assay matrix (4 titration points + 2 controls) in a 96-well flat-bottom plate.

Write an Opentrons OT-2 Python protocol that implements this assay, and save it as **`/app/protocol.py`**.

---

## 1. Robot Deck Layout (Fixed)

Load **each labware with its exact label** as listed below:

```python
protocol.load_labware('<load name>', <slot>, label='<label>')
```

| Slot | Labware (load name) | Label | Description |
|---|---|---|---|
| 1 | `opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap` | `tuberack` | 24-tube rack holding stock reagents |
| 2 | `corning_96_wellplate_360ul_flat` | `plate` | 96-well destination plate for optical reading |
| 10 | `opentrons_96_tiprack_20ul` | `tiprack_20` | Tip rack for P20 pipette (left mount) |
| 11 | `opentrons_96_tiprack_300ul` | `tiprack_300` | Tip rack for P300 pipette (right mount) |

### Pipette Instrumentation:
- **Left Mount:** `p20_single_gen2` (tipracks: `tiprack_20`, operating volume: 1–20 µL).
- **Right Mount:** `p300_single_gen2` (tipracks: `tiprack_300`, operating volume: 20–300 µL).

---

## 2. Reagents in Stock Tubes (Slot 1 `tuberack`)

- **Well A1:** `Enzyme Stock (250 nM)` (1000 µL)
- **Well A2:** `Inhibitor Alpha (100 µM)` (500 µL)
- **Well A3:** `Inhibitor Beta (100 µM)` (500 µL)
- **Well A4:** `Catalytic Cofactor (1 mM)` (1000 µL)
- **Well B1:** `Reaction Buffer (pH 7.4)` (1400 µL)

---

## 3. Protocol Steps to Implement (Total Reaction Volume: 100 µL per well)

Implement the following steps in sequence:

### Step 1: Dispense Reaction Buffer (P300 Pipette)
Transfer Reaction Buffer from `tuberack['B1']` into the destination plate:
- 70.0 µL into `plate['A1']`
- 70.0 µL into `plate['A2']`
- 70.0 µL into `plate['A3']`
- 80.0 µL into `plate['A4']`
- 85.0 µL into `plate['B1']`
- 95.0 µL into `plate['B2']`
*(Note: A single tip may be used for buffer dispensing if the tip touches only clean air/plastic).*

### Step 2: Dispense Catalytic Cofactor (P20 Pipette)
Transfer 5.0 µL of Cofactor from `tuberack['A4']` into each of the 6 wells (`A1`, `A2`, `A3`, `A4`, `B1`, `B2`).

### Step 3: Dispense Enzyme Stock (P20 Pipette)
Transfer 10.0 µL of Enzyme Stock from `tuberack['A1']` into wells `A1`, `A2`, `A3`, `A4`, and `B1`.
*(Leave well `B2` without enzyme as the negative apo control).*

### Step 4: Dispense Inhibitor Alpha (P20 Pipette, Fresh Tip per dispense)
Transfer Inhibitor Alpha from `tuberack['A2']` into the titration wells:
- 7.5 µL into `plate['A1']`
- 10.0 µL into `plate['A2']`
- 5.0 µL into `plate['A3']`
- 2.5 µL into `plate['A4']`

### Step 5: Dispense Inhibitor Beta (P20 Pipette, Fresh Tip per dispense)
Transfer Inhibitor Beta from `tuberack['A3']` into the titration wells:
- 7.5 µL into `plate['A1']`
- 5.0 µL into `plate['A2']`
- 10.0 µL into `plate['A3']`
- 2.5 µL into `plate['A4']`

### Step 6: Gentle Assay Mixing (P300 Pipette)
Perform gentle mixing (3 cycles of 50.0 µL aspiration/dispense) in each active well (`A1`, `A2`, `A3`, `A4`, `B1`, `B2`).
*(Crucial: Pick up a fresh tip for each well during mixing to prevent cross-contamination between titration arms).*

---

## 4. Technical Constraints & Verifier Rules

- Set `apiLevel: '2.14'` in protocol `metadata`.
- Use the correct pipette for each volume:
  - Volumes between 1.0 and 20.0 µL **must** use `p20_single_gen2`.
  - Volumes between 20.0 and 300.0 µL **must** use `p300_single_gen2`.
- **Tip Lifecycle Discipline:** Every picked-up tip must be explicitly dropped via `.drop_tip()`. Never reuse a tip that has touched an inhibitor or enzyme into another tube.
- All 6 wells must end holding exactly **100.0 µL**.
- Simulate with `opentrons_simulate /app/protocol.py`. The protocol must execute without runtime or geometry errors.
