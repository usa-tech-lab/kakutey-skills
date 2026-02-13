---
name: tax-workspace-setup
description: Scaffold the annual tax filing workspace folder structure for a given fiscal year. Creates evidence, processing, and tax-return directories.
---
# 年度別作業フォルダの生成

指定した年度の確定申告作業用フォルダ構造を生成する。年1回の一括作業を開始する前に実行する。

## 使い方

```bash
python3 scripts/scaffold.py <年度> [ベースディレクトリ]
```

- `<年度>`: 対象年度（例: `2025`）
- `[ベースディレクトリ]`: フォルダを作成する場所（省略時: カレントディレクトリ）

### 例

```bash
# カレントディレクトリに 2025/ を生成
python3 scripts/scaffold.py 2025

# 指定パスに生成
python3 scripts/scaffold.py 2025 /path/to/workspace
```

## 生成されるフォルダ構造

```
{year}/
├── 証憑/                              ← 証憑ファイルの格納場所
│   ├── 01_弊社から顧客への請求書/      ← 売上に関する請求書
│   ├── 02_業者から弊社への請求書・領収書/ ← 経費の請求書・領収書
│   ├── 03_銀行口座/                    ← 銀行口座の取引明細・スクリーンショット
│   ├── 04_クレジットカード/            ← クレジットカード利用明細
│   │   └── csv/                       ← カード会社からの CSV エクスポート
│   └── 05_paypay/                     ← PayPay 等の電子決済取引データ
├── 処理/                              ← 書き起こし・仕訳データの格納場所
└── 確定申告/                          ← e-Tax 画面ごとの入力値マークダウン
```

## 次のステップ

1. `証憑/` の各サブフォルダに証憑ファイルを配置する
2. `evidence-processing` スキルに従って `処理/` に書き起こし・仕訳データを生成する
3. `kakutey-bookkeeping` で仕訳を kakutey に登録する
4. `kakutey-evidence` で証憑を kakutey にアップロードする
5. `tax-return-prep` スキルに従って `確定申告/` に入力値マークダウンを生成する

## 冪等性

既にフォルダが存在する場合はスキップされる。既存ファイルを上書き・削除することはない。
