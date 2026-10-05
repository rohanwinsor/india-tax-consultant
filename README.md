# india-tax-consultant

A Claude skill that acts as a careful Indian tax and personal-finance consultant for a resident individual. It builds your **full financial picture**, then advises in a fixed order:

1. **Safety** — legal compliance and capital protection (emergency fund, insurance, debt, concentration, foreign-asset reporting, AIS reconciliation, advance tax)
2. **Tax** — legal minimisation: regime choice by computation, salary structuring, capital-gains timing and harvesting, deductions only where they make sense as investments
3. **Returns** — post-tax allocation by goal horizon, rebalanced tax-efficiently

It is built for the **Income-tax Act, 2025** (in force from 1 April 2026, tax year 2026-27) and makes Claude verify every rate and limit against official sources each time it runs rather than trusting a hard-coded table.

> Not a CA or SEBI-registered investment adviser. Outputs are planning estimates; verify before acting and consult a CA for complex cases.

## What's inside

```
india-tax-consultant/
├── SKILL.md                      # workflow and guardrails
├── references/
│   ├── intake.md                 # questions + document checklist
│   ├── safety-first.md           # ordered safety audit
│   ├── tax-rules.md              # dated rule snapshot + official sources
│   ├── tax-playbook.md           # optimisation levers and traps
│   ├── portfolio-review.md       # broker holdings → keep/change verdicts
│   ├── instruments.md            # tax/safety/liquidity of each instrument
│   └── report-template.md        # output format
└── scripts/
    ├── tax_calc.py               # old vs new regime calculator (no deps)
    ├── rules_fy2026_27.json      # all rule constants, edit when verified changes
    └── example_profile.json
```

## Install

**Claude.ai / Claude desktop:** download `dist/india-tax-consultant.zip` and upload it under Settings → Capabilities → Skills.

**Claude Code:**

```bash
git clone https://github.com/rohanwinsor/india-tax-consultant.git
cp -r india-tax-consultant/india-tax-consultant ~/.claude/skills/
```

Then ask something like *"Here are my Form 16, AIS and CAS — give me a full financial plan"* or *"Old or new regime for me this year?"*

## Calculator

```bash
python india-tax-consultant/scripts/tax_calc.py india-tax-consultant/scripts/example_profile.json
```

Handles slabs, standard deduction, rebate with marginal relief, employer NPS caps, old-regime deductions, equity STCG/LTCG with the annual exemption, other LTCG, VDA, surcharge (with the 15% cap on capital gains and approximate marginal relief) and cess. It does **not** model business income, loss set-off/carry-forward, indexation on pre-July-2024 property, or AMT.

## Updating for a new Budget

1. Copy `rules_fy2026_27.json` to the new year and edit the changed figures.
2. Update `references/tax-rules.md` (snapshot date, tables).
3. Re-run the calculator on the example profile and sanity-check the output.

## Privacy

Redact PAN, Aadhaar, bank/demat account numbers and addresses before sharing documents with any AI tool.

## License

MIT
