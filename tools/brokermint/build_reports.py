"""Build one bilingual PDF per agent, office summaries and a gaps summary from
private/brokermint-cache/. Run fetch.py first.

Usage: python3 -I tools/brokermint/build_reports.py [--as-of YYYY-MM-DD] [--only "Agent Name"]
"""
import datetime as dt
import html
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CACHE = os.path.join(ROOT, "private", "brokermint-cache")
OUT = os.path.join(ROOT, "private", "agent-reports")
FONTS = "file://" + os.path.join(ROOT, "presentations", "fonts")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
AGENT_ROLES = {"agent", "team leader", "owner"}
OFFICE_NAMES = {"WI": "Milwaukee, WI", "FL": "Florida"}
ALL_NAME = "All offices"

args = sys.argv[1:]
AS_OF = dt.date.fromisoformat(args[args.index("--as-of") + 1]) if "--as-of" in args else dt.date.today()
ONLY = args[args.index("--only") + 1].lower() if "--only" in args else None
Y, PY = AS_OF.year, AS_OF.year - 1
YTD = (dt.date(Y, 1, 1), AS_OF)
PRIOR = (dt.date(PY, 1, 1), AS_OF.replace(year=PY))
PRIOR_FULL = (dt.date(PY, 1, 1), dt.date(PY, 12, 31))
YEAR_END = dt.date(Y, 12, 31)


def day(ms):
    return dt.datetime.utcfromtimestamp(ms / 1000).date() if ms else None


def within(d, rng):
    return d is not None and rng[0] <= d <= rng[1]


def lead_label(s):
    s = (s or "").strip()
    if not s:
        return "Not recorded"
    return {"is Family/Friend": "Family/Friend"}.get(s, s)


# ---------------------------------------------------------------- load + attribute
users = {u["id"]: u for u in json.load(open(os.path.join(CACHE, "users.json")))}
details = json.load(open(os.path.join(CACHE, "details.json")))

deals = []          # one row per transaction
credits = []        # one row per (transaction, side, agent)
gaps = defaultdict(list)

for x in details.values():
    t, items, parts = x["detail"], x["commissions"] or [], x["participants"] or []
    rep = (t.get("representing") or "").lower()
    sides = {"buyer": ["buying"], "seller": ["listing"], "both": ["buying", "listing"]}.get(rep, [])
    deal = {
        "id": t["id"], "status": t["status"], "price": t.get("price") or 0,
        "close": day(t.get("closing_date")), "accept": day(t.get("acceptance_date")),
        "updated": day(t.get("updated_at")), "state": (t.get("state") or "").upper(),
        "lead": lead_label(t.get("Lead source")), "tgc": t.get("total_gross_commission") or 0,
        "address": t.get("address") or "",
    }
    # cancelled deals without a closing date are dated by last update
    deal["date"] = deal["close"] or (deal["updated"] if deal["status"] == "cancelled" else None)
    deals.append(deal)

    def by(kind, side):
        out = defaultdict(float)
        for it in items:
            if it.get("item_type") == kind and it.get("side") == side and it.get("payee_type") == "User":
                out[it["payee_id"]] += it.get("calculated_dollar_amount") or 0
        return out

    attributed = False
    for side in sides:
        gci, vol, net = by("award_allocation", side), by("sales_volume", side), by("NET_COMMISSION", side)
        agents = set(gci) | set(vol)
        source = "split"
        if not agents:
            want = "buyer's agent" if side == "buying" else "listing agent"
            agents = {p["user_id"] for p in parts
                      if p.get("type") == "user" and (p.get("role") or "").lower() == want and p.get("user_id")}
            source = "participant"
        if not agents:
            continue
        attributed = True
        tv, tg = sum(vol.values()), sum(gci.values())
        for uid in agents:
            if tv > 0:
                share = vol.get(uid, 0) / tv
            elif tg > 0:
                share = gci.get(uid, 0) / tg
            else:
                share = 1 / len(agents)
            credits.append({
                "deal": deal, "side": side, "uid": uid, "credit": share,
                "gci": gci.get(uid, 0), "net": net.get(uid, 0),
                "vol": vol.get(uid, 0) if tv > 0 else deal["price"] * share,
                "source": source,
            })
    if not attributed:
        gaps["no_agent"].append(deal)

