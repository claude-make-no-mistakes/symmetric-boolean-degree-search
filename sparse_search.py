"""Search exact symmetric sparse profiles for degree deficit at least four."""

import argparse
import json
from itertools import combinations
from math import comb, isqrt


def moments(n, indices):
    return tuple(sum((-1)**i * comb(n, i) * (n - 2*i)**j for i in indices) for j in range(4))


def symmetric_blocks(n, central):
    """Yield all symmetric four-one profiles of odd order with deficit >= 3."""
    middle = n // 2
    increasing = {}
    previous = 0
    rising = True
    coefficient = central
    for i in range(middle, -1, -1):
        q = n - 2*i
        score = q * coefficient
        if score <= previous:
            rising = False
        if rising:
            increasing[score] = i
        elif score < central:
            break
        elif (other := increasing.get(score)) is not None and (other - i) % 2:
            indices = (i, other, n - other, n - i)
            cubic = 2 * (-1)**i * score * (q*q - (n - 2*other)**2)
            yield indices, cubic
        previous = score
        coefficient = coefficient * i // (n - i + 1)


def is_square_block(n, indices):
    t = isqrt((n + 1) // 4)
    k = 2*t*t - t - 1
    return t >= 2 and n == 4*t*t - 1 and indices == (k, k + 1, n - k - 1, n - k)


def scan_blocks(first, last):
    checked = known = blocks = combined = 0
    first = max(5, first | 1)
    central = comb(first, first // 2)
    for n in range(first, last + 1, 2):
        checked += 1
        for_count = list(symmetric_blocks(n, central))
        blocks += len(for_count)
        for indices, cubic in for_count:
            assert moments(n, indices) == (0, 0, 0, cubic)
            if is_square_block(n, indices):
                known += 1
            else:
                print(json.dumps({"other_block": {"n": n, "ones": indices}}), flush=True)
        t = isqrt((n + 1) // 4)
        if t >= 2 and n == 4*t*t - 1 and not any(is_square_block(n, indices) for indices, _ in for_count):
            raise RuntimeError(f"missed square-family control at n={n}")
        for (left, a), (right, b) in combinations(for_count, 2):
            if set(left) & set(right):
                continue
            combined += 1
            if a + b == 0:
                indices = sorted(left + right)
                assert len(indices) < n + 1 and moments(n, indices) == (0, 0, 0, 0)
                print(json.dumps({"counterexample": {"n": n, "ones": indices}}), flush=True)
                return
        central = central * (2*(n + 2)) // (n // 2 + 2)
    print(json.dumps({"first_odd_n": first, "last_bound": last, "odd_sizes": checked,
                      "four_one_blocks": blocks, "square_family_blocks": known,
                      "disjoint_block_pairs": combined, "counterexample": None}), flush=True)


def centered_quintuplets(middle):
    """Yield relative offsets (a,b) of every reflected five-point solution."""
    from fractions import Fraction

    ratio = Fraction(1)
    for a in range(1, middle):
        ratio *= Fraction(middle - a + 1, middle + a)
        numerator, denominator = ratio.as_integer_ratio()
        divisor = 2*numerator - denominator
        if divisor <= 0:
            return
        square, remainder = divmod(2*numerator*a*a, divisor)
        if remainder:
            continue
        b = isqrt(square)
        if b*b != square or b <= a or b > middle:
            continue
        if (comb(2*middle, middle + b) * 2*(b*b - a*a)
                == comb(2*middle, middle) * a*a):
            yield a, b


def scan_quintuples(first, last):
    identities = 0
    for middle in range(first, last + 1):
        for a, b in centered_quintuplets(middle):
            identities += 1
            indices = (middle - b, middle - a, middle, middle + a, middle + b)
            if a % 2 and b % 2 == 0 and 2*middle + 1 > 5:
                n = 2*middle
                assert moments(n, indices) == (0, 0, 0, 0)
                print(json.dumps({"counterexample": {"n": n, "ones": indices}}), flush=True)
                return
            if a % 2 == 0 and b % 2 == 0:
                word = [sum(t < i for t in indices) % 2 for i in range(2*middle + 2)]
                n = 2*middle + 1
                ones = [i for i, bit in enumerate(word) if bit]
                assert moments(n, ones) == (0, 0, 0, 0)
                print(json.dumps({"counterexample": {"n": n, "ones": ones}}), flush=True)
                return
            print(json.dumps({"identity": {"middle": middle, "offsets": [a, b]}}), flush=True)
    print(json.dumps({"first_middle": first, "last_middle": last, "identities": identities,
                      "counterexample": None}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("blocks", "quintuples"))
    parser.add_argument("first", type=int)
    parser.add_argument("last", type=int)
    args = parser.parse_args()
    if not 1 <= args.first <= args.last:
        parser.error("expected 1 <= first <= last")
    if args.mode == "blocks":
        scan_blocks(args.first, args.last)
    else:
        scan_quintuples(args.first, args.last)


if __name__ == "__main__":
    main()
