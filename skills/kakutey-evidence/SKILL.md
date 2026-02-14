---
name: kakutey-evidence
description: Upload and search evidence files (receipts, invoices, statements) in the kakutey bookkeeping app. Use when attaching supporting documents to journal entries.
---

# kakutey-evidence

kakutey の証憑管理ワークフローを支援するスキル。証憑ファイルのアップロード、検索を行う。

## 前提条件

kakutey CLI がインストールされ、アプリが起動している必要があります。

```bash
# インストール
npm install -g kakutey-cli

# 状態確認
kakutey health
```

## リソース

- **API 仕様**: [api_evidence.md](references/api_evidence.md)
- **CLI ヘルプ**: `kakutey evidence --help`

## ワークフロー

### A. 証憑のアップロードと仕訳紐付け

1. **証憑ファイルをアップロード**する
   ```bash
   kakutey evidence upload /path/to/receipt.pdf
   kakutey evidence upload /path/to/receipt.pdf --name "領収書 サンプル商事 2025-01"
   ```
   → `entity_id` が出力される（紐付けに使用）

2. **仕訳に紐付ける**（kakutey-corrections の `journals attach` コマンドを使用）
   ```bash
   kakutey journals attach 1 10
   ```

### B. 証憑の検索

登録済みの証憑を検索する。

```bash
# 表示名で検索
kakutey evidence search --name "サンプル商事"

# タグで検索
kakutey evidence search --tag "交通費"
```

## CLI コマンド一覧

| コマンド | 説明 |
|---------|------|
| `kakutey evidence upload <path> [--name <name>]` | 証憑ファイルをアップロード（PDF, JPG, PNG, CSV, XLSX） |
| `kakutey evidence search --name <query>` | 表示名で証憑を検索 |
| `kakutey evidence search --tag <tag>` | タグで証憑を検索 |
| `kakutey journals attach <journal_id> <evidence_id...>` | 仕訳に証憑を紐付け |

## 関連スキル

- **kakutey-bookkeeping**: 仕訳の entity_id を確認する場合に使用
- **kakutey-corrections**: 仕訳に証憑を紐付ける場合に使用（`kakutey journals attach` コマンド）