# ---------------------------------------------------------------- data gaps (deal level)
for d in deals:
    if d["status"] == "closed" and not d["close"]:
        gaps["closed_no_date"].append(d)
    if d["status"] == "pending":
        if not d["close"]:
            gaps["pending_no_date"].append(d)
        elif d["close"] < AS_OF:
            gaps["pending_past_due"].append(d)
    if d["status"] == "cancelled" and not d["close"] and within(d["date"], YTD):
        gaps["cancelled_no_date"].append(d)
    if d["status"] == "closed" and within(d["close"], YTD):
        if d["tgc"] == 0:
            gaps["closed_zero_gci"].append(d)
        if d["lead"] == "Not recorded":
            gaps["closed_no_lead"].append(d)
for c in credits:
    if c["source"] == "participant" and c["deal"]["status"] == "closed" and within(c["deal"]["close"], YTD):
        gaps["no_split"].append(c["deal"])


# ---------------------------------------------------------------- metrics
def summarize(rows):
    """rows: credit rows for one agent or office."""
    def closed_in(rng):
        return [r for r in rows if r["deal"]["status"] == "closed" and within(r["deal"]["close"], rng)]

    def core(sel):
        ds = {r["deal"]["id"]: r["deal"] for r in sel}
        dtc = [(d["close"] - d["accept"]).days for d in ds.values() if d["accept"] and d["close"] >= d["accept"]]
        return {
            "units": sum(r["credit"] for r in sel),
            "volume": sum(r["vol"] for r in sel),
            "gci": sum(r["gci"] for r in sel),
            "net": sum(r["net"] for r in sel),
            "buyer": sum(r["credit"] for r in sel if r["side"] == "buying"),
            "listing": sum(r["credit"] for r in sel if r["side"] == "listing"),
            "avg_price": (sum(d["price"] for d in ds.values()) / len(ds)) if ds else 0,
            "days": (sum(dtc) / len(dtc)) if dtc else None,
        }

    ytd, prior, prior_full = closed_in(YTD), closed_in(PRIOR), closed_in(PRIOR_FULL)
    pend = [r for r in rows if r["deal"]["status"] == "pending"]
    pend_ye = [r for r in pend if r["deal"]["close"] and AS_OF <= r["deal"]["close"] <= YEAR_END]
    canc = [r for r in rows if r["deal"]["status"] == "cancelled" and within(r["deal"]["date"], YTD)]
    canc_p = [r for r in rows if r["deal"]["status"] == "cancelled" and within(r["deal"]["date"], PRIOR)]
    listings = {r["deal"]["id"] for r in rows if r["deal"]["status"] == "listing"}

    lead = defaultdict(lambda: {"units": 0, "gci": 0, "units_p": 0, "gci_p": 0})
    for r in ytd:
        lead[r["deal"]["lead"]]["units"] += r["credit"]
        lead[r["deal"]["lead"]]["gci"] += r["gci"]
    for r in prior:
        lead[r["deal"]["lead"]]["units_p"] += r["credit"]
        lead[r["deal"]["lead"]]["gci_p"] += r["gci"]

    months = {"cur": [0] * 12, "pend": [0] * 12, "prev": [0] * 12, "gci_cur": [0] * 12, "gci_prev": [0] * 12}
    for r in rows:
        d = r["deal"]
        if d["status"] == "closed" and d["close"] and d["close"].year == Y and d["close"] <= AS_OF:
            months["cur"][d["close"].month - 1] += r["credit"]
            months["gci_cur"][d["close"].month - 1] += r["gci"]
        elif d["status"] == "closed" and d["close"] and d["close"].year == PY:
            months["prev"][d["close"].month - 1] += r["credit"]
            months["gci_prev"][d["close"].month - 1] += r["gci"]
        elif d["status"] == "pending" and d["close"] and AS_OF <= d["close"] <= YEAR_END:
            months["pend"][d["close"].month - 1] += r["credit"]

    return {
        "ytd": core(ytd), "prior": core(prior), "prior_full": core(prior_full),
        "pend_ye": core(pend_ye), "pending_all": core(pend),
        "pending_count": sum(r["credit"] for r in pend),
        "pending_past_due": sum(r["credit"] for r in pend if r["deal"]["close"] and r["deal"]["close"] < AS_OF),
        "cancelled": sum(r["credit"] for r in canc), "cancelled_p": sum(r["credit"] for r in canc_p),
        "listings": len(listings), "lead": dict(lead), "months": months,
        "deal_ids": {r["deal"]["id"] for r in rows},
    }


