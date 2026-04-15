"""算術エージェントの e2e 評価テスト

ADK の AgentEvaluator を使用して、エージェントが正しいツールを呼び出し、
正しい答えを返すことを検証する。

実行方法:
    uv run pytest -m e2e tests/test_agent_eval.py -v

注意: 実際に Gemini API を呼び出すため、Google Cloud 認証情報が必要です。
"""

from pathlib import Path

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

EVAL_DIR = Path(__file__).parent / "eval"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_arithmetic_agent_eval() -> None:
    """算術エージェントが加算・べき乗のツールを呼び、正しい答えを返すことを検証する。

    RED 条件: power が arithmetic_tools に未追加の場合、"2 の 3 乗" の質問に
    対してエージェントが正しい答え (8) を返せず FAIL する。
    GREEN 条件: power を arithmetic_tools に追加後、エージェントが正しく 8 を
    返し PASS する。
    """
    # test_config.json は eval_dataset と同一ディレクトリに配置することで自動参照される
    await AgentEvaluator.evaluate(
        agent_module="app",
        eval_dataset_file_path_or_dir=str(EVAL_DIR / "arithmetic_eval.test.json"),
    )
