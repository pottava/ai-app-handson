# マルチ AI エージェント ハンズオン

## 始めましょう

マルチ AI エージェントをローカルやクラウドで実際に使ってみるまでの流れを体験します。

**[開始]** ボタンをクリックして次のステップに進みます。

<walkthrough-tutorial-duration duration="20"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="1"></walkthrough-tutorial-difficulty>


## 1. プロジェクトの設定

ハンズオン実施対象のプロジェクトを選択してください。

<walkthrough-project-setup></walkthrough-project-setup>


## 2. CLI 初期設定 & API 有効化

選択した環境変数と、ハンズオンで利用するリージョンを環境変数として設定しておきます。  
併せて Gemini の呼び出しを Vertex AI 経由とする `GOOGLE_GENAI_USE_VERTEXAI` も指定します。

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

リソースの利用上限を管理するプロジェクトも設定しておきます。

```bash
gcloud auth application-default set-quota-project "${GOOGLE_CLOUD_PROJECT}"
```


## 4. 学術研究サポート アプリケーション

[ADK の公式サンプル](https://github.com/google/adk-samples/tree/main/python/agents/academic-research) から "学術研究サポート アプリケーション" を画面 UI つきで動かしてみます。まずは資材をダウンロードしてきましょう。

```bash
curl -sL -o main.zip https://github.com/google/adk-samples/archive/refs/heads/main.zip
unzip main.zip
mv adk-samples-main/python/agents/academic-research .
rm -rf main.zip adk-samples-main
```


## 5. 実装の確認

メインのエージェント定義は <walkthrough-editor-open-file filePath="cloudshell_open/ai-app-handson/academic-research/academic_research/agent.py">この agent.py</walkthrough-editor-open-file> です。

1. 別途定義してあるサブエージェントを <walkthrough-editor-select-line filePath="cloudshell_open/ai-app-handson/academic-research/academic_research/agent.py" startLine="20" endLine="21" startCharacterOffset="0" endCharacterOffset="100">import</walkthrough-editor-select-line> して
2. <walkthrough-editor-select-line filePath="cloudshell_open/ai-app-handson/academic-research/academic_research/agent.py" startLine="39" endLine="40" startCharacterOffset="0" endCharacterOffset="100">AgentTool として内部的に利用できる</walkthrough-editor-select-line> ようにしています。

マルチエージェント構成において、エージェントの呼び出し方は大きく 2 種類「サブエージェント」と「ツールとしてのエージェント (AgentTool)」があります。使い分け方は [こちらのブログ](https://cloud.google.com/blog/ja/topics/developers-practitioners/where-to-use-sub-agents-versus-agents-as-tools) を参考にしていただけます。

サブエージェントのうち `academic_websearch_agent` についても中身を見てみましょう。

1. ADK が組み込みで用意している <walkthrough-editor-select-line filePath="cloudshell_open/ai-app-handson/academic-research/academic_research/sub_agents/academic_websearch/agent.py" startLine="17" endLine="17" startCharacterOffset="0" endCharacterOffset="100">Google 検索を import</walkthrough-editor-select-line> して
2. <walkthrough-editor-select-line filePath="cloudshell_open/ai-app-handson/academic-research/academic_research/sub_agents/academic_websearch/agent.py" startLine="29" endLine="29" startCharacterOffset="0" endCharacterOffset="100">Tool として設定</walkthrough-editor-select-line> しているようです。

シンプルですね！


## 6. ローカルでの起動

Python の仮想環境を作り

```bash
cd ~/cloudshell_open/ai-app-handson
cp .devcontainer/pyproject.toml .
uv venv
source .venv/bin/activate
uv sync
```

ローカルで起動してみましょう。

```bash
cd ~/cloudshell_open/ai-app-handson/academic-research
adk web --allow_origins "*"
```

1. ターミナルに表示されたリンクをクリックし、Web UI にアクセスし
2. 画面左上の `Select an agent` から `academic-research` を選択してください。
3. 右下の入力欄に「あなたは何ができますか？」と入力してみましょう。

例えば [Attention Is All You Need](https://arxiv.org/pdf/1706.03762) など、何か論文を手元にダウンロードして、それを解析させてみましょう。

4. 画面からその PDF をアップロードして「これを解析して」と依頼してみてください。

確認ができたら `Ctrl + C` で起動中の Web サービスを停止しましょう。


## 7. クラウドへのデプロイ

学術研究サポート アプリケーションを東京リージョンにデプロイしてみます。

まずはファイル群を経由するためのオブジェクト ストレージを作成し

```bash
export GOOGLE_CLOUD_STORAGE_BUCKET=ai-agents-$(whoami)-$(date -u '+%Y%m%d%H%M%S')
gcloud storage buckets create "gs://${GOOGLE_CLOUD_STORAGE_BUCKET}" --default-storage-class STANDARD --location "${GOOGLE_CLOUD_LOCATION}" --uniform-bucket-level-access
```

必要なサービスアカウントと権限を設定します。

```bash
gcloud beta services identity create --service "aiplatform.googleapis.com"
gcloud storage buckets add-iam-policy-binding "gs://${GOOGLE_CLOUD_STORAGE_BUCKET}" --member "serviceAccount:service-$( gcloud projects describe ${GOOGLE_CLOUD_PROJECT} --format 'get(projectNumber)' )@gcp-sa-aiplatform.iam.gserviceaccount.com" --role "roles/storage.objectViewer"
```

その上で、このアプリケーションをデプロイします。

```bash
cd ~/cloudshell_open/ai-app-handson/academic-research
uv sync --group deployment
uv run deployment/deploy.py --create
```


## 8. デプロイされたアプリの確認

デプロイがうまくいくと、最後のように以下のような出力があるはずです。

`Created remote agent: projects/123456789012/locations/us-central1/reasoningEngines/1234567890123456789`

最後の `1234567890123456789` にあたる部分を `AGENT_ENGINE_ID` として、ユーザーの ID も任意の値を設定しましょう。

```bash
export USER_ID=test-user
export AGENT_ENGINE_ID=
```

出力を見逃してしまった方は、クラウドのコンソールでも確認できます。

[https://console.cloud.google.com/agent-platform/runtimes](https://console.cloud.google.com/agent-platform/runtimes)

画面が開けたら

1. デプロイされた `academic_coordinator` を選択し
2. `プレイグラウンド` タブの右下で実際にチャットを試し
3. 画面左ての `セッション` や画面下の `ログ` に変化があることを確認してください


## 9. クラウド上のアプリに接続

では、クラウドにデプロイされた AI エージェントに対し、以下のコマンドで `ローカルから` 対話形式で接続してみましょう。

```bash
cd ~/cloudshell_open/ai-app-handson/academic-research
uv run deployment/test_deployment.py --resource_id=${AGENT_ENGINE_ID} --user_id=${USER_ID}
```

対話形式に入ったら、PDF が渡せるインターフェイスではないため、例えば以下のようなプロンプトを渡してみましょう。

```bash
以下、解析お願いします。タイトル「AGENT DATA PROTOCOL: UNIFYING DATASETS FOR DIVERSE, EFFECTIVE FINE-TUNING OF LLM AGENTS」。著者: Yueqi Song, Ketan Ramaneti, Zaid Sheikh, Ziru Chen, Boyu Gou。要旨「Public research results on large-scale supervised finetuning of AI agents remain relatively rare, since the collection of agent training data presents unique challenges. In this work, we argue that the bottleneck is not a lack of underlying data sources, but that a large variety of data is fragmented across heterogeneous formats, tools, and interfaces.」
```


## これで終わりです

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

これで `マルチ AI エージェント` のハンズオンは終了です。

お疲れさまでした！
