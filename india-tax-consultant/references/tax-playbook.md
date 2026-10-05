# Tax playbook

Each lever: what it does, when it helps, the trap. Only recommend a lever if it passes the safety audit and makes sense *as a financial decision*, not just as a deduction.

## 1. Regime choice

- Always compute both with `scripts/tax_calc.py` using the user's real numbers. Do not rely on rule-of-thumb break-evens.
- The old regime tends to win only with large deductions together: full 80C + 80CCD(1B) + 80D + high HRA in a metro + home-loan interest. Most salaried users without a home loan are better off in the new regime from FY 2025-26 onward.
- Count only deductions the user would make **anyway**. A ₹1.5 lakh ELSS/PPF that exists only to justify the old regime is not free money.
- Note the regime declared to the employer only affects TDS; the final choice is made in the ITR (for salaried users without business income). Flag if the employer is withholding on the wrong regime — it causes either a big tax bill or a locked-up refund.

## 2. Salary structuring (ask the employer what's allowed)

| Lever | Works in | Notes |
|---|---|---|
| Employer NPS contribution | Both (14% of salary new, 10% old) | Strongest lever for most. Trade-off: locked till 60, partial annuitisation. Size it to retirement needs, not to the cap. |
| HRA | Old only | Needs genuine rent; landlord PAN if rent above the threshold. Rent to parents is legal only if they actually own the property and declare the income. |
| LTA, meal cards, telephone/internet, car lease, gadget reimbursements | Mostly old; some perquisite valuations apply in both | Check under the new Act's perquisite rules; value is usually small. |
| ESOP/RSU | Both | Taxed as salary at vest/exercise (FMV − price paid); a second tax as capital gains on sale. Cost basis = FMV at vest. Keep vest records. |

## 3. Capital gains

- **Holding periods**: Before selling, check days to long-term status (12 months listed equity; 24 months foreign shares, unlisted, property). A few weeks' wait can turn slab or 20% into 12.5%.
- **LTCG harvesting**: Each year, realise listed-equity LTCG up to the ₹1.25 lakh exemption and buy back (no wash-sale rule in India; watch exit loads and STT). Resets cost basis upward tax-free.
- **Loss harvesting**: Book losses to offset gains in the same year; remember STCL offsets both, LTCL only LTCG. File on time to carry forward.
- **RSU diversification**: For foreign RSUs, sale after 24 months from vest = LTCG at 12.5%. Within 24 months = slab. Balance this against concentration risk — for a large single-stock position, risk reduction usually beats waiting for the lower rate.
- **Debt MFs bought after 1 Apr 2023** are taxed at slab regardless of holding — for a 30%-slab user they lose their old edge over FDs except for deferral (tax only on redemption). Consider arbitrage funds (equity taxation) for short-term parking where suitable.
- **Property**: exemptions for reinvestment in a house or specified bonds (old 54/54EC/54F) have caps and lock-ins; verify current limits and sections. Get a CA for any sale above ~₹1 crore.

## 4. Deductions (old regime) — rank by intrinsic value

1. 80D health insurance — needed anyway (safety item); deduction is a bonus.
2. EPF (already deducted from salary) usually fills a large part of 80C.
3. PPF — sovereign, tax-free, long lock-in. Good for the debt part of long-term allocation.
4. NPS 80CCD(1B) — only if the user accepts the lock-in and annuity rules.
5. ELSS — equity with 3-year lock; only if the user wants that equity anyway.
6. Avoid: endowment/money-back/traditional plans and ULIPs bought for 80C. Low returns, long lock-ins. If the user holds them, evaluate surrender vs. paid-up vs. continue on post-tax IRR from today.

## 5. Family and household

- Income from gifts to a spouse (or minor child) is clubbed back to the giver. Gifts to adult children or parents are not clubbed. Investing in a lower-slab parent's name can legally lower tax on the returns (the gift itself is tax-free for relatives) — but control passes to them; say so.
- Pay parents' health premiums (old regime 80D, additional limit).

## 6. Timing and process

- Advance tax: compute after each vest, sale or large interest credit; pay by the instalment dates to avoid interest.
- Declare other income to the employer (where allowed) so TDS covers it.
- Year-end checklist by mid-March: harvest gains/losses, top-up PPF/NPS if planned, collect proofs, confirm regime.
- ITR form: salary + capital gains or foreign assets → ITR-2 (not ITR-1). Business/F&O/freelance → ITR-3 (or ITR-4 presumptive if eligible).

## 7. Foreign assets and income

- Report every foreign holding in the foreign assets schedule (calendar-year basis for many items — verify) with peak and closing values, plus income in the foreign income schedule.
- Claim foreign tax credit (Form 67, filed by the due date) for tax withheld abroad on dividends.
- LRS remittances above ₹10 lakh attract TCS — claimable as credit in the ITR; it is a cash-flow cost, not an extra tax.

## Traps to call out

- Tax-saving products that wreck liquidity or returns.
- Chasing the ₹1.25 lakh LTCG exemption with frequent trading — STT, spreads and short-term gains erase it.
- Moving everything to the old regime for one large deduction while losing the new regime's lower slabs.
- Treating TDS as final tax — interest, dividends and capital gains often leave a balance due.
- Crypto: 30% flat and losses can't be set off — after tax the risk/reward is far worse than headline returns.
