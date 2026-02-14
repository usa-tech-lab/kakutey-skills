---
name: evidence-processing
description: Process evidence files (receipts, invoices, statements) into structured markdown transcriptions and journal entry JSON. Covers the workflow from raw evidence to bookkeeping-ready data.
---
# 証憑の処理と仕訳データ生成

`証憑/` に配置された各種証憑ファイル（請求書、領収書、銀行明細、クレカ明細等）を読み取り、`処理/` に書き起こしマークダウンと仕訳データ JSON を生成するワークフロー。

## 前提

- `tax-workspace-setup` スキルでフォルダ構造を生成済みであること
- `証憑/` の各サブフォルダに証憑ファイルが配置済みであること
- 画像・PDF の読み取りには `image-describer` スキルを使用できること

## ワークフロー概要

詳細は [processing_workflow.md](references/processing_workflow.md) を参照。

1. **明細の書き起こし** (01-03): クレカ CSV、電子決済 CSV、銀行口座明細 → MD テーブル
2. **売上請求書の整理** (04): 請求書 PDF → 取引先・金額・日付の MD テーブル
3. **経費証憑の書き起こし** (05a-05d): サブスク請求書・Amazon・その他領収書 → MD
4. **仕訳対象の一覧化** (06): 全書き起こしから仕訳対象事象を1つの MD に集約
5. **仕訳データの生成** (07): 仕訳一覧 MD → 仕訳データ JSON

## 出力ファイル

| ファイル | 内容 |
|----------|------|
| `01_クレジットカード明細.md` | クレカ利用明細の書き起こし |
| `02_電子決済明細.md` | PayPay 等の取引明細 |
| `03_銀行口座明細.md` | 銀行口座の取引明細 |
| `04_売上請求書.md` | 売上請求書の一覧 |
| `05a_サブスク経費.md` | サブスクリプション請求書の OCR |
| `05b_amazon経費.md` | Amazon 注文履歴 |
| `05c_その他領収書.md` | その他領収書の OCR |
| `05d_その他経費.md` | その他の経費 |
| `06_仕訳対象事象一覧.md` | 全仕訳対象事象のカテゴリ別一覧 |
| `07_仕訳一覧.md` | 仕訳一覧テーブル（勘定科目一覧 + 仕訳テーブル） |
| `07_仕訳データ.json` | kakutey API 用の仕訳 JSON データ |

フォーマット仕様:
- [output_format_md.md](references/output_format_md.md) — マークダウンファイルの形式
- [output_format_json.md](references/output_format_json.md) — 仕訳 JSON の形式

## スクリプト

### md_to_json.py — 仕訳一覧 MD → 仕訳データ JSON 変換

```bash
python scripts/md_to_json.py <処理/07_仕訳一覧.md のパス>
```

`07_仕訳一覧.md` を読み取り、同ディレクトリに `07_仕訳データ.json` を出力する。

## 次のステップ

1. `kakutey journals bulk-add 07_仕訳データ.json` で仕訳を kakutey に一括登録
2. `kakutey evidence upload <ファイルパス>` で証憑ファイルを kakutey にアップロード
3. `kakutey journals attach` で仕訳と証憑の紐付けを実施