by_agent = defaultdict(list)
for c in credits:
    by_agent[c["uid"]].append(c)


def office_of(rows):
    cnt = Counter(r["deal"]["state"] for r in rows if r["deal"]["state"] in OFFICE_NAMES)
    return cnt.most_common(1)[0][0] if cnt else "WI"


def has_activity(rows, rng):
    return any(r["deal"]["status"] in ("closed", "pending", "cancelled", "listing")
               and (within(r["deal"]["date"], rng) or r["deal"]["status"] in ("pending", "listing"))
               for r in rows)


# Who gets a report: agent-type roles that are marked active or have activity this year
report_agents, skipped = [], []
for uid, u in users.items():
    role = (u.get("role") or "").lower()
    rows = by_agent.get(uid, [])
    active_now = has_activity(rows, YTD)
    if role in AGENT_ROLES and (u.get("active") or active_now):
        report_agents.append(uid)
    elif rows and has_activity(rows, (dt.date(PY, 1, 1), AS_OF)):
        skipped.append((u, role, active_now))
for uid in by_agent:
    if uid not in users:
        gaps["unknown_user"].append(uid)

# ---------------------------------------------------------------- formatting
def money(v):
    return "$" + f"{v:,.0f}" if v else "$0"


def num(v, digits=1):
    if v is None:
        return "n/a"
    return f"{v:,.0f}" if abs(v - round(v)) < 0.05 else f"{v:,.{digits}f}"


