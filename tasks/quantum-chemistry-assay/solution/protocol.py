metadata = {
    'protocolName': 'Quantum-Guided Synergistic Catalytic Assay',
    'author': 'Text2WetLab Quantum Biology Initiative',
    'description': 'Automated 6-well dual-inhibitor synergy titration matrix derived from 4-qubit active space Hamiltonian calculation',
    'apiLevel': '2.14'
}


def run(protocol):
    # Load tipracks
    tips20 = protocol.load_labware('opentrons_96_tiprack_20ul', 10, label='tiprack_20')
    tips300 = protocol.load_labware('opentrons_96_tiprack_300ul', 11, label='tiprack_300')

    # Load pipettes
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tips20])
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tips300])

    # Load labware
    tuberack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 1, label='tuberack')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 2, label='plate')

    # Reagents in tuberack
    tube_enzyme = tuberack['A1']
    tube_alpha = tuberack['A2']
    tube_beta = tuberack['A3']
    tube_cofactor = tuberack['A4']
    tube_buffer = tuberack['B1']

    # Step 1: Dispense buffer using P300 (air/plastic contact, single tip)
    buffer_doses = {
        'A1': 70.0,
        'A2': 70.0,
        'A3': 70.0,
        'A4': 80.0,
        'B1': 85.0,
        'B2': 95.0,
    }
    p300.pick_up_tip()
    for well_id, vol in buffer_doses.items():
        p300.aspirate(vol, tube_buffer)
        p300.dispense(vol, plate[well_id])
    p300.drop_tip()

    # Step 2: Dispense cofactor using P20 (5.0 uL into all 6 wells)
    p20.pick_up_tip()
    for well_id in ['A1', 'A2', 'A3', 'A4', 'B1', 'B2']:
        p20.aspirate(5.0, tube_cofactor)
        p20.dispense(5.0, plate[well_id])
    p20.drop_tip()

    # Step 3: Dispense enzyme stock using P20 (10.0 uL into A1..B1, B2 is apo)
    p20.pick_up_tip()
    for well_id in ['A1', 'A2', 'A3', 'A4', 'B1']:
        p20.aspirate(10.0, tube_enzyme)
        p20.dispense(10.0, plate[well_id])
    p20.drop_tip()

    # Step 4: Dispense Inhibitor Alpha using P20 (fresh tip per dispense)
    alpha_doses = {
        'A1': 7.5,
        'A2': 10.0,
        'A3': 5.0,
        'A4': 2.5,
    }
    for well_id, vol in alpha_doses.items():
        p20.pick_up_tip()
        p20.aspirate(vol, tube_alpha)
        p20.dispense(vol, plate[well_id])
        p20.drop_tip()

    # Step 5: Dispense Inhibitor Beta using P20 (fresh tip per dispense)
    beta_doses = {
        'A1': 7.5,
        'A2': 5.0,
        'A3': 10.0,
        'A4': 2.5,
    }
    for well_id, vol in beta_doses.items():
        p20.pick_up_tip()
        p20.aspirate(vol, tube_beta)
        p20.dispense(vol, plate[well_id])
        p20.drop_tip()

    # Step 6: Gentle mixing using P300 (fresh tip per well to eliminate cross-talk)
    for well_id in ['A1', 'A2', 'A3', 'A4', 'B1', 'B2']:
        p300.pick_up_tip()
        p300.mix(3, 50.0, plate[well_id])
        p300.drop_tip()
