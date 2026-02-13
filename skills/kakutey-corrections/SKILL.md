---
name: kakutey-corrections
description: Update or delete existing journal entries in the kakutey bookkeeping app. Supports full edits, evidence linking, and journal deletion.
---

# kakutey-corrections

kakutey の仕訳修正ワークフローを支援するスキル。登録済み仕訳の更新（証憑紐付け含む）と削除を行う。

## リソース

- **API 仕様**: [api_journals.md](references/api_journals.md)

## スクリプト実行方法

すべてのスクリプトは `scripts/` ディレクトリから `uv run` で実行する。

## ワークフロー

### A. 仕訳の修正

1. **対象の仕訳を特定**（kakutey-bookkeeping の `get_journals.py` で entity_id を確認）
   ```bash
   uv run .claude/skills/kakutey-bookkeeping/scripts/get_journals.py 2025-01-01 2025-01-31
   ```

2. **仕訳を修正**（フル更新）
   ```bash
   uv run scripts/update_journal.py '{"entity_id": 1, "date": "2025-01-15", "description": "文房具購入（修正）", "lines": [{"side": "debit", "account": "消耗品費", "amount": 1500}, {"side": "credit", "account": "現金", "amount": 1500}], "evidence_ids": [], "expected_revision": 1}'
   ```

### B. 証憑の紐付け

既存の仕訳に証憑 ID を追加する（GET → マージ → PUT を自動化）。

```bash
uv run scripts/update_journal.py '{"entity_id": 1, "add_evidence_ids": [10, 20]}'
```

### C. 仕訳の削除

```bash
uv run scripts/delete_journal.py 1
```

## スクリプト一覧

| スクリプト | 説明 |
|-----------|------|
| `update_journal.py` | 仕訳を更新（フル更新 or 証憑追加モード） |
| `delete_journal.py` | 仕訳を削除 |

## 関連スキル

- **kakutey-bookkeeping**: 仕訳の entity_id 確認（`get_journals.py`）、修正後の再確認
- **kakutey-evidence**: 紐付けする証憑の entity_id 確認（`search_evidence.py`）
