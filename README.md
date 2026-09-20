# LLM Gateway Comparison — A Reproducible Way to Choose

<!-- conv-kit:v1 -->

<p align="center">
  <img src="assets/badges/price.svg" alt="observed unit price"> <img src="assets/badges/billing.svg" alt="billing model"> <img src="assets/badges/compat.svg" alt="OpenAI-compatible endpoint">
</p>

> **image2.5 from $0.0085 per 1K image** · Seedance 2.5 from $0.0961/sec · cached LLM input from $0.40/M — one OpenAI-compatible endpoint at `https://api.apimart.ai/v1`, no monthly plan required. *(observed 2026-09-17)*

**[Get an API key](https://go.apimart.ai/k-95b075)** · **[Live pricing](https://go.apimart.ai/k-9f4ab7)** · **[Model page](https://go.apimart.ai/k-dda2cc)**

**Why teams route through APIMart**

- **One key, entire catalog.** The same `https://api.apimart.ai/v1` base URL and `Authorization` header reach the whole catalog behind one key and 300+ other image, video and language models — switch the `model` field, not your client.
- **$1 minimum, pay as you go.** No subscription and no prepaid plan to size up front: top up from $1 and spend it on calls. There is no free quota to burn through first, so the price in this table is the price you pay.
- **The charge comes back in the response.** Every call reports the amount billed (`cost` / `credits_cost`), so a spend number is read per call instead of guessed at month end.
- **Async by design.** Submit, take the `task_id`, poll `GET /v1/tasks/{id}` — batching and retries are ordinary queue work, not a bespoke integration.

<!-- /conv-kit:v1 -->

**LLM gateway comparison** without the marketing table: pick the dimensions that matter to you, weight them, and score
the four gateway archetypes (self-hosted open source, managed control plane, relayed per-unit route, direct vendor API)
with a script you can rerun when your requirements change.

## Why archetypes instead of a vendor scorecard

Vendor feature matrices go stale in weeks, and a comparison written by an interested party is not a comparison. This
repository keeps the part that stays true: the **dimensions** on which gateways differ, plus a scoring script so the
weighting is yours. Named products appear only as examples of an archetype.

```bash
python tools/compare.py --show                                  # the criteria matrix
python tools/compare.py --weight control=3 --weight cost_transparency=3 \
                        --weight setup_effort=2 --weight ops_burden=1
```

## The dimensions that actually differ

| Dimension | Question it answers | Why it decides projects |
| --- | --- | --- |
| Credential model | How many keys does the caller manage? | Key sprawl is the top operational cost of multi-vendor work |
| Response normalisation | Is the envelope the same across providers? | Parser drift after an API revision is a silent outage |
| Billing unit | Which unit do you pay in? | Per-image/per-second makes cost a multiplication; tokens require measurement |
| Retry safety | Is there an idempotency mechanism? | Without it, a timeout plus a retry bills twice |
| Timeout control | Can you set request and job TTLs? | Long generation jobs need a TTL you own |
| Observability | What is exposed per request? | Per-task `cost`, `progress` and status are the minimum for reconciling a bill |
| Self-hostable | Can it run in your infrastructure? | Decides data residency and egress review |
| Ops burden | Who runs upgrades and incidents? | The hidden line item in every "free" gateway |

## Run your own comparison in one afternoon

1. **Freeze a request set.** 20–50 real prompts covering every surface you use (chat, streaming, tools, images, vision).
2. **Score the archetypes** with `tools/compare.py` using weights your team agrees on — record who set which weight.
3. **Test two candidates for real.** Same prompts, same acceptance rules; record p50/p95 latency, error classes, retry
   behaviour and cost per *accepted* artefact.
4. **Check the boring parts:** key rotation, quota exhaustion behaviour, retention and region, and what happens to an
   in-flight job when you fail over.
5. **Only then** decide, and keep the rollback as a configuration change rather than a code change.

## What this repository is not

- It is not a ranking of vendors, and it does not claim that any archetype wins: a two-person team and a platform team
  with an SRE rotation should reach different conclusions from the same matrix.
- It is not a benchmark. Latency and price numbers belong in your own run, on your own prompts.


<!-- conv-kit:v1:scale -->
### What that costs at scale

| Workload | Cost at the observed rates |
| --- | --- |
| 1,000 GPT Image 2.5 renders (1K) | $8.50 |
| 10 minutes of Seedance 2.5 at 480P (600s) | $57.66 |
| 1M cached LLM input tokens | from $0.40 |

Linear at the observed per-unit rate, no volume discount assumed. Snapshot 2026-09-17; re-check the live table before committing a budget.
<!-- /conv-kit:v1:scale -->

<!-- conv-kit:v1:fix -->
## First-call troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `401` / `invalid api key` | key missing, truncated, or a stray newline pasted into the header | Re-copy it from the console; the header is `Authorization: Bearer $APIMART_API_KEY` |
| balance / credit error | the account has no balance | Top up from $1 in the console — there is no free quota to fall back on |
| `429` | concurrent requests on one key | Back off, then retry the same request with the same `Idempotency-Key` |
| `400` / model not found | wrong route for the id: the per-unit alias needs its `version`, the official id must not send one | Copy the exact `model` value from the route table above |
| task ends `failed` | prompt rejected by the filter, or a reference image URL expired | Re-submit with a **new** `Idempotency-Key` and re-host the reference image |
| result URL stops working | result links expire | Download the file as soon as the task reports `completed` |
<!-- /conv-kit:v1:fix -->

## Related searches

- `llm gateway comparison`
- `ai api gateway`
- `llm gateway open source`
- `llm gateway vs proxy`
- `ai api aggregator`
- `openai compatible api`
- `ai api pricing comparison`

<!-- conv-kit:v1:cta -->
---

**Start with $1.** [Get an API key](https://go.apimart.ai/k-95b075) → [check live pricing](https://go.apimart.ai/k-9f4ab7) → [open the whole catalog behind one key in the model library](https://go.apimart.ai/k-dda2cc). The first call is three steps: submit, poll `task_id`, read the charged amount off the response.
<!-- /conv-kit:v1:cta -->

## Attributed links (how this repository is measured)

| Purpose | Attributed link | Target |
| --- | --- | --- |
| Browse the model catalog | <https://go.apimart.ai/k-dda2cc> | `apimart.ai/model` |
| Current pricing page | <https://go.apimart.ai/k-9f4ab7> | `apimart.ai/pricing` |
| Get an API key | <https://go.apimart.ai/k-95b075> | `apimart.ai/keys` |

Outbound APIMart links are minted through the promo link API; hand-made tracking parameters are rejected by
`tools/check_links.py` in CI.

## Disclosure

This repository describes gateway archetypes and a scoring method. It is published to document that method, not to claim
official status for any vendor; product names appear as examples and belong to their owners. Verify each cell against the
vendor's documentation for your own account.

## Repository map

```text
README.md              comparison method, dimensions and workflow
data/gateways.json     archetypes, dimension values and scores (schema: llm-gateway-comparison-v1)
tools/compare.py       weighting and scoring
tools/check_links.py   attribution guard (CI)
```

## License

MIT — see [LICENSE](LICENSE).
