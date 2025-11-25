# HealthLab AI Workflow

## Problem
Interpreting medical lab reports can be confusing for non-experts. Patients often receive PDF reports with complex test names, values, and reference ranges, but lack clear explanations or guidance. This can lead to anxiety, misunderstanding, or missed follow-up actions.

## Solution
This project automates the extraction, explanation, and interactive Q&A of medical lab test results using AI agents. It generates synthetic lab reports, parses results from PDF, and provides empathetic, easy-to-understand explanations and follow-up answers. The workflow leverages Google Gemini LLMs and configurable reference ranges for accurate interpretation.

## Architecture for Prototype

- **Synthetic Lab Report Generation:** Randomly creates realistic lab test results and PDF reports.
- **Lab Result Parsing:** Extracts test names and values from PDF files.
- **AI Explanation Agent:** Explains lab results in plain language, highlighting concerns and next steps.
- **Follow-up Q&A Agent:** Answers user questions about their lab results.
- **Reference Ranges:** Uses configurable reference ranges for interpretation.
- **Logging:** Tracks agent interactions for debugging and review.

## Requirements

- Python 3.8+
- `reportlab`, `faker`, `pdfplumber`, `numpy`
- Google ADK and Gemini API access
- `.env` file with your API key:
`GOOGLE_API_KEY=your_api_key_here`


## Setup

1. Clone the repository.
2. Install dependencies:

`pip install -r requirements.txt`
3. Add your Google API key to `.env`.
4. Run the main workflow:

`python main.py`

## Usage

- On each run, a synthetic lab report PDF is generated.
- The workflow extracts lab results, explains them, and allows interactive follow-up questions.
- Type your questions at the prompt, or type `quit` to exit.

## File Structure

- `main.py` — Entry point for the workflow.
- `pdf_creator.py` — Generates random lab results and PDF reports.
- `lab_workflow/parsing_tool.py` — Parses lab results from PDF.
- `lab_workflow/explain_tool.py` — Explains lab results using reference ranges.
- `lab_workflow/agents.py` — Defines AI agents for explanation and Q&A.
- `lab_workflow/runner.py` — Orchestrates agent workflow and sessions.
- `lab_reference_ranges.json` — Reference ranges for lab tests.

## Disclaimer

This project is for educational and informational purposes only. It does not provide medical advice. Always consult a healthcare professional for clinical interpretation.
