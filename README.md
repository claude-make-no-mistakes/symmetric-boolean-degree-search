# Searching for a symmetric Boolean degree counterexample

The von zur Gathen–Roche conjecture says that every nonconstant symmetric Boolean function on $n$ bits has exact real degree at least $n-3$. A minimum-order counterexample would have two length-$n$ windows whose deficits are exactly three, and at least one window would be neither palindromic nor anti-palindromic. This follows because a nonconstant polynomial can have only one reflection center. The conjecture remains open. [Paper](paper.pdf) · [Proof and search derivations](PROOF.md) · [Original conjecture](https://doi.org/10.1007/BF01215917)

## Exact searches

| Families searched | Range and outcome |
| --- | --- |
| Reflected supports with four ones and deficit at least three, and disjoint unions of two such supports | All 24,999 odd orders from 5 through 50,001. The only 110 matches were the published square-family blocks. No order supplied two disjoint matching blocks. [Log](four-one-blocks.jsonl) |
| Five ones, five zeros, or five transitions with at least two reflected pairs among their five positions | All even binomial rows through 60,000. The sole arithmetic identity gives the constant all-ones control. [Log](reflected-quintuples.jsonl) |
| Reflected supports of six or eight ones within $|n-2k|\le 4\lfloor\sqrt n\rfloor$ | All 1,904 odd orders from 8,193 to 11,999. No counterexample. [Log](central-search.jsonl) |
| Five ones with arbitrary placement within $|n-2k|\le 2\lfloor\sqrt n\rfloor$ | The 100 consecutive orders 8,193 through 8,292, and 55 square-family orders $n=4t^2-1$ from 8,193 through 40,000. No counterexample. [Consecutive orders](five-ones-frontier.jsonl) · [Square-family orders](five-ones-squares.jsonl) |

The central searches use congruence signatures modulo $2^{64}$. Any true solution must match the signatures exactly. Each candidate that matches is checked with all four integer moments. Complementing the profile gives the same exclusions for supports of zeros. These are exhaustive searches of the stated families.

## Reproduce

The scripts use the standard library in Python 3.10 or later.

```sh
python -B sparse_search.py blocks 5 50001
python -B sparse_search.py quintuples 1 30000
python -B central_search.py 8193 11999 --window 4
python -B five_ones.py 8193 8292 --window 2
python -B five_ones.py 8193 40000 --window 2 --square-family
python -B verify.py
```

The verifier compares the moment test with exact finite differences on 16,304 nonconstant Boolean profiles through order 12. It checks the four-one and quintuple searches against direct exact enumeration. It also lowers the modulus to eight to force collisions and checks that the congruence searches pass the exact checker every matching support. A fresh GPT-6.2 Sol High referee independently checked the reflection proposition and the two sparse enumerators against direct small-order computations. [Verification output](verification.json)
