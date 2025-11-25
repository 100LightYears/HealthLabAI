import asyncio
import os
from lab_workflow.parsing_tool import parse_lab_results_from_pdf
from lab_workflow.runner import run_lab_workflow, ask_followup
from pdf_creator import create_random_lab_results, create_lab_report_pdf  # <-- Import functions

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("No API key set. Define GOOGLE_API_KEY or GEMINI_API_KEY in .env")

async def main():
    pdf_path = "random_lab_report.pdf"
    # Generate new lab results and PDF each run
    lab_data = create_random_lab_results(max_tests=10)
    create_lab_report_pdf(pdf_path, lab_data)

    lab_results = parse_lab_results_from_pdf(pdf_path)

    if not lab_results:
        print("⚠️ Could not extract any lab results from the PDF.")
        return

    explanation, session_id, runner, session_service = await run_lab_workflow(lab_results)
    print("\n=== Explanation ===")
    print(explanation)

    while True:
        question = input("\nAsk a follow-up question (or type 'quit' to exit): ")
        if question.strip().lower() == "quit":
            print("Exiting. Take care!")
            break
        answer = await ask_followup("user1", session_id, runner, session_service, question)
        print("Answer:", answer)

if __name__ == "__main__":
    asyncio.run(main())
