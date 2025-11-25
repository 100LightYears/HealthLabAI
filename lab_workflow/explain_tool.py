import json
from typing import Dict, Any
from google.adk.tools import FunctionTool

# Load reference ranges from a JSON file
def load_reference_ranges(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    ref = {}
    # Extract low, high, and unit for each test
    for name, rd in data.items():
        ref[name] = (rd["low"], rd["high"], rd["unit"])
    return ref

# Global variable holding reference ranges for lab tests
REFERENCE_RANGES = load_reference_ranges("lab_reference_ranges.json")

# Explain lab results based on reference ranges
def explain_lab_results_from_dict(lab_results: Dict[str, float]) -> Dict[str, Any]:
    explanations = {}
    out_of_range = []
    # Iterate through each lab result
    for name, val in lab_results.items():
        if name in REFERENCE_RANGES:
            low, high, unit = REFERENCE_RANGES[name]
            normal = f"{low}–{high} {unit}"
            in_range = (low <= val <= high)
        else:
            normal = None
            in_range = None

        # Generate explanation and next steps based on value range
        if in_range is True:
            expl = (
                f"{name} is {val} {unit}, which is within the normal range ({normal}). "
                "That’s generally a good sign."
            )
            next_steps = "No immediate concern, but keep monitoring as advised by your healthcare provider."
        elif in_range is False:
            expl = (
                f"{name} is {val} {unit}, which is outside the normal range ({normal}). "
                "This could possibly indicate something to check, but it doesn’t mean a diagnosis."
            )
            next_steps = "Consider repeating this test or discussing it with your doctor."
            out_of_range.append(name)
        else:
            expl = f"{name} is {val}. We don't have a reference range for this test, so it's hard to interpret confidently."
            next_steps = "You might want to ask your doctor to interpret this value."

        # Store explanation for each test
        explanations[name] = {
            "value": val,
            "normal_range": normal,
            "explanation": expl,
            "next_steps": next_steps,
        }

    # Create summary and disclaimer
    summary = (
        "You have several lab test values. "
        f"{len(out_of_range)} of them are outside the usual reference ranges. "
        "Below is a breakdown per test."
    )
    disclaimer = (
        "⚠️ **Disclaimer:** I am not a doctor. This is for general informational purposes only, "
        "to help you understand your lab results. Always consult a medical professional for any health concerns."
    )

    # Return structured explanation
    return {
        "summary": summary,
        "tests": explanations,
        "disclaimer": disclaimer,
    }

# Register the explanation function as a tool for an agent
explain_tool = FunctionTool(explain_lab_results_from_dict)
