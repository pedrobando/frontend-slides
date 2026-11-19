"""Pull users and 2025-2026 transactions (with detail, commissions, participants)
into private/brokermint-cache/. Read-only GET calls only.

Usage: python3 -I tools/brokermint/fetch.py [--refresh]
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bm  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CACHE = os.path.join(ROOT, "private", "brokermint-cache")
SINCE = "2025-01-01"


def save(name, data):
    os.makedirs(CACHE, exist_ok=True)
    with open(os.path.join(CACHE, name), "w") as f:
        json.dump(data, f)


def main():
    refresh = "--refresh" in sys.argv
    users = bm.list_all("/v1/users")
    save("users.json", users)
    print(f"users: {len(users)}")

    # Closed since Jan 2025, plus everything not closed (pending, listing, cancelled)
    closed = bm.list_all("/v2/transactions", statuses="closed", closed_since=SINCE)
    other = bm.list_all("/v2/transactions", statuses="pending,listing,cancelled",
                        updated_since=SINCE)
    seen, txs = set(), []
    for t in closed + other:
        if t["id"] not in seen:
            seen.add(t["id"])
            txs.append(t)
    print(f"transactions: {len(closed)} closed since {SINCE}, {len(other)} other")

    detail_path = os.path.join(CACHE, "details.json")
    details = {}
    if os.path.exists(detail_path) and not refresh:
        with open(detail_path) as f:
            details = json.load(f)
    todo = [t["id"] for t in txs if str(t["id"]) not in details]
    for i, tid in enumerate(todo, 1):
        details[str(tid)] = {
            "detail": bm.get(f"/v2/transactions/{tid}"),
            "commissions": bm.get(f"/v1/transactions/{tid}/commissions"),
            "participants": bm.get(f"/v1/transactions/{tid}/participants"),
        }
        if i % 25 == 0:
            save("details.json", details)
            print(f"  fetched {i}/{len(todo)}")
        time.sleep(0.15)
    save("details.json", details)
    save("fetched_at.json", {"fetched_at": time.strftime("%Y-%m-%d %H:%M")})
    print(f"details cached: {len(details)}")


if __name__ == "__main__":
    main()
