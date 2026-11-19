"""One small read-only call per endpoint. Prints field names and types only, no values."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import bm  # noqa: E402


def shape(obj, depth=0):
    if isinstance(obj, dict):
        return {k: shape(v, depth + 1) if depth < 1 else type(v).__name__ for k, v in obj.items()}
    if isinstance(obj, list):
        return [shape(obj[0], depth)] if obj else []
    return type(obj).__name__


for label, path in [("users", "/v1/users"), ("transactions", "/v2/transactions")]:
    data = bm.get(path, count=1)
    rows = data if isinstance(data, list) else data.get("data", data)
    print(f"{label}: OK, got {len(rows) if isinstance(rows, list) else 1} row")
    if isinstance(rows, list) and rows:
        print(f"  fields: {shape(rows[0])}")

txs = bm.get("/v2/transactions", count=1, statuses="closed")
if txs:
    tid = txs[0]["id"]
    for label, path in [("transaction detail", f"/v2/transactions/{tid}"),
                        ("commissions", f"/v1/transactions/{tid}/commissions"),
                        ("participants", f"/v1/transactions/{tid}/participants")]:
        d = bm.get(path)
        print(f"{label}: OK")
        print(f"  fields: {shape(d[0] if isinstance(d, list) and d else d)}")
