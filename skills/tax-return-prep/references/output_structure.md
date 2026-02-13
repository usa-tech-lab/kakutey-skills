# 確定申告/ 出力構成と実行順序

## 実行順序

依存関係を考慮した推奨実行順序:

```
Step 0: kakutey-reports でデータ取得
  ├─ get_summary.py --type both    → PL/BS データ
  └─ get_fixed_assets.py --depreciation <年度> → 固定資産データ
        │
        ▼
Step 1: blue-return-income-statement → 01_決算書.md
        │  ※ PL データが必要
        ▼
Step 2: blue-return-monthly-sales → 02_月別売上仕入.md
        │  ※ 仕訳データの月別集計が必要
        ▼
Step 3: blue-return-sales-detail → 03_売上明細.md
        │  ※ 取引先情報 (customers.json) + 売上仕訳が必要
        ▼
Step 4: blue-return-depreciation → 04_減価償却.md
        │  ※ 固定資産データが必要
        ▼
Step 5: blue-return-balance-sheet → 05_貸借対照表.md
        │  ※ BS データが必要。所得金額は 01_決算書 の値を使用
        ▼
Step 6: blue-return-consumption-tax → 06_消費税.md
        ※ 01_決算書 の全経費科目 + 消費税区分 (tax_classification.json) が必要
```

## 依存関係

| ステップ | 入力元 | 出力 |
|----------|--------|------|
| Step 1 | kakutey PL データ | 01_決算書.md |
| Step 2 | 仕訳データ（月別集計） | 02_月別売上仕入.md |
| Step 3 | 仕訳データ + customers.json | 03_売上明細.md |
| Step 4 | kakutey 固定資産データ | 04_減価償却.md |
| Step 5 | kakutey BS データ + 01_決算書の所得金額 | 05_貸借対照表.md |
| Step 6 | 01_決算書の全科目 + tax_classification.json | 06_消費税.md |

Step 2 と Step 3 は互いに独立。Step 4 も独立。
Step 5 は Step 1 の所得金額に依存。
Step 6 は Step 1 の経費内訳に依存。

## 各スキルの参照先

| スキル | リファレンス |
|--------|-------------|
| `blue-return-income-statement` | SKILL.md 内の出力項目定義 |
| `blue-return-monthly-sales` | SKILL.md 内の出力項目定義 |
| `blue-return-sales-detail` | SKILL.md + `references/customers.json` |
| `blue-return-depreciation` | SKILL.md 内の出力項目定義 |
| `blue-return-balance-sheet` | SKILL.md 内の出力項目定義 |
| `blue-return-consumption-tax` | SKILL.md + `references/tax_classification.json` |

## 検算チェックリスト

全ファイル生成後に以下を確認:

- [ ] `01_決算書` の売上金額 = `02_月別売上仕入` の合計
- [ ] `01_決算書` の売上金額 = `03_売上明細` の合計
- [ ] `01_決算書` #18 減価償却費 = `04_減価償却` の合計額
- [ ] `05_貸借対照表` 期首: 資産合計 = 負債+資本合計
- [ ] `05_貸借対照表` 期末: 資産合計 = 負債+資本合計（所得金額含む）
- [ ] `01_決算書` の経費合計 = `06_消費税` A列(32)の経費計
- [ ] `06_消費税` A = B + C（各科目）
- [ ] `06_消費税` C = D+E + F+G（各科目）
