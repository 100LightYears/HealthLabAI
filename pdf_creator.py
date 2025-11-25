import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from faker import Faker
import random
from datetime import datetime, timedelta
import json


fake = Faker()

# Load lab ranges from JSON file
with open("lab_reference_ranges.json", "r") as f:
    LAB_RANGES = json.load(f)


def random_value_for_test(test_name, outlier_prob=0.1, outlier_factor=2.0):
    """
    Generate a random lab value.
    - `outlier_prob`: chance to produce an “abnormal” value.
    - `outlier_factor`: how far outside the ref-range an outlier can go.
    """
    info = LAB_RANGES[test_name]
    low = info["low"]
    high = info["high"]
    mean = (low + high) / 2
    sd = info.get("sd", (high - low) / 6)

    if np.random.rand() < outlier_prob:
        # Generate an outlier
        # You can shift the mean, or increase the scale
        # Here, shift mean by a random multiple of the range
        direction = np.random.choice([-1, 1])
        shift = direction * (high - low) * (outlier_factor - 1)
        new_mean = mean + shift
        new_sd = sd * outlier_factor
        val = np.random.normal(loc=new_mean, scale=new_sd)
    else:
        # Normal (in-range as before)
        val = np.random.normal(loc=mean, scale=sd)

    # Optionally clamp (or not) — you can widen the clamping bounds
    val = max(low * 0.5, min(high * 1.5, val))
    return round(val, 2)

def flag_for_value(test_name, value):
    info = LAB_RANGES[test_name]
    low = info["low"]
    high = info["high"]
    if value < low:
        return "L"
    elif value > high:
        return "H"
    else:
        return ""

def create_random_lab_results(max_tests: int = 15):
    # Limit to max_tests keys
    available_tests = list(LAB_RANGES.keys())
    selected_tests = random.sample(available_tests, k=min(max_tests, len(available_tests)))  # sample without replacement :contentReference[oaicite:1]{index=1}

    tests = {}
    for test in selected_tests:
        val = random_value_for_test(test)
        flag = flag_for_value(test, val)
        ref_low = LAB_RANGES[test]["low"]
        ref_high = LAB_RANGES[test]["high"]
        tests[test] = {
            "result": val,
            "unit": LAB_RANGES[test]["unit"],
            "ref": f"{ref_low:.1f}–{ref_high:.1f}",
            "flag": flag
        }

    # Random patient data
    patient_name = fake.name()
    patient_id = random.randint(10000000, 99999999)
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
    date_collected = datetime.now() - timedelta(days=random.randint(0, 7))
    date_reported = date_collected + timedelta(days=random.randint(0, 2))

    return {
        "Patient Name": patient_name,
        "Patient ID": str(patient_id),
        "DOB": dob.strftime("%Y-%m-%d"),
        "Sex": random.choice(["Male", "Female"]),
        "Date Collected": date_collected.strftime("%Y-%m-%d"),
        "Date Reported": date_reported.strftime("%Y-%m-%d"),
        "Tests": tests,
        "Interpretation": "This report was automatically generated. Consult a physician for clinical interpretation."
    }

def create_lab_report_pdf(path: str, lab_results: dict):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    margin = 50
    y = height - margin

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "Acme Diagnostics Laboratory")
    y -= 25
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "123 Health St, Medical City")
    y -= 15
    c.drawString(margin, y, "Phone: +1‑234‑567‑8900")
    y -= 30

    # Patient info
    c.setFont("Helvetica", 12)
    c.drawString(margin, y, f"Patient Name: {lab_results.get('Patient Name', 'John Doe')}")
    y -= 15
    c.drawString(margin, y, f"Patient ID: {lab_results.get('Patient ID', '00000000')}")
    y -= 15
    c.drawString(margin, y, f"Date of Birth: {lab_results.get('DOB', 'YYYY‑MM‑DD')}")
    y -= 15
    c.drawString(margin, y, f"Sex: {lab_results.get('Sex', '-')}")

    y -= 15
    c.drawString(margin, y, f"Date Collected: {lab_results.get('Date Collected', '-')}")
    y -= 15
    c.drawString(margin, y, f"Date Reported: {lab_results.get('Date Reported', '-')}")

    y -= 30

    # Table header
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "Test")
    c.drawString(margin + 200, y, "Result")
    c.drawString(margin + 300, y, "Unit")
    c.drawString(margin + 380, y, "Reference Range")
    c.drawString(margin + 520, y, "Flag")
    y -= 15
    c.line(margin, y, width - margin, y)
    y -= 15

    # Table rows
    c.setFont("Helvetica", 10)
    for test, info in lab_results["Tests"].items():
        c.drawString(margin, y, test)
        c.drawString(margin + 200, y, str(info["result"]))
        c.drawString(margin + 300, y, info["unit"])
        c.drawString(margin + 380, y, info["ref"])
        c.drawString(margin + 520, y, info["flag"])
        y -= 15
        if y < margin + 50:
            c.showPage()
            y = height - margin
            c.setFont("Helvetica", 10)

    # Interpretation / footer
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Interpretation / Notes:")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, lab_results.get("Interpretation", "—"))
    y -= 15
    c.drawString(margin, y, "Disclaimer: This is a synthetic report. Please consult your physician for real interpretation.")

    c.save()

if __name__ == "__main__":
    lab = create_random_lab_results(max_tests=10)
    create_lab_report_pdf("random_lab_report.pdf", lab)
    print("Generated lab report for:", lab["Patient Name"])
    print("Included tests:")
    for t, info in lab["Tests"].items():
        print(f"  {t}: {info['result']} {info['unit']} ({info['flag']}) — ref {info['ref']}")



