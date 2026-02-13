# Reports API リファレンス

Base URL: `http://localhost:8000/api`

## 財務諸表

### GET /api/financial-statements/pl/{year}

損益計算書（P/L）を取得する。

**Response:**
```json
{
  "year": 2025,
  "items": [
    {
      "account_id": 100,
      "account_name": "売上高",
      "amount": 5000000,
      "is_abstract": false,
      "is_total": false,
      "relative_depth": 0
    }
  ],
  "net_income": 1000000
}
```

- `is_abstract`: 集約科目（見出し行）
- `is_total`: 小計行
- `relative_depth`: インデントレベル

### GET /api/financial-statements/bs/{year}

貸借対照表（B/S）を取得する。

**Response:**
```json
{
  "year": 2025,
  "sections": [
    {
      "category": "asset",
      "items": [
        {"account_id": 10, "account_name": "現金", "amount": 500000, "is_abstract": false, "is_total": false, "relative_depth": 0}
      ]
    },
    {"category": "liability", "items": [...]},
    {"category": "equity", "items": [...]}
  ],
  "net_income": 1000000,
  "is_balanced": true
}
```

- `category`: asset / liability / equity
- `is_balanced`: 貸借一致の検証結果

## 元帳

### GET /api/ledgers/cash

現金出納帳（指定勘定科目の元帳）を取得する。

**Query Parameters:**
- `account_id` (必須): 勘定科目の entity_id
- `start_date` (任意): 開始日
- `end_date` (任意): 終了日

**Response:**
```json
{
  "account_name": "現金",
  "lines": [
    {"date": "2025-01-15", "description": "文房具購入", "debit": 0, "credit": 1000, "balance": 49000}
  ],
  "total_debit": 50000,
  "total_credit": 1000,
  "balance": 49000,
  "opening_balance": 0
}
```

### GET /api/ledgers/general

総勘定元帳（全科目）を取得する。

**Query Parameters:** `start_date`, `end_date`（任意）

### GET /api/ledgers/expense

経費帳（費用科目のみ）を取得する。

**Query Parameters:** `start_date`, `end_date`（任意）

**Response:**
```json
{
  "groups": [
    {
      "account_name": "旅費交通費",
      "total_amount": 50000,
      "lines": [
        {"date": "2025-01-15", "description": "電車代", "debit": 1000, "credit": 0, "balance": 1000}
      ]
    }
  ],
  "grand_total": 50000
}
```

## 固定資産

### GET /api/fixed-assets

固定資産一覧を取得する。

**Response:**
```json
[
  {
    "entity_id": 1,
    "name": "業務用PC",
    "acquisition_date": "2025-06-01",
    "acquisition_cost": 200000,
    "useful_life": 4,
    "depreciation_method": "straight_line",
    "purchase_journal_entity_id": 10,
    "depreciation_journals": [
      {"journal_entity_id": 50, "date": "2025-12-31", "description": "減価償却費", "amount": 25000}
    ]
  }
]
```

- `depreciation_method`: `"straight_line"`（定額法）/ `"declining_balance"`（定率法）

### GET /api/fixed-assets/{eid}/depreciation?target_year={year}

指定年度の減価償却を計算する。

**Response:**
```json
{
  "fixed_asset_id": 1,
  "target_year": 2025,
  "depreciation_expense": 25000,
  "accumulated_depreciation": 25000,
  "book_value": 175000
}
```

### GET /api/fixed-assets/candidates

固定資産として登録可能な仕訳（資産勘定への借方 10万円以上）を検索する。

### POST /api/fixed-assets

固定資産を登録する。

```json
{
  "name": "業務用PC",
  "acquisition_date": "2025-06-01",
  "acquisition_cost": 200000,
  "useful_life": 4,
  "depreciation_method": "straight_line",
  "purchase_journal_entity_id": 10
}
```

## 関連エンドポイント

### GET /api/fiscal-year

会計年度情報を取得する。

### POST /api/closing/{year}/execute

年度末の決算処理を実行する。翌年度の開始残高が作成される。

### POST /api/closing/{year}/reopen

決算済み年度を再開する。

### POST /api/export/execute

帳簿データをエクスポートする。
