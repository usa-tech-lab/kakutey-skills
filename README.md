# kakutey-skills

個人事業主向け確定申告ワークフローの [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills) 集です。
[kakutey](https://github.com/usa-tech-lab/kakutey) 記帳アプリと連携し、証憑処理から青色申告書類の作成までをカバーします。

## スキル一覧

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

### 確定申告（青色申告決算書）

| スキル | 説明 |
|--------|------|
| **blue-return-income-statement** | 決算書（一般用）の入力値を算出 |
| **blue-return-monthly-sales** | 月別売上・仕入金額の入力値を算出 |
| **blue-return-sales-detail** | 売上先別の明細入力値を算出 |
| **blue-return-depreciation** | 減価償却資産の入力値を算出 |
| **blue-return-balance-sheet** | 貸借対照表の入力値を算出 |
| **blue-return-consumption-tax** | 消費税の課税取引金額内訳を算出 |
| **tax-return-prep** | 上記 blue-return-* スキルを統括し、e-Tax 用の全書類を一括生成 |

## インストール

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

以下のリファレンスファイルにはサンプルデータが入っています。実際のデータに置き換えてください。

| ファイル | 場所 | 内容 |
|----------|------|------|
| `customers.json` | `blue-return-sales-detail/references/` | 売上先の顧客情報（名前・住所・登録番号） |
| `business_profile.json` | `kakutey-reports/references/` | 事業者情報（屋号・会計期間・勘定科目設定） |
| `tax_classification.json` | `blue-return-consumption-tax/references/` | 勘定科目ごとの消費税区分 |

## ライセンス

MIT License
