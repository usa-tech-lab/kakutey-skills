# 仕訳データ JSON フォーマット仕様

## ファイル

- ファイル名: `07_仕訳データ.json`
- 配置先: `処理/` ディレクトリ
- 生成方法: `md_to_json.py` で `07_仕訳一覧.md` から自動変換

## JSON 構造

```json
[
  {
    "date": "YYYY-MM-DD",
    "description": "摘要テキスト",
    "lines": [
      { "side": "debit", "account_id": 12345, "amount": 50000 },
      { "side": "credit", "account_id": 67890, "amount": 50000 }
    ]
  }
]
```

### フィールド定義

| フィールド | 型 | 説明 |
|-----------|------|------|
| `date` | string | 仕訳日（ISO 8601 形式: `YYYY-MM-DD`） |
| `description` | string | 摘要（取引内容の説明） |
| `lines` | array | 仕訳明細行の配列 |
| `lines[].side` | string | `"debit"`（借方）または `"credit"`（貸方） |
| `lines[].account_id` | integer | kakutey の勘定科目 entity_id |
| `lines[].amount` | integer | 金額（円、整数） |

### 整合性ルール

- 各仕訳の借方合計 = 貸方合計（貸借一致）
- 配列は日付の昇順でソート済み

## 単一仕訳の例

CC 経費（借方1行・貸方1行）:

```json
{
  "date": "2025-01-01",
  "description": "CC サンプルクラウドサービス",
  "lines": [
    { "side": "debit", "account_id": 15338, "amount": 5000 },
    { "side": "credit", "account_id": 20593, "amount": 5000 }
  ]
}
```

## 複合仕訳の例

開始仕訳（借方3行・貸方2行）:

```json
{
  "date": "2025-01-01",
  "description": "開始仕訳（前年度末残高の引継ぎ）",
  "lines": [
    { "side": "debit", "account_id": 20006, "amount": 50000 },
    { "side": "debit", "account_id": 20007, "amount": 600000 },
    { "side": "credit", "account_id": 20592, "amount": 640000 },
    { "side": "credit", "account_id": 10414, "amount": 10000 }
  ]
}
```

## kakutey への登録

生成された JSON は `kakutey-bookkeeping` スキルの `bulk_add_journals.py` で kakutey に一括登録できる:

```bash
python bulk_add_journals.py 07_仕訳データ.json
```

`bulk_add_journals.py` は `account_id` をそのまま使用して API にリクエストする。
