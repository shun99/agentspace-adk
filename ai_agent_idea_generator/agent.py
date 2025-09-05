import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import load_artifacts


root_agent = Agent(
    name="ai_agent_ideal_generator",
    model="gemini-2.5-flash",
    description=(
        "企業情報のファイルからどのようなAI Agentを企業内で作成すると良いか提案するアドバイザーです"
    ),
    instruction=(
        "全ての回答は load_artifacts ツールを使って、添付ファイルを参照の上回答してください。"
    ),
    tools=[load_artifacts],
)