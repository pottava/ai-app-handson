from google.adk.agents import LlmAgent
from google.adk.tools import enterprise_web_search
from .tools import arithmetic_tools


root_agent = LlmAgent(
    name="arithmetic_operations_agent",
    model="gemini-2.5-flash",
    instruction="""
        あなたは算術演算を支援する優秀なアシスタントです。
        直感で質問に答えず、できる限り利用可能なツールを鑑み
        事前にどのように応答するかを慎重に計画、冷静に答えてください。
        """.strip(),
    tools=arithmetic_tools,
)
