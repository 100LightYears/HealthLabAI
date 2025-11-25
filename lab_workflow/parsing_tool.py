import re
from typing import Dict
import pdfplumber

def parse_lab_results_from_pdf(pdf_path: str) -> Dict[str, float]:
    results: Dict[str, float] = {}
    pattern = re.compile(
        r"^([\w_]+)\s+([0‑9]+(?:\.[0‑9]+)?)\s+([^\s]+)\s+([0‑9]+(?:\.[0‑9]+)?)\s?[–\\-]\s?([0‑9]+(?:\.[0‑9]+)?)"
    )
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.splitlines():
                line = line.strip()
                m = pattern.match(line)
                if m:
                    name = m.group(1)
                    val_str = m.group(2)
                    try:
                        val = float(val_str)
                        results[name] = val
                    except ValueError:
                        pass
                else:
                    parts = line.split()
                    if len(parts) >= 2:
                        key = parts[0]
                        maybe_num = parts[1]
                        try:
                            val2 = float(maybe_num)
                            results[key] = val2
                        except ValueError:
                            pass
    return results
