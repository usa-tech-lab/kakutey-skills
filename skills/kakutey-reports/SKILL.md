---
name: kakutey-reports
description: Retrieve financial statements (P/L, B/S) and fixed asset / depreciation data from the kakutey bookkeeping app. Use for year-end closing review and tax filing preparation.
---

# kakutey-reports

kakutey の決算確認ワークフローを支援するスキル。P/L（損益計算書）、B/S（貸借対照表）、固定資産・減価償却情報を取得・表示する。

## リソース

- **API 仕様**: [api_reports.md](references/api_reports.md)
- **事業主情報**: [business_profile.json](references/business_profile.json)（常用する勘定科目等を記載）

## スクリプト実行方法

すべてのスクリプトは `scripts/` ディレクトリから `uv run` で実行する。

## ワークフロー

### A. 決算確認

1. **損益計算書と貸借対照表を確認**
   ```bash
   uv run scripts/get_summary.py 2025              # P/L + B/S 両方
   uv run scripts/get_summary.py 2025 --type pl     # P/L のみ
   uv run scripts/get_summary.py 2025 --type bs     # B/S のみ
   ```

2. **固定資産と減価償却を確認**
   ```bash
   uv run scripts/get_fixed_assets.py                     # 資産一覧
   uv run scripts/get_fixed_assets.py --depreciation 2025  # 償却計算付き
   ```

3. 確認結果に基づき、必要に応じて仕訳を修正（kakutey-corrections を使用）

## スクリプト一覧

| スクリプト | 説明 |
|-----------|------|
| `get_summary.py` | 損益計算書（P/L）・貸借対照表（B/S）を表示 |
| `get_fixed_assets.py` | 固定資産一覧と減価償却計算 |

## 関連スキル

- **kakutey-corrections**: 決算確認で発見した仕訳の修正・削除
- **kakutey-bookkeeping**: 不足する仕訳の追加登録
