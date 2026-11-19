"""Read-only Brokermint API helper.

The API key is read from the macOS Keychain (service "brokermint", account "api")
at runtime. It is never printed, logged or written to disk.
"""
import json
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://my.brokermint.com/api"


def _api_key():
    try:
        out = subprocess.run(
            ["security", "find-generic-password", "-s", "brokermint", "-a", "api", "-w"],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError:
        sys.exit("No Brokermint key in Keychain (service 'brokermint', account 'api').")
    key = out.stdout.strip()
    if not key:
        sys.exit("Keychain entry 'brokermint' is empty.")
    return key


_KEY = None


def get(path, **params):
    """GET a Brokermint endpoint. Only GET is ever used here."""
    global _KEY
    if _KEY is None:
        _KEY = _api_key()
    params = {k: v for k, v in params.items() if v is not None}
    query = urllib.parse.urlencode({**params, "api_key": _KEY})
    req = urllib.request.Request(f"{BASE_URL}{path}?{query}", method="GET")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 4:
                time.sleep(2 ** attempt * 2)
                continue
            # Never echo the URL: it contains the key.
            body = e.read().decode("utf-8", "replace")[:300].replace(_KEY, "[redacted]")
            raise RuntimeError(f"GET {path} failed: HTTP {e.code} {body}") from None
        except urllib.error.URLError as e:
            raise RuntimeError(f"GET {path} failed: {e.reason}") from None


def list_all(path, page_size=1000, **params):
    """Page through a list endpoint using starting_from_id."""
    rows, start = [], None
    while True:
        page = get(path, count=page_size, starting_from_id=start, **params)
        if isinstance(page, dict):
            page = page.get("data") or page.get("items") or []
        if not page:
            break
        new = [r for r in page if not rows or r.get("id") != rows[-1].get("id")]
        rows.extend(new)
        if len(page) < page_size or not new:
            break
        start = max(r["id"] for r in page) + 1
    return rows