def change(cur, prev):
    if not prev:
        return "new" if cur else ""
    pct = (cur - prev) / prev * 100
    cls = "up" if pct > 0.5 else "down" if pct < -0.5 else ""
    return f'<span class="{cls}">{"+" if pct > 0 else ""}{pct:.0f}%</span>'


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def month_chart(m):
    W, H, pad_l, pad_b, top = 640, 170, 26, 34, 12
    peak = max([1] + [a + b for a, b in zip(m["cur"], m["pend"])] + m["prev"])
    step = max(1, round(peak / 4 + 0.49))
    ceil = step * ((peak + step - 0.001) // step) if peak > step else step * 2
    gw = (W - pad_l) / 12
    bw = gw * 0.32
    sy = (H - pad_b - top) / ceil
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Closings by month">']
    v = 0
    while v <= ceil + 0.001:
        y = H - pad_b - v * sy
        out.append(f'<line x1="{pad_l}" x2="{W}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>'
                   f'<text x="{pad_l - 6}" y="{y + 3:.1f}" class="ax" text-anchor="end">{num(v)}</text>')
        v += step
    for i in range(12):
        x0 = pad_l + i * gw + gw * 0.15
        hp = m["prev"][i] * sy
        out.append(f'<rect x="{x0:.1f}" y="{H - pad_b - hp:.1f}" width="{bw:.1f}" height="{hp:.1f}" rx="2" class="prev"/>')
        hc, hpe = m["cur"][i] * sy, m["pend"][i] * sy
        x1 = x0 + bw + 3
        out.append(f'<rect x="{x1:.1f}" y="{H - pad_b - hc:.1f}" width="{bw:.1f}" height="{hc:.1f}" rx="2" class="cur"/>')
        if hpe:
            out.append(f'<rect x="{x1:.1f}" y="{H - pad_b - hc - hpe:.1f}" width="{bw:.1f}" height="{hpe:.1f}" rx="2" class="pend"/>')
        cx = pad_l + i * gw + gw / 2
        out.append(f'<text x="{cx:.1f}" y="{H - pad_b + 14}" class="ax" text-anchor="middle">{MONTHS[i]}</text>'
                   f'<text x="{cx:.1f}" y="{H - pad_b + 26}" class="ax es" text-anchor="middle">{MESES[i]}</text>')
    out.append("</svg>")
    return "".join(out)


CSS = f"""
@font-face{{font-family:'Poppins';font-weight:500;src:url('{FONTS}/poppins-latin-500.woff2')}}
@font-face{{font-family:'Poppins';font-weight:600;src:url('{FONTS}/poppins-latin-600.woff2')}}
@font-face{{font-family:'Poppins';font-weight:700;src:url('{FONTS}/poppins-latin-700.woff2')}}
@font-face{{font-family:'Instrument Sans';font-weight:400;src:url('{FONTS}/instrument-sans-regular.woff2')}}
@font-face{{font-family:'Instrument Sans';font-weight:700;src:url('{FONTS}/instrument-sans-bold.woff2')}}
@font-face{{font-family:'Instrument Sans';font-style:italic;src:url('{FONTS}/instrument-sans-italic.woff2')}}
@page{{size:Letter;margin:0.45in 0.5in}}
:root{{--ink:#1B252F;--muted:#6E7A88;--line:#E3E0DA;--card:#F4F2EE;--brand:#034C76;--brand-l:#6BA8D6;
--sprout:#8CC94E;--sprout-d:#2C5E15;--clay:#C05445;--prev:#C9D3DC}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Instrument Sans',system-ui,sans-serif;color:var(--ink);font-size:9.6pt;line-height:1.35;background:#fff}}
.page{{page-break-after:always}}
.page:last-child{{page-break-after:auto}}
h1,h2,h3,.big{{font-family:'Poppins',system-ui,sans-serif}}
header{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid var(--brand);padding-bottom:8px;margin-bottom:12px}}
.eyebrow{{font-size:8pt;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
h1{{font-size:21pt;font-weight:700;line-height:1.1;color:var(--brand)}}
.meta{{text-align:right;font-size:8.4pt;color:var(--muted)}}
.private{{display:inline-block;background:var(--card);color:var(--clay);font-weight:700;font-size:7.6pt;padding:2px 7px;border-radius:3px;margin-bottom:4px;letter-spacing:.04em}}
h2{{font-size:11pt;font-weight:600;color:var(--brand);margin:12px 0 5px}}
h2 .es,.es{{font-family:'Instrument Sans',sans-serif;font-style:italic;font-weight:400;color:var(--muted)}}
h2 .es{{font-size:9pt;margin-left:6px}}
.es{{font-size:.92em}}
table{{width:100%;border-collapse:collapse}}
th{{text-align:right;font-size:7.6pt;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;padding:4px 6px;border-bottom:1px solid var(--ink)}}
th:first-child,td:first-child{{text-align:left}}
th .es{{display:block;text-transform:none;letter-spacing:0;font-weight:400}}
td{{text-align:right;padding:4px 6px;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}}
td .es{{display:block;font-size:8pt}}
td.hl{{font-weight:700;background:#EEF5FA}}
.up{{color:var(--sprout-d);font-weight:700}} .down{{color:var(--clay);font-weight:700}}
.cols{{display:grid;grid-template-columns:1.15fr 1fr;gap:18px}}
.tiles{{display:grid;grid-template-columns:1fr 1fr;gap:6px}}
.tile{{background:var(--card);border-radius:5px;padding:7px 9px}}
.tile .big{{font-size:14pt;font-weight:700;color:var(--ink);line-height:1.15}}
.tile .lbl{{font-size:7.8pt;color:var(--muted)}}
.chart{{width:100%;height:auto;display:block}}
.chart .grid{{stroke:var(--line);stroke-width:1}} .chart .ax{{font-size:9px;fill:var(--muted)}} .chart .ax.es{{font-style:italic;font-size:8px}}
.chart .prev{{fill:var(--prev)}} .chart .cur{{fill:var(--brand)}} .chart .pend{{fill:var(--brand-l)}}
.legend{{display:flex;gap:14px;font-size:8pt;color:var(--muted);margin-top:2px}}
.legend i{{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:4px;vertical-align:-1px}}
.note{{font-size:7.6pt;color:var(--muted);margin-top:10px;border-top:1px solid var(--line);padding-top:6px}}
.callout{{background:#EEF5FA;border-left:3px solid var(--brand);padding:6px 9px;font-size:8.6pt;margin-top:8px}}
.small td{{padding:3px 6px;font-size:8.6pt}}
"""


def bi(en, es):
    return f'{en}<span class="es">{es}</span>'


SCORE_ROWS = [
    ("units", "Closed units", "Unidades cerradas", num),
    ("volume", "Sales volume", "Volumen de ventas", money),
    ("gci", "GCI (your share)", "GCI (tu parte)", money),
    ("net", "Agent net", "Neto del agente", money),
    ("buyer", "Buyer sides", "Lados de comprador", num),
    ("listing", "Listing sides", "Lados de vendedor", num),
]


def scoreboard(s, office=False):
    head = (f"<tr><th>{bi('Metric', 'Métrica')}</th><th>{bi(f'{Y} YTD', f'{Y} a la fecha')}</th>"
            f"<th>{bi(f'+ pending to Dec 31', 'con pendientes al 31 dic')}</th>"
            f"<th>{bi(f'{PY} same period', f'{PY} mismo periodo')}</th><th>{bi('Change', 'Cambio')}</th>"
            f"<th>{bi(f'{PY} full year', f'{PY} año completo')}</th></tr>")
    body = ""
    for key, en, es, fmt in SCORE_ROWS:
        if office and key == "gci":
            en, es = "GCI (agent shares)", "GCI (partes de agentes)"
        cur, pe = s["ytd"][key], s["pend_ye"][key]
        body += (f"<tr><td>{en}<span class=\"es\">{es}</span></td><td class=\"hl\">{fmt(cur)}</td>"
                 f"<td>{fmt(cur + pe)}</td><td>{fmt(s['prior'][key])}</td>"
                 f"<td>{change(cur, s['prior'][key])}</td><td>{fmt(s['prior_full'][key])}</td></tr>")
    return f"<table>{head}{body}</table>"


def lead_table(s):
    rows = sorted(s["lead"].items(), key=lambda kv: (-kv[1]["gci"], -kv[1]["units"]))
    rows = [r for r in rows if r[1]["units"] or r[1]["units_p"]]
    if not rows:
        return '<p class="es" style="font-style:normal">No closings in either period. / Sin cierres en ningún periodo.</p>'
    head = (f"<tr><th>{bi('Source', 'Fuente')}</th><th>{bi(f'Units {Y}', f'Unidades {Y}')}</th>"
            f"<th>{bi(f'GCI {Y}', f'GCI {Y}')}</th><th>{bi(f'Units {PY}', f'Unidades {PY}')}</th></tr>")
    body = "".join(f"<tr><td>{html.escape(k)}</td><td>{num(v['units'])}</td><td>{money(v['gci'])}</td>"
                   f"<td>{num(v['units_p'])}</td></tr>" for k, v in rows)
    return f'<table class="small">{head}{body}</table>'


def tiles(s):
    fall = s["cancelled"] / (s["cancelled"] + s["ytd"]["units"]) * 100 if (s["cancelled"] + s["ytd"]["units"]) else 0
    t = [
        (num(s["pending_count"]), "Pending now", "Pendientes hoy"),
        (money(s["pending_all"]["gci"]), "Pending GCI", "GCI pendiente"),
        (num(s["cancelled"]), f"Cancelled in {Y}", f"Canceladas en {Y}"),
        (f"{fall:.0f}%", "Fall-through rate", "Tasa de caída"),
        (money(s["ytd"]["avg_price"]), "Avg. closed price", "Precio promedio"),
        (num(s["ytd"]["days"], 0) + (" days" if s["ytd"]["days"] is not None else ""),
         "Contract to close", "Contrato a cierre"),
        (num(s["listings"]), "Active listings", "Listados activos"),
        (num(s["prior"]["days"], 0) + (" days" if s["prior"]["days"] is not None else ""),
         f"Contract to close {PY}", f"Contrato a cierre {PY}"),
    ]
    return '<div class="tiles">' + "".join(
        f'<div class="tile"><div class="big">{a}</div><div class="lbl">{b} · <span class="es">{c}</span></div></div>'
        for a, b, c in t) + "</div>"


def footer(extra=""):
    return (f'<div class="note">Source: Brokermint, pulled {AS_OF:%b %-d, %Y}. Closings count by closing date. '
            f"Units and volume are your credited share when a deal is split. GCI is your share of gross commission before the company split; "
            f"agent net is after splits and fees. Same period means Jan 1 to {PRIOR[1]:%b %-d}, {PY}. {extra}<br>"
            f'<span class="es">Fuente: Brokermint, {AS_OF:%d/%m/%Y}. Los cierres cuentan por fecha de cierre. '
            f"GCI es tu parte de la comisión bruta antes del split; el neto es después de splits y cargos.</span></div>")


def agent_page(uid, s):
    u = users[uid]
    name = u.get("name") or f'{u.get("first_name", "")} {u.get("last_name", "")}'.strip()
    office = OFFICE_NAMES[office_of(by_agent.get(uid, []))]
    gap_note = ""
    if s["pending_past_due"]:
        gap_note = (f'<div class="callout">{num(s["pending_past_due"])} pending deal(s) show a closing date that has passed. '
                    f'Update them in Brokermint so they count. <span class="es">Actualiza en Brokermint las pendientes con fecha vencida.</span></div>')
    return f"""<section class="page">
<header><div><div class="private">PRIVATE · PRIVADO</div><div class="eyebrow">{Y} Look back · Mirada atrás · {office}</div>
<h1>{html.escape(name)}</h1></div>
<div class="meta">Jan 1 to {AS_OF:%b %-d, %Y}<br><span class="es">1 ene al {AS_OF.day} {MESES[AS_OF.month - 1]} {AS_OF.year}</span><br>2027 Agent Retreat</div></header>
<h2>Scoreboard<span class="es">Marcador</span></h2>
{scoreboard(s)}
<div class="callout">Copy the <b>{Y} YTD</b> column into <b>Actual</b> on workbook p.10. <span class="es">Copia la columna {Y} a la fecha en Real, página 10 del cuaderno.</span></div>
<h2>Closings by month<span class="es">Cierres por mes</span></h2>
{month_chart(s["months"])}
<div class="legend"><span><i style="background:var(--prev)"></i>{PY} closed · cerradas</span><span><i style="background:var(--brand)"></i>{Y} closed · cerradas</span><span><i style="background:var(--brand-l)"></i>{Y} pending · pendientes</span></div>
<div class="cols">
<div><h2>Where your business came from<span class="es">De dónde vino tu negocio</span></h2>{lead_table(s)}
<div class="callout">Use these rows on workbook p.11, then add what each source cost you. <span class="es">Usa estas filas en la página 11 y añade el costo de cada fuente.</span></div></div>
<div><h2>Pipeline and fallout<span class="es">Pendientes y caídas</span></h2>{tiles(s)}{gap_note}</div>
</div>
{footer()}
</section>"""


def office_page(code, agents_stats, s):
    rows = sorted(agents_stats, key=lambda a: -a[1]["ytd"]["gci"])
    head = (f"<tr><th>{bi('Agent', 'Agente')}</th><th>{bi('Units', 'Unidades')}</th><th>{bi('Volume', 'Volumen')}</th>"
            f"<th>GCI</th><th>{bi('Agent net', 'Neto')}</th><th>{bi(f'Units {PY}', f'Unid. {PY}')}</th>"
            f"<th>{bi('Pending', 'Pend.')}</th><th>{bi('Cancelled', 'Canc.')}</th></tr>")
    body = "".join(
        f"<tr><td>{html.escape(users[uid].get('name') or '')}</td><td>{num(a['ytd']['units'])}</td><td>{money(a['ytd']['volume'])}</td>"
        f"<td>{money(a['ytd']['gci'])}</td><td>{money(a['ytd']['net'])}</td><td>{num(a['prior']['units'])}</td>"
        f"<td>{num(a['pending_count'])}</td><td>{num(a['cancelled'])}</td></tr>" for uid, a in rows)
    return f"""<section class="page">
<header><div><div class="private">BROKER ONLY · SOLO BROKER</div><div class="eyebrow">{Y} Look back · Office summary</div>
<h1>{OFFICE_NAMES.get(code, ALL_NAME)}</h1></div><div class="meta">Jan 1 to {AS_OF:%b %-d, %Y}<br>{len(rows)} agents</div></header>
<h2>Scoreboard<span class="es">Marcador</span></h2>{scoreboard(s, office=True)}
<h2>Closings by month<span class="es">Cierres por mes</span></h2>{month_chart(s["months"])}
<div class="legend"><span><i style="background:var(--prev)"></i>{PY} closed</span><span><i style="background:var(--brand)"></i>{Y} closed</span><span><i style="background:var(--brand-l)"></i>{Y} pending</span></div>
</section><section class="page">
<h2>Agents, {Y} YTD<span class="es">Agentes, {Y} a la fecha</span></h2><table class="small">{head}{body}</table>
<div class="cols" style="margin-top:6px"><div><h2>Lead sources<span class="es">Fuentes</span></h2>{lead_table(s)}</div><div><h2>Pipeline and fallout</h2>{tiles(s)}</div></div>
{footer("Office totals count each deal once per side, so co-listed deals are not double counted.")}
</section>"""


def render(html_body, pdf_path):
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    html_path = pdf_path[:-4] + ".html"
    with open(html_path, "w") as f:
        f.write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Report</title><style>{CSS}</style></head><body>{html_body}</body></html>')
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=3000", f"--print-to-pdf={pdf_path}", "file://" + html_path],
                   check=True, capture_output=True)
    os.remove(html_path)


