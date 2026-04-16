# 生成 AI エージェント開発 ハンズオン

## 始めましょう

生成 AI エージェントを作り、クラウドにデプロイ、利用するまでの流れを体験していきます。

**[開始]** ボタンをクリックして次のステップに進みます。

<walkthrough-tutorial-duration duration="20"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="1"></walkthrough-tutorial-difficulty>


## 1. プロジェクトの設定

ハンズオン実施対象のプロジェクトを選択してください。

<walkthrough-project-setup></walkthrough-project-setup>


## 2. CLI 初期設定 & API 有効化

選択した環境変数と、ハンズオンで利用するリージョンを環境変数として設定しておきます。  
併せて Gemini の呼び出しを Vertex AI 経由とする `GOOGLE_GENAI_USE_VERTEXAI` も指定しておきます。

```bash
export GOOGLE_CLOUD_PROJECT=<walkthrough-project-id/>
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_GENAI_USE_VERTEXAI=True
```

[gcloud（Google Cloud の CLI ツール)](https://cloud.google.com/sdk/gcloud?hl=ja) のデフォルト プロジェクトを設定します。

```bash
gcloud config set project "${GOOGLE_CLOUD_PROJECT}"
```

[Vertex AI](https://cloud.google.com/vertex-ai?hl=ja) など、関連サービスを有効化し、利用できる状態にしましょう。

<walkthrough-enable-apis apis=
 "generativelanguage.googleapis.com,
  aiplatform.googleapis.com,
  artifactregistry.googleapis.com,
  cloudbuild.googleapis.com,
  run.googleapis.com,
  iap.googleapis.com,
  iamcredentials.googleapis.com,
  cloudresourcemanager.googleapis.com">
</walkthrough-enable-apis>


## 3. 認証

みなさんの権限でアプリケーションを動作させられるよう、[デフォルト認証情報（ADC）](https://cloud.google.com/docs/authentication/provide-credentials-adc?hl=ja) を作成します。表示される URL をブラウザの別タブで開き、認証コードをコピー、ターミナルにもどってきてそれを貼り付け、Enter を押してください。

```bash
gcloud auth application-default login --quiet
```


## 4. 生成 AI アプリケーションの確認

算術演算のできる AI アプリです。

関数ツールは <walkthrough-editor-select-line filePath="cloudshell_open/ai-app-handson/app/agent.py" startLine="17" endLine="17" startCharacterOffset="4" endCharacterOffset="100">agent.py の 18 行目</walkthrough-editor-select-line> で設定していますが

<walkthrough-editor-open-file filePath="cloudshell_open/ai-app-handson/app/tools/arithmetic_operations.py">AI から利用される関数</walkthrough-editor-open-file> はいずれも、とてもシンプルな実装です。

ADK は関数の引数やコメント情報を整理して LLM に渡し、どの関数をいつ、どんな引数で使うかを考える手助けをします。ADK は関数の返り値として **辞書型** を[推奨しています](https://google.github.io/adk-docs/tools/function-tools/#return-type)が、例えば<walkthrough-editor-select-line filePath="cloudshell_open/ai-app-handson/app/tools/arithmetic_operations.py" startLine="54" endLine="54" startCharacterOffset="8" endCharacterOffset="100">ここ</walkthrough-editor-select-line>ではゼロ除算のときに `{"status": "error"}` を返し、LLM に処理が失敗したことを伝えています。


## 5. ローカルでの AI エージェント起動

Python の仮想環境を作り

```bash
cd ~/cloudshell_open/ai-app-handson
uv venv
source .venv/bin/activate
uv sync
```

起動してみましょう。

```bash
adk web --allow_origins "*"
```

ターミナルに表示される `INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)` の中のリンクをクリックし、Web UI にアクセスしてください。

画面の左上 "Select an agent" となっている選択肢から `app` を選び、切り替わった右側の画面の下 "Type a Message" に以下のような質問をしてみましょう。

```txt
9*(1234+678/32) の答えは？
```

正しい答え `11296.6875` になりましたか？


## 6. ADK の機能確認

ADK は開発支援のライブラリであると同時に、以下のように様々な機能が同梱されています。

- 開発者用の Web UI
- ツールの呼び出し結果や応答速度などの計測や表示
- API 形式でのサービス提供
- セッション管理、状態管理
- テスト・評価のための仕組み
- GUI でのエージェント作成
- マルチエージェント管理などなど

少し動作を確認してみましょう。

1. 画面の左側の Invocations の "9*(1234+678/32) の答えは？" をクリックしてみる
2. みなさんの指示の後に表示された `divide` や `add` をクリックしてみる

確認ができたらターミナルにもどり、`Ctrl + C` コマンドで起動中の Web サービスを停止しましょう。


## 7. Cloud Run へのデプロイ

算術演算 AI エージェントをクラウドにデプロイしてみます。

ソースコードのビルドもクラウドで実施できるよう、依存関係ファイルも app フォルダに作成します。

```bash
uv pip freeze > app/requirements.txt
```

その上で ADK の `deploy` コマンドを実行してみましょう！

途中で `Deploying from source requires... Do you want to continue (Y/n)?` と聞かれたら **Y**、`Allow unauthenticated invocations to [...] (y/N)?` については本来安全のため N を選ぶべきですが、今回はハンズオンということもあり **y** と回答してください。

完成までは 5 分前後かかります。

```bash
export GENAI_APP_NAME="arithmetic_operations_agent"
export CLOUD_RUN_SERVICE_NAME="arithmetic-operations-service"
adk deploy cloud_run --region "${GOOGLE_CLOUD_LOCATION}" --app_name "${GENAI_APP_NAME}" --service_name "${CLOUD_RUN_SERVICE_NAME}" ./app -- --set-env-vars "GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT},GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION},GOOGLE_GENAI_USE_VERTEXAI=True"
```

## 8. クラウド上のアプリに接続

接続先を確認し、

```bash
endpoint=$( gcloud run services describe "${CLOUD_RUN_SERVICE_NAME}" --region "${GOOGLE_CLOUD_LOCATION}" --format='value(status.address.url)' ) && echo "${endpoint}"
```

会話するためのセッションを作りましょう。

```bash
curl -sX POST -H "Authorization: Bearer $( gcloud auth print-identity-token )" -H "Content-Type: application/json" ${endpoint}/apps/${GENAI_APP_NAME}/users/user-01/sessions/session-001 | jq .
```

メッセージを送信してみます。  
（応答結果はすべてのやりとりが返ってくるため `sed` と `jq` で結果だけを抽出していますが、気になる方は `jq -s .` と書き換えてみてください）

```text
curl -sX POST -H "Authorization: Bearer $( gcloud auth print-identity-token )" -H "Content-Type: application/json" ${endpoint}/run \
    -d '{
        "app_name": "arithmetic_operations_agent",
        "user_id": "user-01",
        "session_id": "session-001",
        "streaming": false,
        "new_message": {
            "role": "user",
            "parts": [{"text": "75*(430*91-7130)/(60*2000)の答えは？"}]
        }
    }' | jq ".[-1].content.parts[0].text"
```


## 9. Cloud Run の状態確認

[Cloud Run](https://cloud.google.com/run?hl=ja) は Google Cloud のフルマネージドなコンテナ実行環境です。今回のような AI エージェントを一番手軽に、費用を抑えて動かすことができます。

クラウド上で何が確認できるのかを確かめてみましょう。

1. 隣のタブで [https://console.cloud.google.com/run/services](https://console.cloud.google.com/run/services) を開き `arithmetic-operations-service` という名前をクリックしてください。
2. `Observability` というタブの `Metrics` というメニューが開いたと思います。ここでは、ユーザーからのリクエスト数や応答速度などが確認できます。
3. `Observability` タブのまま `Logs` メニューをクリックしてみてください。みなさんからの直前の要求がログとして出力されていることと思います。
4. お隣の `Revisions` タブは、新しい AI エージェントをデプロイする度に増えるデプロイ履歴です。過去のバージョンに戻すことも簡単です。
5. `Revisions` タブの右半分をご確認ください。Containers, Networking, Security, YAML といった項目が並んでいます。ここでは、今回のデプロイにおける環境変数などの設定値が確認できます。
6. その隣の `Source` タブでは、クラウドにアップロードされたソースコードが確認できます。
7. `Security` タブでは、認証されたユーザだけがアクセスできるような制御など、セキュリティ関係の設定ができますが、今日は割愛します。気になる方は [こちら](https://docs.cloud.google.com/run/docs/securing/security?hl=ja) をご覧ください。


## 10. チャレンジ問題

余力のある方は `instruction` や `tools` の変更、または関数の追加を行って、以下の課題にチャレンジしてみてください！

- 現在の実装では `((12^3)*4!-56)/10` の正答率を高めるためのツールが足りません。関数を追加するなどして、LLM を助けてあげてください。
- `app/tools/apis.py` は外部 API をツールとして利用する実装例です。これを使い、LLM がお客様メールアドレス一覧を返すことを確認してください。

さらに余力のある方は https://explore.qwiklabs.com のクラスに戻り、「Gemini CLI で AI エージェントの開発（機能追加や不具合修正）をする場合は..」からコーディングエージェントによる開発をお試しください！


## これで終わりです

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

これで `生成 AI エージェント開発` のハンズオンは終了です。

お疲れさまでした！
