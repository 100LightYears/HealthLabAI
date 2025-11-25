import json
from google.adk.runners import InMemoryRunner
from google.genai import types
from google.adk.plugins.logging_plugin import LoggingPlugin

from .agents import lab_agent, followup_agent
from google.adk.agents import SequentialAgent

pipeline = SequentialAgent(
    name="LabWorkflow",
    sub_agents=[lab_agent, followup_agent]
)

def configure_runner_with_logging():
    runner = InMemoryRunner(
        agent=pipeline,
        app_name="agents",
        plugins=[LoggingPlugin()]  # Enable logging plugin
    )

    print("✅ LoggingPlugin is configured.")

    return runner

async def run_lab_workflow(lab_results: dict):
    content = types.Content(role="user", parts=[types.Part(text=json.dumps({"lab_results": lab_results}))])

    runner = configure_runner_with_logging()
    session_service = runner.session_service
    user_id = "user1"
    session_id = "session_lab"

    await session_service.create_session(app_name="agents", user_id=user_id, session_id=session_id)

    final_message = None
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.content:
            for p in event.content.parts:
                if p.text:
                    final_message = p.text

    return final_message, session_id, runner, session_service

async def ask_followup(user_id: str, session_id: str, runner, session_service, question: str):
    content2 = types.Content(role="user", parts=[types.Part(text=question)])
    answer = None
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content2):
        if event.content:
            for p in event.content.parts:
                if p.text:
                    answer = p.text
    return answer