def slug(s):
    return "".join(ch if ch.isalnum() else "-" for ch in s).strip("-").replace("--", "-")


# ---------------------------------------------------------------- build
year_dir = os.path.join(OUT, str(Y))
office_agents = defaultdict(list)
totals = []
for uid in sorted(report_agents, key=lambda i: (users[i].get("last_name") or "", users[i].get("first_name") or "")):
    rows = by_agent.get(uid, [])
    s = summarize(rows)
    code = office_of(rows)
    office_agents[code].append((uid, s))
    u = users[uid]
    totals.append((u, code, s))
    if ONLY and ONLY not in (u.get("name") or "").lower():
        continue
    fname = slug(f'{u.get("last_name", "")}-{u.get("first_name", "")}') + ".pdf"
    render(agent_page(uid, s), os.path.join(year_dir, OFFICE_NAMES[code].split(",")[0], fname))

if not ONLY:
    for code, lst in office_agents.items():
        # office totals: every credit row whose deal is in that state, once per deal-side
        rows = [c for c in credits if (c["deal"]["state"] or "WI") == code]
        render(office_page(code, lst, summarize(rows)),
               os.path.join(year_dir, "_broker-only", f"office-summary-{code}.pdf"))
    render(office_page("ALL", [a for lst in office_agents.values() for a in lst], summarize(credits)),
           os.path.join(year_dir, "_broker-only", "office-summary-ALL.pdf"))

