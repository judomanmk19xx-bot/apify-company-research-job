# Company Research Job

**Give a company name. Get a finished research job back.**

Most research tools sell you raw search results and leave the synthesis to you. This Actor sells the *finished job*: one run researches one company live and returns a single structured result:

- **Headline signals** — the company's current notable developments, each with its source URL
- **Digital footprint** — web presence and key facts found for the company and its domain
- **Written briefing** — a stitched, readable research summary, not a pile of links

## Input

| Field | Required | Description |
|---|---|---|
| `company` | Yes | Company name, e.g. `Vinamilk` |
| `domain` | No | Company website domain, e.g. `vinamilk.com.vn` — improves footprint accuracy |
| `geo` | No | Country focus, e.g. `VN`, `US` |

## Output

One dataset item per run containing the full report: `research_summary`, `footprint`, `briefing`, `web`, plus `generated_at` and any `partial_failures` (the job reports honestly if one component could not complete).

## Pricing

Pay per event: **one charge per completed job**. If the job fails, the run fails and you are not charged for a result you did not get.

## Who runs this

Operated by **Mekong Trade Intelligence**, a pay-per-call API seller on Base (x402). The same job is available directly as an API for agent builders; this Actor is the no-wallet, no-crypto way to buy it.

Results are generated live for each run from current web sources — they are research assistance, not financial advice.
