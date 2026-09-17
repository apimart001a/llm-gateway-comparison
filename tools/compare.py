#!/usr/bin/env python3
"""Score gateway archetypes against your own weights, from data/gateways.json.

    python tools/compare.py --weight control=3 --weight cost_transparency=3 --weight setup_effort=2 --weight ops_burden=1
    python tools/compare.py --show            # print the criteria matrix
"""
from __future__ import annotations

import argparse
import json
import pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "gateways.json"


def load() -> dict:
    return json.loads(DATA.read_text())


def main() -> None:
    ap = argparse.ArgumentParser(description="Compare gateway archetypes with your own weighting")
    ap.add_argument("--weight", action="append", default=[], metavar="DIM=N",
                    help="score weight, e.g. --weight control=3 (repeatable)")
    ap.add_argument("--show", action="store_true", help="print the criteria matrix instead of scoring")
    args = ap.parse_args()

    payload = load()
    archetypes = payload["archetypes"]

    if args.show or not args.weight:
        dims = [d["id"] for d in payload["dimensions"]]
        print(f"{'archetype':26}" + "".join(f"{d:20}" for d in dims))
        for a in archetypes:
            print(f"{a['label'][:25]:26}" + "".join(f"{str(a.get(d, '—'))[:19]:20}" for d in dims))
        print("\nScores are 1 (weak) to 5 (strong) per dimension; pass --weight dim=N to rank.")
        return

    weights: dict[str, float] = {}
    for item in args.weight:
        if "=" not in item:
            raise SystemExit(f"expected DIM=N, got {item!r}")
        dim, value = item.split("=", 1)
        weights[dim] = float(value)

    scored = []
    for a in archetypes:
        scores = a.get("scores", {})
        total = sum(scores.get(dim, 0) * weight for dim, weight in weights.items())
        max_total = sum(5 * weight for weight in weights.values())
        scored.append((total, max_total, a["label"], a["id"]))
    scored.sort(reverse=True)
    for total, max_total, label, ident in scored:
        pct = (total / max_total * 100) if max_total else 0
        print(f"{label:38} {total:6.1f}/{max_total:.0f}  ({pct:5.1f}%)  [{ident}]")
    print("\nThese scores describe archetypes, not vendors. Re-check every cell then re-weight.")


if __name__ == "__main__":
    main()