# ---------------------------------------------------------------- summary.md
def deal_line(d):
    return f'- #{d["id"]} {d["address"]} ({d["status"]}, closing date {d["close"] or "none"})'


all_rows = credits
tot = summarize(all_rows)
lines = [
    f"# {Y} agent look-back reports, summary",
    "",
    f"Pulled from Brokermint on {AS_OF:%b %-d, %Y}. Period: Jan 1 to {AS_OF:%b %-d}, {Y}, compared with Jan 1 to {PRIOR[1]:%b %-d}, {PY}.",
    "",
    f"Reports: {len(totals)} agents ({', '.join(f'{OFFICE_NAMES[k]}: {len(v)}' for k, v in sorted(office_agents.items()))}).",
    "",
    "## Brokerage totals (each deal side counted once)",
    "",
    "| Metric | " + f"{Y} YTD | + pending to Dec 31 | {PY} same period | {PY} full year |",
    "|---|---|---|---|---|",
]
for key, en, _es, fmt in SCORE_ROWS:
    en = "GCI (agent shares)" if key == "gci" else en
    lines.append(f"| {en} | {fmt(tot['ytd'][key])} | {fmt(tot['ytd'][key] + tot['pend_ye'][key])} | "
                 f"{fmt(tot['prior'][key])} | {fmt(tot['prior_full'][key])} |")
