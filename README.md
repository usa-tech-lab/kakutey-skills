# kakutey-skills

個人事業主向け確定申告ワークフローの [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills) 集です。
[kakutey](https://github.com/usa-tech-lab/kakutey) 記帳アプリと連携し、証憑処理から記帳までをカバーします。

## スキル一覧

### 会計方針

| スキル | 説明 |
|--------|------|
| **accounting-policy-setup** | 会計方針を対話的に定義し、ワークスペースに `accounting-policy.md` を生成するメタスキル |

### アプリ管理

| スキル | 説明 |
|--------|------|
| **kakutey-installer** | kakutey アプリを GitHub からダウンロード・セットアップする |
| **kakutey-launcher** | kakutey アプリ（Electron + FastAPI）を起動する |
| **kakutey-healthcheck** | バックエンド (port 8000) とフロントエンド (port 4200) の稼働確認 |
| **kakutey-stopper** | kakutey アプリのプロセスを停止する |
| **tax-workspace-setup** | 年度ごとの確定申告ワークスペース（証憑・処理・確定申告フォルダ）を作成 |

### 記帳操作

| スキル | 説明 |
|--------|------|
| **kakutey-bookkeeping** | 仕訳の登録（単発・一括）と一覧取得 |
| **kakutey-evidence** | 証憑ファイル（領収書・請求書等）のアップロードと検索 |
| **kakutey-corrections** | 既存仕訳の修正・削除・証憑紐付け |
| **kakutey-reports** | 損益計算書・貸借対照表・固定資産データの取得 |

### 証憑処理

| スキル | 説明 |
|--------|------|
| **evidence-processing** | 証憑ファイルを構造化マークダウン・仕訳 JSON に変換 |
| **image-describer** | Gemini 3 Flash を使った画像・PDF の内容分析 |

## インストール

### プラグインとしてインストール（推奨）

Claude Code 内で以下を実行：

```
/plugin marketplace add usa-tech-lab/kakutey-skills
/plugin install kakutey-skills@kakutey-marketplace
```

インストール後、スキルは `/kakutey-skills:スキル名` で呼び出せます（例: `/kakutey-skills:kakutey-bookkeeping`）。

### 手動インストール

```bash
# リポジトリをクローン
git clone https://github.com/usa-tech-lab/kakutey-skills.git

# 使いたいスキルをコピー（例: 全スキル）
cp -R kakutey-skills/skills/* ~/.claude/skills/

# または特定のスキルだけ
cp -R kakutey-skills/skills/kakutey-bookkeeping ~/.claude/skills/
```

## 前提条件

- **kakutey アプリ**: kakutey-* スキル群の利用に必要
- **Python 3**: スクリプト実行用
  - `requests` パッケージ（kakutey API 連携）
  - `google-genai` パッケージ（image-describer 用）
- **環境変数**:
  - `GOOGLE_CLOUD_PROJECT` — image-describer で Vertex AI を使用する場合

## カスタマイズ

### 会計方針（推奨）

`accounting-policy-setup` スキルで `accounting-policy.md` を生成し、事業の実情に合わせて編集してください。`accounting-policy.md` には事業者情報、仕訳ルール、消費税区分、顧客情報等が含まれ、他のスキルが AI エージェントのコンテキストとして参照します。

### フォールバック

`accounting-policy.md` が未作成の場合、以下のリファレンスファイルがフォールバックとして使用されます。サンプルデータが入っているため、実際のデータに置き換えてください。

| ファイル | 場所 | 内容 |
|----------|------|------|
| `business_profile.json` | `kakutey-reports/references/` | 事業者情報（屋号・会計期間・勘定科目設定） |

## ライセンス

MIT License
