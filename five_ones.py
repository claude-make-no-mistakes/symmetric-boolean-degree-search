"""Search five-one supports in a central window without a reflection assumption."""

import argparse
import json
from math import comb, isqrt

from central_search import MASK
from sparse_search import moments


def entries(n, middle_weight, limit):
    out = []
    weight = middle_weight
    for k in range(n // 2, -1, -1):
        q = n - 2*k
        if q > limit:
            break
        w = (-1)**k * weight
        out.append((k, w & MASK, (w*q) & MASK))
        if q:
            w = (-1)**(n-k) * weight
            out.append((n-k, w & MASK, (-w*q) & MASK))
        weight = weight*k // (n-k+1)
    return sorted(out)


def find(n, central, window):
    points = entries(n, central, window * isqrt(n))
    pairs = ({}, {})
    hit_count = 0
    for i in range(2, len(points) - 2):
        b, b0, b1 = points[i - 1]
        for a, a0, a1 in points[:i - 1]:
            if (a ^ b) & 1:
                key = ((a0+b0) & MASK, (a1+b1) & MASK)
                pairs[b % 2].setdefault(key, []).append((a, b))
        c, c0, c1 = points[i]
        candidates = pairs[1 - c % 2]
        for j in range(i + 1, len(points) - 1):
            d, d0, d1 = points[j]
            if not (c ^ d) & 1:
                continue
            target0, target1 = -c0-d0, -c1-d1
            for e, e0, e1 in points[j + 1:]:
                if not (d ^ e) & 1:
                    continue
                for a, b in candidates.get(((target0-e0) & MASK, (target1-e1) & MASK), ()):
                    hit_count += 1
                    found = (a, b, c, d, e)
                    if n + 1 > 5 and moments(n, found) == (0, 0, 0, 0):
                        return found, len(points), hit_count
    return None, len(points), hit_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=int)
    parser.add_argument("last", type=int)
    parser.add_argument("--square-family", action="store_true")
    parser.add_argument("--window", type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.first <= args.last or args.window < 1:
        parser.error("expected positive window and 1 <= first <= last")
    if args.square_family:
        sizes = (4*t*t-1 for t in range(2, isqrt((args.last+1)//4)+1)
                 if 4*t*t-1 >= args.first)
    else:
        sizes = range(args.first, args.last+1)
    checked = positions = hits = 0
    for n in sizes:
        witness, count, tested = find(n, comb(n, n//2), args.window)
        checked += 1
        positions += count
        hits += tested
        if witness is not None:
            print(json.dumps({"counterexample": {"n": n, "ones": witness}}), flush=True)
            return
    print(json.dumps({"first_bound": args.first, "last_bound": args.last,
                      "square_family_only": args.square_family, "window_multiplier": args.window,
                      "sizes": checked, "positions": positions, "full_moment_checks": hits,
                      "counterexample": None}), flush=True)


if __name__ == "__main__":
    main()
