---
name: blue-return-sales-detail
description: Calculate input values for the Blue Return Sales Detail by Customer (売上（収入）金額の明細の入力) page.
---

# 売上（収入）金額の明細の入力値算出

指定された年度の会計データから、国税庁 確定申告作成コーナー「売上（収入）金額の明細の入力」画面の入力値を算出して Markdown 形式で出力する。

## 前提

- 対象年度の売上データ（取引先別の内訳が判別可能な形式）が利用可能であること
- 取引先の詳細情報は [customers.json](references/customers.json) を参照すること
- customers.json に登録されていない取引先や、所在地・登録番号が不足している場合はユーザーに確認すること

## 出力項目

### 取引先ごとの明細

各取引先について以下を出力する:

| 項目 | 説明 |
|------|------|
| 売上先名 | 取引先の正式名称 |
| 所在地 | 郵便番号＋住所 |
| 登録番号 | インボイス制度の適格請求書発行事業者登録番号（T + 13桁） |
| 売上金額 | その取引先への年間売上合計 |

### 合計

- 全取引先の売上金額合計（blue-return-income-statement の売上金額と一致すること）

## 出力形式

Markdown。取引先ごとにブロック分け。最後に合計の検算を記載。
