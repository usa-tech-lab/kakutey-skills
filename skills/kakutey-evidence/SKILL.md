---
name: kakutey-evidence
description: Upload and search evidence files (receipts, invoices, statements) in the kakutey bookkeeping app. Use when attaching supporting documents to journal entries.
---

# kakutey-evidence

kakutey の証憑管理ワークフローを支援するスキル。証憑ファイルのアップロード、検索を行う。

## リソース

- **API 仕様**: [api_evidence.md](references/api_evidence.md)

## スクリプト実行方法

すべてのスクリプトは `scripts/` ディレクトリから `uv run` で実行する。

## ワークフロー

### A. 証憑のアップロードと仕訳紐付け

1. **証憑ファイルをアップロード**する
   ```bash
   uv run scripts/upload_evidence.py /path/to/receipt.pdf "領収書 サンプル商事 2025-01"
   ```
   → `entity_id` が出力される（紐付けに使用）

2. **仕訳に紐付ける**（kakutey-corrections スキルの `update_journal.py` を使用）
   ```bash
   uv run .claude/skills/kakutey-corrections/scripts/update_journal.py '{"entity_id": 1, "add_evidence_ids": [10]}'
   ```

### B. 証憑の検索

登録済みの証憑を検索する。

```bash
# 表示名で検索
uv run scripts/search_evidence.py --name "サンプル商事"

# タグで検索
uv run scripts/search_evidence.py --tag "交通費"
```

## スクリプト一覧

| スクリプト | 説明 |
|-----------|------|
| `upload_evidence.py` | 証憑ファイルをアップロード（PDF, JPG, PNG, CSV, XLSX） |
| `search_evidence.py` | 表示名またはタグで証憑を検索 |

## 関連スキル

- **kakutey-bookkeeping**: 仕訳の entity_id を確認する場合に使用
- **kakutey-corrections**: 仕訳に証憑を紐付ける場合に使用（`update_journal.py` の証憑追加モード）
