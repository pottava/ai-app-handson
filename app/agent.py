from google.adk import Agent

from .tools import arithmetic_tools


root_agent = Agent(
    name="assistant_agent",
    model="gemini-2.5-flash",
    instruction="""
        あなたは算術演算を支援する優秀なアシスタントです。

        利用可能なツール:
        - 算術演算: 足し算・引き算・掛け算・割り算・階乗

        直感で質問に答えず、できる限り利用可能なツールを活用し、
        事前にどのように応答するかを慎重に計画してから、冷静に答えてください。
        """.strip(),
    tools=arithmetic_tools,
)
