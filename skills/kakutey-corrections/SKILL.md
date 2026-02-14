---
name: kakutey-corrections
description: Update or delete existing journal entries in the kakutey bookkeeping app. Supports full edits, evidence linking, and journal deletion.
---

# kakutey-corrections

kakutey の仕訳修正ワークフローを支援するスキル。登録済み仕訳の更新（証憑紐付け含む）と削除を行う。

## 前提条件

kakutey CLI がインストールされ、アプリが起動している必要があります。

```bash
# インストール
npm install -g kakutey-cli

# 状態確認
kakutey health
```

## リソース

- **API 仕様**: [api_journals.md](references/api_journals.md)
- **CLI ヘルプ**: `kakutey journals --help`

## ワークフロー

### A. 仕訳の修正

1. **対象の仕訳を特定**（entity_id と revision を確認）
   ```bash
   kakutey journals list 2025-01-01 2025-01-31
   ```

2. **仕訳を修正**（フル更新、楽観ロック使用）
   ```bash
   kakutey journals update '{"entity_id":1,"date":"2025-01-15","description":"文房具購入（修正）","lines":[{"side":"debit","account":"消耗品費","amount":1500},{"side":"credit","account":"現金","amount":1500}],"evidence_ids":[],"expected_revision":1}'
   ```

### B. 証憑の紐付け

既存の仕訳に証憑 ID を追加する。

```bash
# 仕訳 ID 1 に証憑 ID 10, 20 を紐付け
kakutey journals attach 1 10 20
```

### C. 仕訳の削除

```bash
kakutey journals delete 1
```

## CLI コマンド一覧

| コマンド | 説明 |
|---------|------|
| `kakutey journals list <start> <end>` | 仕訳一覧（entity_id 確認用） |
| `kakutey journals update '<json>'` | 仕訳を更新（フル更新モード、楽観ロック） |
| `kakutey journals attach <journal_id> <evidence_id...>` | 仕訳に証憑を紐付け |
| `kakutey journals delete <id>` | 仕訳を削除（論理削除） |

## 関連スキル

- **kakutey-bookkeeping**: 仕訳の entity_id 確認、修正後の再確認
- **kakutey-evidence**: 紐付けする証憑の entity_id 確認
