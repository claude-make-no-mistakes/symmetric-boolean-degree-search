"""Verify bounded search coverage by direct integer enumeration."""

import json
from itertools import combinations, product
from math import comb, isqrt, prod
from unittest.mock import patch

import central_search
import five_ones
from sparse_search import centered_quintuplets, moments, symmetric_blocks


def degree(word):
    row = list(word)
    result = 0
    while row:
        if row[0]:
            result = len(word) - len(row)
        row = [b-a for a, b in zip(row, row[1:])]
    return result


def check_moments():
    checked = 0
    for n in range(5, 13):
        for word in product((0, 1), repeat=n+1):
            if min(word) == max(word):
                continue
            assert (degree(word) <= n-4) == (moments(n, [k for k, v in enumerate(word) if v]) == (0, 0, 0, 0))
            assert degree([b-a for a, b in zip(word, word[1:])]) == degree(word)-1
            checked += 1
    return checked


def check_sparse():
    for n in range(5, 302, 2):
        expected = set()
        signed = [(-1)**k * (n-2*k) * comb(n, k) for k in range(n//2+1)]
        for i, j in combinations(range(n//2+1), 2):
            if signed[i] + signed[j] == 0:
                expected.add((i, j, n-j, n-i))
        assert expected == {indices for indices, _ in symmetric_blocks(n, comb(n, n//2))}
    for m in range(1, 58):
        expected = set()
        weights = [comb(2*m, k) for k in range(2*m+1)]
        for a, b in combinations(range(1, m+1), 2):
            points = [m-b, m-a, m, m+a, m+b]
            products = {weights[k]*prod(abs(k-j) for j in points if j != k) for k in points}
            if len(products) == 1:
                expected.add((a, b))
        assert expected == set(centered_quintuplets(m))


def check_central(module, sizes, arities, fold, tests):
    # Force many hash collisions, then compare the actual exact-check set to
    # combinations filtered by direct sums modulo eight.
    total = 0
    for n in sizes:
        weights = [(-1)**k * comb(n, k) for k in range(n+1)]
        window = 3
        positions = [k for k in range(n+1) if abs(n-2*k) <= window*isqrt(n)]
        if fold:
            positions = [k for k in positions if 2*k < n]
        expected = set()
        for arity in arities:
            for points in combinations(positions, arity):
                if not fold and any(a % 2 == b % 2 for a, b in zip(points, points[1:])):
                    continue
                if any(sum(weights[k]*(n-2*k)**j for k in points) % 8 for j in tests):
                    continue
                support = tuple(sorted(points + tuple(n-k for k in points))) if fold else points
                if len(support) < n+1:
                    expected.add(support)
        called = set()

        def record(n, positions):
            called.add(tuple(positions))
            return 1, 1, 1, 1

        with patch.object(module, "MASK", 7), patch.object(module, "moments", record):
            assert module.find(n, comb(n, n//2), window)[0] is None
        assert called == expected
        total += len(called)
    return total


if __name__ == "__main__":
    count = check_moments()
    check_sparse()
    folded = check_central(central_search, range(7, 32, 2), (3, 4), True, (1, 3))
    five = check_central(five_ones, range(5, 25), (5,), False, (0, 1))
    print(json.dumps({"nonconstant_profiles": count, "direct_four_one_last_odd": 301,
                      "direct_quintuple_last_middle": 57,
                      "forced_modulo_eight_candidates_folded": folded,
                      "forced_modulo_eight_candidates_five_ones": five}))
