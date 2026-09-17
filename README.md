# LLM Gateway Comparison — A Reproducible Way to Choose

**LLM gateway comparison** without the marketing table: pick the dimensions that matter to you, weight them, and score
the four gateway archetypes (self-hosted open source, managed control plane, relayed per-unit route, direct vendor API)
with a script you can rerun when your requirements change.

**Attributed entry points:** [Browse the model catalog](https://go.apimart.ai/k-dda2cc) · [Current pricing](https://go.apimart.ai/k-9f4ab7) · [Get an API key](https://go.apimart.ai/k-95b075)

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

## Related searches

- `llm gateway comparison`
- `ai api gateway`
- `llm gateway open source`
- `llm gateway vs proxy`
- `ai api aggregator`
- `openai compatible api`
- `ai api pricing comparison`

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
