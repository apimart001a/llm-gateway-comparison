# Contributing

Useful contributions:

1. A dimension we are missing, phrased as a question a buyer would actually ask.
2. A correction to a cell in `data/gateways.json`, with the vendor documentation you checked and the date.
3. A new archetype (for example: edge/CDN-hosted inference gateways) with honest scores.

Before opening a pull request:

```bash
python tools/compare.py --show
python tools/check_links.py
```

Rules: keep the file about archetypes rather than vendor marketing, disclose your affiliation when proposing a change
that favours a product, and never state a number you have not verified.
