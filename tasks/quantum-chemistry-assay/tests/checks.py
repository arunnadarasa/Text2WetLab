#!/usr/bin/env python3
"""
Text2WetLab Verifier & Rubric Checks for Quantum Chemistry Synergistic Assay
=============================================================================
Evaluates Opentrons OT-2 protocols against the 6-point robotics benchmark:
1. Python AST parsing
2. API metadata structure (apiLevel >= 2.2)
3. Deck slot validity ([1, 11] bounds, zero collisions)
4. Instrument mount management (P20 left, P300 right)
5. Tip lifecycle discipline (pick_up_tip == drop_tip balance)
6. Volume boundaries and pipetting logic for quantum-derived titration matrix
"""

import ast
import json
import re
import sys
from pathlib import Path


def evaluate_protocol(protocol_path: Path):
    if not protocol_path.exists():
        return {
            "score": 0.0,
            "pass": False,
            "error": f"File not found: {protocol_path}"
        }

    code = protocol_path.read_text(encoding="utf-8")
    checks = {}
    passed_count = 0
    total_criteria = 6

    # 1. AST Syntax
    try:
        parsed_ast = ast.parse(code)
        checks["criterion_1_ast_syntax"] = {
            "pass": True,
            "details": f"Valid Python 3 syntax ({len(code.splitlines())} lines)."
        }
        passed_count += 1
    except SyntaxError as e:
        checks["criterion_1_ast_syntax"] = {"pass": False, "details": f"SyntaxError: {e}"}
        return {"score": 0.0, "pass": False, "criteria": checks}

    # 2. Protocol API Structure & Metadata
    has_metadata = False
    has_api_level = False
    has_run_func = False
    api_version = None

    for node in parsed_ast.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "metadata":
                    has_metadata = True
                    if isinstance(node.value, ast.Dict):
                        for k, v in zip(node.value.keys, node.value.values):
                            if isinstance(k, ast.Constant) and k.value == "apiLevel":
                                has_api_level = True
                                api_version = getattr(v, "value", None)
        elif isinstance(node, ast.FunctionDef) and node.name == "run":
            has_run_func = True

    c2_pass = has_metadata and has_api_level and has_run_func
    checks["criterion_2_protocol_api_structure"] = {
        "pass": c2_pass,
        "details": f"metadata={has_metadata}, apiLevel='{api_version}', run(protocol)={has_run_func}"
    }
    if c2_pass:
        passed_count += 1

    # 3. Deck Layout Validity
    deck_slots = re.findall(r'protocol\.load_labware\([^,]+,\s*(\d+)', code)
    deck_slots = [int(s) for s in deck_slots]
    valid_slots = all(1 <= s <= 11 for s in deck_slots) and (len(deck_slots) == len(set(deck_slots)))
    has_required_slots = all(s in deck_slots for s in [1, 2, 10, 11])
    c3_pass = valid_slots and has_required_slots
    checks["criterion_3_deck_layout_validity"] = {
        "pass": c3_pass,
        "details": f"Loaded slots: {deck_slots} (bounds 1..11, required: [1, 2, 10, 11])."
    }
    if c3_pass:
        passed_count += 1

    # 4. Pipette Management
    pipette_loads = re.findall(r'protocol\.load_instrument\(\s*["\']([^"\']+)["\'],\s*["\']([^"\']+)["\']', code)
    mounts = [m for _, m in pipette_loads]
    valid_mounts = all(m in ["left", "right"] for m in mounts) and (len(mounts) == len(set(mounts)))
    models = [p for p, _ in pipette_loads]
    has_p20 = any("p20" in m.lower() for m in models)
    has_p300 = any("p300" in m.lower() for m in models)
    c4_pass = valid_mounts and has_p20 and has_p300
    checks["criterion_4_pipette_management"] = {
        "pass": c4_pass,
        "details": f"Instruments: {dict(zip(mounts, models))} (left/right mounts, P20 & P300 present)."
    }
    if c4_pass:
        passed_count += 1

    # 5. Tip Lifecycle Discipline
    pick_ups = len(re.findall(r'\.pick_up_tip\(', code))
    drop_tips = len(re.findall(r'\.drop_tip\(', code))
    return_tips = len(re.findall(r'\.return_tip\(', code))
    total_drops = drop_tips + return_tips
    c5_pass = (pick_ups == total_drops) and (pick_ups > 0)
    checks["criterion_5_tip_lifecycle_discipline"] = {
        "pass": c5_pass,
        "details": f"pick_up_tip={pick_ups}, drop_tip={drop_tips}, return_tip={return_tips} (balanced: {c5_pass})."
    }
    if c5_pass:
        passed_count += 1

    # 6. Volume Boundary & Assay Specifics
    # Extract all numeric float/int constants in code that correspond to dosing
    num_constants = [node.value for node in ast.walk(parsed_ast) if isinstance(node, ast.Constant) and isinstance(node.value, (int, float))]
    
    # Check key quantum dosing volumes: 70.0, 80.0, 85.0, 95.0 (buffer), 5.0 (cofactor), 10.0 (enzyme), 7.5, 2.5 (titration)
    expected_doses = {70.0, 80.0, 85.0, 95.0, 5.0, 10.0, 7.5, 2.5}
    found_doses = expected_doses.intersection(set(num_constants))
    has_quantum_doses = len(found_doses) >= 6
    
    # Check pipette call actions
    has_mix = ".mix(" in code
    has_p20_calls = "p20.aspirate" in code or "p20.transfer" in code or "p20.dispense" in code
    has_p300_calls = "p300.aspirate" in code or "p300.transfer" in code or "p300.dispense" in code
    
    c6_pass = has_quantum_doses and has_mix and has_p20_calls and has_p300_calls
    checks["criterion_6_volume_boundary_guards"] = {
        "pass": c6_pass,
        "details": f"Quantum doses verified: {sorted(list(found_doses))} uL, mixing_performed={has_mix}, dual_pipette_pipetting={has_p20_calls and has_p300_calls}"
    }
    if c6_pass:
        passed_count += 1

    final_score = passed_count / total_criteria
    return {
        "score": round(final_score, 3),
        "pass": final_score == 1.0,
        "passed_criteria": f"{passed_count}/{total_criteria}",
        "criteria": checks
    }


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "solution" / "protocol.py"
    res = evaluate_protocol(target)
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["pass"] else 1)
