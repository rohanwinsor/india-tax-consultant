#!/usr/bin/env python3
"""Indian individual income-tax calculator: old vs new regime.

Usage:
    python tax_calc.py profile.json [--rules rules_fy2026_27.json] [--json]

The profile format is documented in example_profile.json. All amounts are
annual rupees for the tax year. Rule constants come from the rules JSON, so a
verified change only needs that file updated.

Scope: resident individuals; salary, other slab income, equity STCG/LTCG,
other LTCG at 12.5%, VDA at 30%. Not modelled: business income, set-off of
house-property loss, carried-forward losses, agricultural income, AMT,
indexation option on pre-July-2024 property, and the EPF/NPS/superannuation
perquisite above Rs 7.5 lakh. Treat output as an estimate and say so.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def slab_tax(income, slabs):
    tax, lower = 0.0, 0.0
    for upper, rate in slabs:
        if upper is None or income <= upper:
            tax += max(0.0, income - lower) * rate
            return tax
        tax += (upper - lower) * rate
        lower = upper
    return tax


def basic_exemption(slabs):
    upper, rate = slabs[0]
    return upper if rate == 0 else 0


def surcharge_rate(total_income, table):
    rate = 0.0
    for threshold, r in table:
        if total_income > threshold:
            rate = r
    return rate


def compute(profile, rules, regime):
    r = rules[regime]
    sp = rules["special_rates"]
    notes = []

    age = profile.get("age", 30)
    if regime == "old":
        key = "below_60" if age < 60 else ("60_to_79" if age < 80 else "80_plus")
        slabs = r["slabs_by_age"][key]
    else:
        slabs = r["slabs"]

    salary = float(profile.get("salary_gross", 0))
    basic = float(profile.get("basic_salary", 0))
    employer_nps = float(profile.get("employer_nps", 0))
    prof_tax = float(profile.get("professional_tax", 0))

    # Salary income
    salary_income = salary + employer_nps
    deductions = {"standard_deduction": min(r["standard_deduction"], salary_income) if salary_income else 0}
    nps_cap = r["employer_nps_pct_of_basic"] * basic
    deductions["employer_nps"] = min(employer_nps, nps_cap)
    if employer_nps > nps_cap:
        notes.append(f"Employer NPS {employer_nps:,.0f} exceeds the {regime}-regime cap {nps_cap:,.0f}; excess is taxable.")

    old_d = profile.get("old_regime", {}) or {}
    if regime == "old":
        deductions["professional_tax"] = prof_tax
        deductions["hra_exempt"] = float(old_d.get("hra_exempt", 0))
        deductions["lta_and_other_exemptions"] = float(old_d.get("other_salary_exemptions", 0))
        c = r["caps"]
        deductions["80C"] = min(float(old_d.get("80C", 0)), c["80C"])
        deductions["80CCD1B"] = min(float(old_d.get("80CCD1B", 0)), c["80CCD1B"])
        deductions["80D"] = float(old_d.get("80D", 0))
        deductions["24b"] = min(float(old_d.get("home_loan_interest_self_occupied", 0)), c["24b_self_occupied"])
        deductions["other_chapter_via"] = float(old_d.get("other_deductions", 0))
        notes.append("80D and 'other' deductions are taken as entered; confirm they are within their limits.")

    salary_deductions = deductions["standard_deduction"] + deductions["employer_nps"] + deductions.get("professional_tax", 0) \
        + deductions.get("hra_exempt", 0) + deductions.get("lta_and_other_exemptions", 0)
    net_salary = max(0.0, salary_income - salary_deductions)

    other = float(profile.get("other_income_slab", 0))
    chapter_via = sum(deductions.get(k, 0) for k in ("80C", "80CCD1B", "80D", "24b", "other_chapter_via"))
    normal_income = max(0.0, net_salary + other - chapter_via)

    stcg_eq = float(profile.get("stcg_equity", 0))
    ltcg_eq_gross = float(profile.get("ltcg_equity", 0))
    ltcg_eq = max(0.0, ltcg_eq_gross - sp["ltcg_equity_exemption"])
    ltcg_other = float(profile.get("ltcg_other", 0))
    vda = float(profile.get("vda_gains", 0))

    # Residents may use unused basic exemption against special-rate gains (not VDA).
    shortfall = max(0.0, basic_exemption(slabs) - normal_income)
    used = {}
    for name, amt in (("stcg_equity", stcg_eq), ("ltcg_other", ltcg_other), ("ltcg_equity", ltcg_eq)):
        take = min(shortfall, amt)
        used[name] = take
        shortfall -= take
    stcg_eq_t = stcg_eq - used["stcg_equity"]
    ltcg_other_t = ltcg_other - used["ltcg_other"]
    ltcg_eq_t = ltcg_eq - used["ltcg_equity"]

    total_income = normal_income + stcg_eq + ltcg_eq + ltcg_other + vda

    tax_normal = slab_tax(normal_income, slabs)
    tax_stcg = stcg_eq_t * sp["stcg_equity"]
    tax_ltcg_eq = ltcg_eq_t * sp["ltcg_equity"]
    tax_ltcg_other = ltcg_other_t * sp["ltcg_other"]
    tax_vda = vda * sp["vda"]

    # Rebate
    reb = r["rebate"]
    rebate = 0.0
    if regime == "new":
        eligible = tax_normal
    else:
        eligible = tax_normal + (tax_stcg if reb.get("applies_to_stcg_equity") else 0)
    if total_income <= reb["income_limit"]:
        rebate = min(eligible, reb["max_rebate"])
    elif reb.get("marginal_relief"):
        excess = total_income - reb["income_limit"]
        if eligible > excess:
            rebate = eligible - excess
            notes.append("Marginal relief on the rebate applied.")
    if regime == "new" and (stcg_eq or ltcg_eq or ltcg_other or vda) and total_income <= reb["income_limit"]:
        notes.append("New-regime rebate not applied to special-rate gains (verify current position).")

    base_normal = max(0.0, tax_normal - rebate) if regime == "new" else tax_normal
    base_special = tax_stcg + tax_ltcg_eq + tax_ltcg_other
    if regime == "old":
        # rebate reduces normal + 111A tax together
        combined = max(0.0, tax_normal + tax_stcg - rebate)
        base_normal, base_special = combined, tax_ltcg_eq + tax_ltcg_other
    tax_before_surcharge = base_normal + base_special + tax_vda

    # Surcharge with 15% cap on equity/other LTCG and STCG; VDA and normal at full rate
    s_rate = surcharge_rate(total_income, r["surcharge"])
    s_cap = min(s_rate, sp["surcharge_cap_on_equity_gains_and_dividends"])
    surcharge = (base_normal + tax_vda) * s_rate + base_special * s_cap

    # Marginal relief on surcharge
    if s_rate > 0:
        thresholds = [t for t, _ in r["surcharge"] if t < total_income]
        t = max(thresholds)
        # Approximation: tax at the threshold, taking the excess off slab income
        lower_rate = surcharge_rate(t, r["surcharge"])
        tax_at_t = slab_tax(max(0.0, t - (total_income - normal_income)), slabs) + base_special + tax_vda
        tax_at_t_with_s = tax_at_t * (1 + lower_rate) if lower_rate else tax_at_t
        limit = tax_at_t_with_s + (total_income - t)
        if tax_before_surcharge + surcharge > limit:
            relief = tax_before_surcharge + surcharge - limit
            surcharge = max(0.0, surcharge - relief)
            notes.append("Marginal relief on surcharge applied (approximate).")

    cess = (tax_before_surcharge + surcharge) * rules["cess_rate"]
    total_tax = round(tax_before_surcharge + surcharge + cess)

    return {
        "regime": regime,
        "gross_total_income": round(salary_income + other + stcg_eq + ltcg_eq_gross + ltcg_other + vda),
        "deductions": {k: round(v) for k, v in deductions.items() if v},
        "normal_income": round(normal_income),
        "special_rate_income": {"stcg_equity": round(stcg_eq), "ltcg_equity_taxable": round(ltcg_eq),
                                "ltcg_other": round(ltcg_other), "vda": round(vda)},
        "total_income": round(total_income),
        "tax_on_normal_income": round(tax_normal),
        "tax_on_special_income": round(tax_stcg + tax_ltcg_eq + tax_ltcg_other + tax_vda),
        "rebate": round(rebate),
        "surcharge": round(surcharge),
        "cess": round(cess),
        "total_tax": total_tax,
        "effective_rate_on_gross": round(total_tax / max(1.0, salary_income + other + stcg_eq + ltcg_eq_gross + ltcg_other + vda) * 100, 2),
        "notes": notes,
    }


def fmt(n):
    s = str(int(round(n)))
    neg = s.startswith("-")
    s = s.lstrip("-")
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return ("-" if neg else "") + "₹" + s


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("profile")
    ap.add_argument("--rules", default=os.path.join(HERE, "rules_fy2026_27.json"))
    ap.add_argument("--json", action="store_true", help="print machine-readable output")
    a = ap.parse_args()

    with open(a.profile) as f:
        profile = json.load(f)
    with open(a.rules) as f:
        rules = json.load(f)

    res = {k: compute(profile, rules, k) for k in ("new", "old")}
    better = min(res, key=lambda k: res[k]["total_tax"])
    diff = abs(res["new"]["total_tax"] - res["old"]["total_tax"])
    out = {"tax_year": rules["tax_year"], "rules_snapshot": rules["snapshot_date"], "results": res,
           "lower_tax_regime": better, "saving": diff}

    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print(f"Tax year {rules['tax_year']} (rules snapshot {rules['snapshot_date']}, verify before use)\n")
    rows = [("Total income", "total_income"), ("Tax on slab income", "tax_on_normal_income"),
            ("Tax on special-rate income", "tax_on_special_income"), ("Rebate", "rebate"),
            ("Surcharge", "surcharge"), ("Cess", "cess"), ("TOTAL TAX", "total_tax")]
    print(f"{'':28}{'New regime':>16}{'Old regime':>16}")
    for label, key in rows:
        print(f"{label:28}{fmt(res['new'][key]):>16}{fmt(res['old'][key]):>16}")
    print(f"{'Effective rate on gross':28}{res['new']['effective_rate_on_gross']:>15}%{res['old']['effective_rate_on_gross']:>15}%")
    print(f"\nLower tax: {better.upper()} regime, by {fmt(diff)}")
    for k in ("new", "old"):
        for n in res[k]["notes"]:
            print(f"  [{k}] {n}")


if __name__ == "__main__":
    sys.exit(main())
