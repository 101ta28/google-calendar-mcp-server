# Google Calendar MCP Server

[English README is here](README.md)

このドキュメントでは、Google Calendar APIを使用してカレンダーの内容を検索するMCPサーバーを構築するための手順を説明します。

## 前提条件

- [uv](https://github.com/astral-sh/uv)がインストールされていること
- Googleアカウントを持っていること

## 手順

### 1. Google Cloud プロジェクトを作成

Google Cloud コンソールまたは、下のリンクから、Google Calendar API を有効にします。

[APIの有効化](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com&hl=ja)

### 2. OAuth 2.0 同意画面を設定

Google Cloud コンソールのメニューまたは、下のリンクからブランディングに移動します。

[ブランディング](https://console.cloud.google.com/auth/branding?hl=ja)

1. アプリ名を設定します。
2. ユーザーサポートメールを設定します。
3. デベロッパーの連絡先情報を設定します。

### 3. デスクトップ アプリケーションの認証情報を設定

Google Cloud コンソールのメニューまたは、下のリンクからクライアントに移動します。

[クライアント](https://console.cloud.google.com/auth/clients?hl=ja)

1. **クライアントを作成**をクリックします。
2. アプリケーション種類 -> デスクトップアプリ をクリックします。
3. 名前フィールドに、認証情報の名前を入力します。
4. 作成をクリックします。
5. ダウンロードした JSON ファイルを `credentials.json` として保存し、ファイルを作業ディレクトリに移動します。

### 4. Python 環境のセットアップ

#### 仮想環境の作成

1. ターミナルまたはコマンドプロンプトを開きます。
2. プロジェクトディレクトリに移動します。
3. 仮想環境の設定と必要なライブラリをダウンロードします。

   ```sh
   uv sync
   ```

### 5. calendar_settings.jsonの設定

1. プロジェクトディレクトリ内の`calendar_settings.json.sample`ファイルを編集します。

例えば、以下のように設定します。

```json
{
  "calendar_ids": {
    "primary": "primary",
    "work": "example_work_schedule_id"
  }
}
```

- `primary`: GoogleアカウントのプライマリカレンダーのID（通常は"primary"）。
- `work`: 仕事用カレンダーのID。

必要なカレンダーIDを設定し、ファイルを`calendar_settings.json`に**リネーム**して保存してください。

### 6. MCPの設定

1. プロジェクトディレクトリ内の`.vscode`ディレクトリに移動し、`mcp.json`ファイルを編集します。
2. `mcp.json`ファイルを以下のように編集してください。

   ```json
   {
     "servers": {
       "google-calendar-mcp-server": {
         "type": "stdio",
         "command": "/home/<username>/<dir>/.venv/bin/python",
         "args": [
           "/home/<username>/<dir>/google_calendar_mcp_server.py"
         ]
       }
     }
   }
   ```

   - `<username>`の部分をあなたのユーザー名に置き換えてください。
   - `<dir>`の部分をプロジェクトのディレクトリ名に置き換えてください。

   例えば、ユーザー名が`tatsuya`、プロジェクトのディレクトリ名が`google-calendar-mcp-server`の場合、以下のようになります。

   ```json
   {
     "servers": {
       "google-calendar-mcp-server": {
         "type": "stdio",
         "command": "/home/tatsuya/google-calendar-mcp-server/.venv/bin/python",
         "args": [
           "/home/tatsuya/google-calendar-mcp-server/main.py"
         ]
       }
     }
   }
   ```

3. 編集が完了したら、`mcp.json`ファイルを保存してください。

### 7. Agentモードの設定

Visual Studio CodeのGitHub Copilot ChatのAgentモードを設定する手順を以下に示します。

1. Visual Studio Codeを起動し、拡張機能のインストール画面を開きます。
2. 「GitHub Copilot Chat」拡張機能を検索してインストールします。
3. インストールが完了したら、左側のサイドバーに「Copilot Chat」アイコンが表示されます。それをクリックしてCopilot Chatパネルを開きます。
4. Copilot Chatパネルの上部にある「歯車」アイコンをクリックして設定画面を開きます。
5. 設定画面で「Agent Mode」を有効にします。

### 8. MCPの利用

1. Copilot Chatパネルを開きます。
2. 例えば、「4月8日の予定をリストアップしてほしいです。」といったチャットを行います。
3. ツールの実行確認が表示されるので、**Continue**ボタンをクリックして実行します。
4. 初回利用時は、ブラウザが立ち上がり、Googleアカウントへのアクセス許可を求められます。許可を与えてください。
5. 結果が表示されます。

### トラブルシューティング

- **エラーが発生した場合**: エラーメッセージを確認し、必要に応じて依存関係を再インストールしたり、Google Cloud Consoleの設定を確認してください。
