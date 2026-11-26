"""Meet-in-the-middle search for symmetric supports of six or eight ones."""

import argparse
import json
from itertools import combinations
from math import comb, isqrt

from sparse_search import moments

MASK = (1 << 64) - 1


def find(n, central, window):
    entries = []
    middle = n // 2
    weight = central
    limit = window * isqrt(n)
    for k in range(middle, max(-1, (n - limit + 1) // 2 - 1), -1):
        q = n - 2*k
        signed = (-1)**k * weight * q
        entries.append((k, signed & MASK, (signed*q*q) & MASK))
        weight = weight * k // (n - k + 1)

    def check(half):
        full = sorted(half + [n-k for k in half])
        if len(full) < n + 1 and moments(n, full) == (0, 0, 0, 0):
            return full
        return None

    singles = {}
    for k, linear, cubic in entries:
        singles.setdefault((linear, cubic), []).append(k)
    pairs = {}
    compared = 0
    for (a, first, second), (b, third, fourth) in combinations(entries, 2):
        signature = ((first + third) & MASK, (second + fourth) & MASK)
        target = ((-signature[0]) & MASK, (-signature[1]) & MASK)
        for c in singles.get(target, ()):
            if c not in (a, b):
                compared += 1
                if (witness := check([a, b, c])) is not None:
                    return witness, len(entries), compared
        for c, d in pairs.get(target, ()):
            if a not in (c, d) and b not in (c, d):
                compared += 1
                if (witness := check([a, b, c, d])) is not None:
                    return witness, len(entries), compared
        pairs.setdefault(signature, []).append((a, b))
    return None, len(entries), compared


def scan(first, last, window):
    first |= 1
    central = comb(first, first // 2)
    checked = positions = modular_hits = 0
    for n in range(first, last + 1, 2):
        witness, count, hits = find(n, central, window)
        checked += 1
        positions += count
        modular_hits += hits
        if witness is not None:
            print(json.dumps({"counterexample": {"n": n, "ones": witness}}), flush=True)
            return
        central = central * (2*(n + 2)) // (n // 2 + 2)
    print(json.dumps({"first_odd_n": first, "last_bound": last, "window_multiplier": window,
                      "odd_sizes": checked, "left_positions": positions,
                      "full_moment_checks": modular_hits, "counterexample": None}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=int)
    parser.add_argument("last", type=int)
    parser.add_argument("--window", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.first <= args.last or args.window < 1:
        parser.error("expected positive window and 1 <= first <= last")
    scan(args.first, args.last, args.window)


if __name__ == "__main__":
    main()
