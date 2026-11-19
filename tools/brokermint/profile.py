"""Shape of the cached data: counts and category values only, no names or dollar figures."""
import json
import os
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CACHE = os.path.join(ROOT, "private", "brokermint-cache")
users = json.load(open(os.path.join(CACHE, "users.json")))
details = json.load(open(os.path.join(CACHE, "details.json")))

c = {k: Counter() for k in ["role", "type", "active", "status", "repr", "state", "lead",
                            "buy_rep_type", "list_rep_type", "item_type", "item_name",
                            "payee_type", "side", "part_role", "owner_count", "has_close",
                            "close_year", "tx_type", "prop"]}
for u in users:
    c["role"][u.get("role")] += 1
    c["type"][u.get("type")] += 1
    c["active"][(u.get("active"), u.get("account_user_active"))] += 1
for d in details.values():
    t = d["detail"]
    c["status"][t.get("status")] += 1
    c["repr"][t.get("representing")] += 1
    c["state"][t.get("state")] += 1
    c["lead"][t.get("Lead source")] += 1
    c["tx_type"][t.get("transaction_type")] += 1
    c["prop"][t.get("Property type")] += 1
    c["buy_rep_type"][(t.get("buying_side_representer") or {}).get("type")] += 1
    c["list_rep_type"][(t.get("listing_side_representer") or {}).get("type")] += 1
    c["has_close"][(t.get("status"), bool(t.get("closing_date")))] += 1
    if t.get("closing_date"):
        import time
        c["close_year"][(t.get("status"), time.gmtime(t["closing_date"] / 1000).tm_year)] += 1
    for it in d["commissions"] or []:
        c["item_type"][it.get("item_type")] += 1
        c["item_name"][it.get("name")] += 1
        c["payee_type"][(it.get("payee_type"), it.get("payer_type"))] += 1
        c["side"][it.get("side")] += 1
    parts = d["participants"] or []
    c["part_role"].update(p.get("role") for p in parts)
    c["owner_count"][sum(1 for p in parts if p.get("owner"))] += 1
    # does buying/listing representer id match a participant id or user_id?
    for k in ["buying_side_representer", "listing_side_representer"]:
        r = t.get(k)
        if r and r.get("type") == "User":
            ids = {p.get("id") for p in parts}
            uids = {p.get("user_id") for p in parts}
            c.setdefault("rep_match", Counter())[(r["id"] in ids, r["id"] in uids)] += 1

for k, v in c.items():
    print(f"{k}: {v.most_common(25)}")
