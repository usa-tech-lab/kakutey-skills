---
name: tax-return-prep
description: Generate tax return input value markdowns for each e-Tax form page. Orchestrates blue-return-* skills using data from kakutey-reports to produce filing-ready documents.
---
# 確定申告 入力値マークダウンの生成

kakutey の決算データから、e-Tax 確定申告作成コーナーの各画面に対応する入力値マークダウンを `確定申告/` ディレクトリに生成する。

## 前提

- kakutey アプリが起動済みで、対象年度の仕訳が登録済みであること
- `kakutey-reports` スキルでデータ取得が可能な状態であること
- `blue-return-*` スキル（6つ）が利用可能であること

## ワークフロー

### Step 0: kakutey からデータ取得

`kakutey-reports` スキルのスクリプトで決算データを取得する:

```bash
# 損益計算書 + 貸借対照表
python kakutey-reports/scripts/get_summary.py --type both

# 固定資産 + 減価償却
python kakutey-reports/scripts/get_fixed_assets.py --depreciation <年度>
```

### Step 1-6: blue-return-* スキルで入力値を算出

取得したデータを元に、各 `blue-return-*` スキルに従って入力値を算出し、マークダウンとして `確定申告/` に保存する。

実行順序と依存関係は [output_structure.md](references/output_structure.md) を参照。

## 出力ファイル一覧

| 順序 | ファイル名 | 対応する e-Tax 画面 | 使用スキル |
|------|-----------|-------------------|-----------|
| 1 | `01_決算書.md` | 決算書（一般用）の入力 | `blue-return-income-statement` |
| 2 | `02_月別売上仕入.md` | 売上（収入）金額・仕入金額の入力 | `blue-return-monthly-sales` |
| 3 | `03_売上明細.md` | 売上（収入）金額の明細の入力 | `blue-return-sales-detail` |
| 4 | `04_減価償却.md` | 減価償却資産の入力 | `blue-return-depreciation` |
| 5 | `05_貸借対照表.md` | 貸借対照表（一般用）の入力 | `blue-return-balance-sheet` |
| 6 | `06_消費税.md` | 消費税 決算額・課税取引金額の内訳等の入力 | `blue-return-consumption-tax` |

## 検算ルール

スキル間で以下の値が一致することを確認する:

| チェック項目 | 一致すべきスキル |
|-------------|----------------|
| 売上金額 | `01_決算書` #1 = `02_月別売上仕入` 合計 = `03_売上明細` 合計 = `06_消費税` A列(1) |
| 減価償却費 | `01_決算書` #18 = `04_減価償却` 合計 |
| 経費合計 | `01_決算書` 経費計 = `06_消費税` A列(32) |
| 期首資産 = 期首負債+資本 | `05_貸借対照表` |
| 期末資産 = 期末負債+資本 | `05_貸借対照表`（所得金額含む） |
