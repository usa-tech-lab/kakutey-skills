import requests

API_BASE = "http://localhost:8000/api"


def request(method, path, data=None, params=None):
    url = f"{API_BASE}{path}"
    resp = requests.request(method, url, json=data, params=params)
    if not resp.ok:
        detail = resp.text[:500] if resp.content else resp.reason
        raise RuntimeError(f"API {method.upper()} {path} → {resp.status_code}: {detail}")
    return resp.json()


def upload(path, file_path, display_name=None):
    import mimetypes
    import os

    if not display_name:
        display_name = os.path.basename(file_path)
    content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    url = f"{API_BASE}{path}"
    with open(file_path, "rb") as f:
        resp = requests.post(
            url,
            files={"file": (os.path.basename(file_path), f, content_type)},
            data={"display_name": display_name},
        )
    if not resp.ok:
        detail = resp.text[:500] if resp.content else resp.reason
        raise RuntimeError(f"API POST {path} → {resp.status_code}: {detail}")
    return resp.json()
