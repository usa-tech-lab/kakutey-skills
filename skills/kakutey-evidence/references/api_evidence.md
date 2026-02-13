# Evidence API リファレンス

Base URL: `http://localhost:8000/api`

## POST /api/evidence

証憑ファイルをアップロードする。

**Request:** `multipart/form-data`
- `file`: アップロードファイル（必須）
- `display_name`: 表示名（必須）

**対応ファイル形式:** PDF, JPEG, PNG, CSV, XLSX

**Response:** `EvidenceRead`
```json
{
  "entity_id": 1,
  "revision": 1,
  "file_id": "a1b2c3d4-uuid.pdf",
  "display_name": "領収書 サンプル商事 2025-01",
  "file_type": "application/pdf",
  "tags": [],
  "linked_journals": []
}
```

## GET /api/evidence/search

証憑を検索する。

**Query Parameters:**
- `display_name` (任意): 表示名の部分一致
- `tag` (任意): タグ名で絞り込み

**Response:** `List[EvidenceRead]`

## GET /api/evidence/{eid}

証憑の詳細を取得する。

**Response:** `EvidenceRead`（`linked_journals` に紐付き仕訳の情報を含む）

## PUT /api/evidence/{eid}

証憑のメタデータを更新する。

**Request Body:**
```json
{"display_name": "新しい表示名"}
```

**Response:** `EvidenceRead`（新しいリビジョンが作成される）

## DELETE /api/evidence/{eid}

証憑を削除する（ソフトデリート）。

**Response:** `{"ok": true}`

## GET /api/evidence/{eid}/file

証憑の原本ファイルをダウンロードする。

## GET /api/evidence/{eid}/thumbnail

サムネイル画像を取得する（200x200 JPEG）。

## GET /api/evidence/{eid}/preview

PDF 形式でプレビューする。画像・CSV・XLSX は自動的に PDF に変換される。

## GET /api/journals/{eid}/evidence/preview

仕訳に紐付く全証憑を結合した PDF を取得する。

## タグ管理

### GET /api/tags

全タグ名一覧を取得する。

**Response:** `["交通費", "会議費", ...]`

### POST /api/evidence/{eid}/tags

証憑にタグを追加する。

**Request Body:**
```json
{"tag_name": "交通費"}
```

**Response:** `EvidenceRead`（新しいリビジョンが作成される）
