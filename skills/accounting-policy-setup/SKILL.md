---
name: accounting-policy-setup
description: Define or update the accounting policy for a fiscal year. Creates a structured accounting-policy.md that governs how other kakutey skills process journal entries and financial statements.
---

# 会計方針の定義・更新

税理士・会計士・経理担当者が対話的に会計方針を定義し、ワークスペースに `accounting-policy.md` を生成する。

## 概要

このスキルは**メタスキル**である。他のスキル（evidence-processing, kakutey-reports 等）が参照する会計方針ファイルを生成・更新する。

## ワークフロー

### A. 新規作成（対話モード）

[template.md](references/template.md) をベースに、以下の順序でユーザーに確認しながら会計方針を定義する。

#### Step 1: 事業者情報

- 事業形態（個人事業主 / 法人）
- 屋号・事業者名
- インボイス登録番号
- 申告種別（青色申告 / 白色申告）
- 青色申告特別控除額（65万円 / 55万円 / 10万円）
- 会計期間（個人事業主は通常 1月〜12月）
- 課税事業者 / 免税事業者

#### Step 2: 仕訳ルール

- 会計基準: 現金主義 / 発生主義
- 事業用銀行口座の有無
- クレジットカード経費の処理方法:
  - 簡便法（利用日に直接計上、事業主借）
  - 未払金方式（利用日に未払金計上、引落日に消込）
- 売上の計上タイミング（請求日 / 納品日 / 入金日）
- 入金時の処理（事業主貸 / 普通預金）
- 電子決済・口座振替の処理方法

#### Step 3: 常用勘定科目

- 現金、売掛金、事業主貸/借、元入金 等の勘定科目名を確認
- カスタム勘定科目の追加

#### Step 4: 減価償却方法

- デフォルトの償却方法（定額法 / 定率法）
- 資産種類別の例外設定（任意）

#### Step 5: 消費税区分

- 非課税科目のリスト
- 事業固有の非課税理由
- 軽減税率対象の確認
- 標準税率科目の補足

#### Step 6: 貸借対照表の処理方針

- 事業主貸・事業主借の決算時の取扱い
- 元入金の取扱い

#### Step 7: 顧客情報

- 主要取引先の正式名称、インボイス番号、住所
- 仕訳での照合パターン

#### Step 8: 按分ルール（任意）

- 家事按分の対象科目と按分率

### B. 既存ファイルの更新

既存の `accounting-policy.md` を読み込み、ユーザーの指示に従って特定セクションを更新する。

### C. 前年度からの引き継ぎ

前年度の `accounting-policy.md` をコピーし、年度固有の変更（新規顧客追加、控除額変更等）のみを反映する。

## 出力

`{year}/accounting-policy.md` を生成する。テンプレートは [template.md](references/template.md) を参照。
