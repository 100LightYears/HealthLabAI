from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from .explain_tool import explain_tool

# Lab explanation agent
lab_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite"),
    name="lab_explanation_agent",
    instruction=(
        "You are a calm, empathetic assistant specialized in explaining medical lab test results. "
        "You receive a JSON with lab test names and values. "
        "Call the `explain_lab_results` tool to compute structured explanations. "
        "Then respond in natural language explaining each test in a way a non‑expert can understand. "
        "Include what might be concerning, what is good, next steps, and a clear disclaimer."
    ),
    tools=[explain_tool],
    output_key="lab_explanation",
)

# Follow-up agent
followup_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite"),
    name="lab_followup_agent",
    instruction=(
        "Here is the explanation of your lab results: {lab_explanation}.\n\n"
        "Now, you can ask me questions about your lab results. "
        "For example: 'Why is my cholesterol high?' or 'What should I do next for this value?' "
        "Answer in a clear, empathetic style, using the explanation as background. "
        "Include context, possible implications, and sensible next steps, but remind the user to talk to a medical professional."
    ),
    output_key="followup_response",
)
