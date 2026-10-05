# Portfolio review

Review what the user actually holds and how they invest, then give a verdict. "No change needed" is a valid and often correct answer — do not invent changes to look useful. Recommend a change only if it clears one of the bars below.

## 1. Get the holdings

Prefer live, read-only connections; fall back to exports.

| Source | Best route | Fallback |
|---|---|---|
| Zerodha | Kite MCP connector (official, free, `https://mcp.kite.trade/mcp`; mostly read-only, GTT orders only) | Console → Holdings + Tax P&L export (CSV/XLSX) |
| Groww | Groww MCP connector (official, `https://mcp.groww.in/mcp`; stocks and F&O only, **can place orders**) | Holdings and capital-gains report export; MF holdings always via CAS (not covered by the MCP as of Oct 2026) |
| Angel One | Holdings / P&L export from the app or web | — Do not ask the user to share SmartAPI keys, passwords or TOTP secrets with an unofficial MCP server. |
| Mutual funds (any platform) | CAS from CAMS/KFintech/MF Central — one file covers every AMC and platform | Platform exports |
| Demat (direct equity, bonds, SGB, ETFs) | NSDL/CDSL consolidated CAS | Broker exports |
| Foreign (RSUs, US stocks) | Brokerage statements | — |

Check the session's tools for a connector before asking for exports. Neither connector is in Claude's directory; the user adds them as custom connectors using the URLs above. Connector coverage changes — if a call fails or a data type is missing, fall back to exports and say so.

Never place, modify or cancel orders (including GTTs), even if a connector allows it — this skill is advisory only. Recommend the user disable a connector's order tools if their client allows per-tool control.

De-duplicate across sources (the same MF can appear in a CAS and a platform export). Note the as-of date of each source.

## 2. Reconstruct the investing pattern

From transactions (CAS, tax P&L, order history where available):
- SIPs: amount, funds, regularity, step-ups, stopped SIPs.
- Lump sums and their timing (chasing rallies? panic sells?).
- Trading activity: count of trades, holding periods, intraday/F&O share, realised P&L after charges and tax.
- Churn: funds or stocks held < 12 months and replaced.

## 3. Assess, item by item

For each holding: asset class, sub-type (large/mid/small, index/active, sector/thematic, debt credit quality), value, % of portfolio, unrealised gain split into short/long-term, expense ratio, and how long until short-term lots turn long-term.

Then the portfolio:

| Check | Flag when |
|---|---|
| Fits the target allocation per goal (instruments.md) | Off target by more than ~5 percentage points at portfolio level |
| Concentration | Single stock > 10%, single sector > 25–30%, employer stock + RSUs > 10% of net worth |
| Overlap | Several funds holding largely the same stocks (e.g. multiple large-cap/flexi-cap funds) |
| Cost | Regular plans where direct is available; active fund with high expense ratio that has lagged its index over 5+ years |
| Fund count | More funds than distinct roles (often > 6–8) |
| Behaviour | Frequent trading or F&O with net losses after costs and tax; stopped SIPs during falls |
| Quality | Credit-risk debt funds, small-cap/thematic beyond a satellite slice, penny/illiquid stocks, unregulated products |
| Tax efficiency | Unharvested LTCG exemption; short-term lots about to turn long-term; losses available to book; debt held in high-slab name when a lower-slab family member could hold it |

## 4. Decide: change or keep

Recommend a change only when at least one holds:
- It fixes a **safety** gap (concentration, unregulated product, liquidity for a near goal).
- The **net benefit over 5 years** exceeds the cost of switching (exit loads, STT, tax on gains realised now), shown in rupees.
- It removes a **behavioural** leak the data shows (loss-making trading, churn).

Otherwise mark it **Keep**. If the whole portfolio passes, say so directly: "This is in good shape — keep the SIPs running; next review in 12 months or on a life event."

When a switch is warranted, sequence it to cut tax: redirect new SIPs first; sell lots that are long-term, at a loss, or within the annual LTCG exemption; delay short-term lots close to turning long-term unless the safety reason is urgent.

## 5. Output

| Holding | Value | % | Role | Verdict (Keep / Reduce / Exit / Add) | Reason | Tax cost of change | Net 5-yr effect |

Followed by: portfolio-level verdict in one line, the SIP changes (if any), and the order of execution.
