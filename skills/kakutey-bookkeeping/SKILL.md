---
name: kakutey-bookkeeping
description: Register journal entries (single or bulk) and list journals in the kakutey bookkeeping app. Use for daily bookkeeping, year-end batch entry, and reviewing posted journals.
---

# kakutey-bookkeeping

kakutey の仕訳登録ワークフローを支援するスキル。勘定科目の確認、単発・一括の仕訳登録、登録済み仕訳の一覧表示を行う。

## リソース

- **API 仕様**: [api_journals.md](references/api_journals.md)

## スクリプト実行方法

すべてのスクリプトは `scripts/` ディレクトリから `uv run` で実行する。

## ワークフロー

### A. 年次一括記帳

仕訳データを JSON ファイルとして準備し、一括登録する。

1. **勘定科目を確認**して、科目名を把握する
   ```bash
   uv run scripts/get_accounts.py
   uv run scripts/get_accounts.py --category expense
   ```

2. **仕訳データ JSON を準備**する（配列形式）
   ```json
   [
     {
       "date": "2025-01-15",
       "description": "文房具購入",
       "lines": [
         {"side": "debit", "account": "消耗品費", "amount": 1000},
         {"side": "credit", "account": "現金", "amount": 1000}
       ]
     }
   ]
   ```

3. **一括登録**する
   ```bash
   uv run scripts/bulk_add_journals.py journals.json
   ```

4. **登録内容を確認**する
   ```bash
   uv run scripts/get_journals.py 2025-01-01 2025-12-31
   ```

### B. 日常の仕訳登録

単発の取引を登録する。

```bash
# 簡易形式（2行仕訳）
uv run scripts/add_journal.py '{"date":"2025-03-10","description":"サンプル商事 打ち合わせ交通費","debit_account":"旅費交通費","credit_account":"現金","amount":500}'

# 複合仕訳（3行以上）
uv run scripts/add_journal.py '{"date":"2025-01-01","description":"開始仕訳","lines":[{"side":"debit","account":"現金","amount":50000},{"side":"debit","account":"普通預金","amount":100000},{"side":"credit","account":"元入金","amount":150000}]}'
```

## スクリプト一覧

| スクリプト | 説明 |
|-----------|------|
| `get_accounts.py` | 勘定科目一覧（entity_id, code, name, category） |
| `add_journal.py` | 仕訳を1件登録（簡易形式 or 複合仕訳形式） |
| `bulk_add_journals.py` | JSON ファイルから仕訳を一括登録 |
| `get_journals.py` | 指定期間の仕訳一覧を表示（entity_id 付き） |

## 関連スキル

- **kakutey-evidence**: 仕訳に証憑（領収書等）を紐付ける場合に使用
- **kakutey-corrections**: 登録済み仕訳の修正・削除を行う場合に使用
