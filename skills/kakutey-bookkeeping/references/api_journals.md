# Journal API リファレンス

Base URL: `http://localhost:8000/api`

## POST /api/journals

仕訳を1件登録する。複合仕訳（3行以上）にも対応。

**Request Body:**
```json
{
  "date": "2025-01-15",
  "description": "サンプル商事 交通費",
  "lines": [
    {"side": "debit", "account_id": 100, "amount": 1000},
    {"side": "credit", "account_id": 200, "amount": 1000}
  ],
  "evidence_ids": [10, 20]
}
```

- `lines`: 借方(debit)と貸方(credit)の合計は一致する必要がある
- `evidence_ids`: 任意。登録済み証憑の entity_id リスト

**Response:** `JournalRead`
```json
{
  "id": 1,
  "entity_id": 1,
  "revision": 1,
  "journal_date": "2025-01-15",
  "description": "サンプル商事 交通費",
  "lines": [
    {"id": 1, "side": "debit", "account_id": 100, "amount": 1000},
    {"id": 2, "side": "credit", "account_id": 200, "amount": 1000}
  ],
  "evidence_ids": [10, 20],
  "created_at": "2025-01-15T10:00:00",
  "deleted_at": null
}
```

## GET /api/journals

仕訳一覧を取得する（最新リビジョン、削除済み除外）。

**Query Parameters:**
- `start_date` (任意): 開始日 (YYYY-MM-DD)
- `end_date` (任意): 終了日 (YYYY-MM-DD)

**Response:** `List[JournalRead]`

## PUT /api/journals/{eid}

仕訳を更新する。楽観的ロック（`expected_revision`）を使用。

**Request Body:**
```json
{
  "date": "2025-01-15",
  "description": "サンプル商事 交通費（修正）",
  "lines": [
    {"side": "debit", "account_id": 100, "amount": 1500},
    {"side": "credit", "account_id": 200, "amount": 1500}
  ],
  "evidence_ids": [10],
  "expected_revision": 1
}
```

- `expected_revision`: 現在のリビジョンと一致しない場合は **409 Conflict** を返す
- 更新成功時は新しいリビジョン（revision + 1）が作成される

## DELETE /api/journals/{eid}

仕訳を削除する（ソフトデリート）。

**Response:** `{"ok": true}`

- 固定資産の購入仕訳・償却仕訳として紐付いている場合は削除不可
- 対象年度の会計期間が閉じている場合は削除不可

## GET /api/journals/{eid}/history

仕訳の全リビジョン履歴を取得する。

**Response:** `List[JournalRead]`

## POST /api/journals/{eid}/restore

指定リビジョンから仕訳を復元する。

**Request Body:**
```json
{"revision": 2}
```

## 関連エンドポイント

### GET /api/accounts

勘定科目一覧を取得。仕訳登録時の `account_id` 解決に使用。

```json
[
  {
    "entity_id": 100,
    "code": "1001",
    "name": "現金",
    "category": "asset",
    "is_abstract": 0
  }
]
```

`category`: asset / liability / equity / revenue / expense

### POST /api/accounts

勘定科目を新規作成。

```json
{
  "code": "5099",
  "name": "雑費",
  "category": "expense",
  "display_order": 999,
  "parent_entity_id": null,
  "is_abstract": 0
}
```