lines += [f"| Pending now | {num(tot['pending_count'])} | | | |",
          f"| Cancelled | {num(tot['cancelled'])} | | {num(tot['cancelled_p'])} | |", ""]
for code, lst in sorted(office_agents.items()):
    rows = [c for c in credits if (c["deal"]["state"] or "WI") == code]
    o = summarize(rows)
    lines.append(f"- {OFFICE_NAMES[code]}: {num(o['ytd']['units'])} closed units, {money(o['ytd']['volume'])} volume, "
                 f"{money(o['ytd']['gci'])} GCI, {num(o['pending_count'])} pending.")
no_deals = [u for u, _c, s in totals if not s["deal_ids"]]
quiet = [u for u, _c, s in totals if s["deal_ids"] and not s["ytd"]["units"] and not s["pending_count"]]
lines += ["", "## Data gaps", ""]
gap_text = {
    "closed_no_date": "Closed deals with no closing date (left out of every period)",
    "pending_past_due": "Pending deals whose closing date has already passed (not counted as closed; likely need updating)",
    "pending_no_date": "Pending deals with no expected closing date",
    "cancelled_no_date": f"Cancelled deals with no date, placed in {Y} by last-updated date",
    "no_agent": "Deals with no agent on the commission split or participant list (not in any agent report)",
    "no_split": f"{Y} closed deals with no commission split, credited to the participant agent with $0 GCI",
    "closed_zero_gci": f"{Y} closed deals with $0 total gross commission",
    "closed_no_lead": f"{Y} closed deals with no lead source",
}
for k, label in gap_text.items():
    seen, items = set(), []
    for d in gaps.get(k, []):
        if d["id"] not in seen:
            seen.add(d["id"])
            items.append(d)
    lines.append(f"### {label}: {len(items)}")
    lines += [deal_line(d) for d in items[:40]] or ["- none"]
    if len(items) > 40:
        lines.append(f"- ...and {len(items) - 40} more")
    lines.append("")
lines.append(f"### Agents with a report but no deals in Brokermint: {len(no_deals)}")
lines += [f"- {u.get('name')}" for u in no_deals] or ["- none"]
lines += ["", f"### Agents with deals but nothing closed or pending in {Y}: {len(quiet)}"]
lines += [f"- {u.get('name')}" for u in quiet] or ["- none"]
lines += ["", f"### People with {PY} or {Y} deals who did not get a report (inactive or non-agent role): {len(skipped)}"]
lines += [f"- {u.get('name')} ({role}, {'has' if act else 'no'} {Y} activity)" for u, role, act in skipped] or ["- none"]
if gaps.get("unknown_user"):
    lines += ["", f"### Deal credits paid to user IDs not in the user list: {len(set(gaps['unknown_user']))}"]
if not ONLY:
    with open(os.path.join(year_dir, "_broker-only", "summary.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
print(f"agents: {len(totals)}; offices: {dict((k, len(v)) for k, v in office_agents.items())}")
print(f"output: {year_dir}")
