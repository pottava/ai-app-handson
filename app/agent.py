from google.adk.agents import LlmAgent

from .tools import arithmetic_tools, user_apis

root_agent = LlmAgent(
    name="assistant_agent",
    model="gemini-2.5-flash",
    instruction="""
        あなたは算術演算とユーザー情報の取得を支援する優秀なアシスタントです。

        利用可能なツール:
        - 算術演算: 足し算・引き算・掛け算・割り算・階乗・べき乗・平方根
        - ユーザー情報: ペットストアの全ユーザー一覧の取得、ID によるユーザー情報の取得

        直感で質問に答えず、できる限り利用可能なツールを活用し、
        事前にどのように応答するかを慎重に計画してから、冷静に答えてください。
        """.strip(),
    tools=arithmetic_tools | user_apis,
)
