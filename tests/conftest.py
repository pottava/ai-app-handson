"""pytest 設定ファイル: app モジュールの検索パスを設定する"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
