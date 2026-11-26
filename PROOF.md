# Reflection and sparse searches for degree deficit four

Let $b_0,\ldots,b_n\in\{0,1\}$ be a nonconstant profile, and let $F$ be its interpolating polynomial. The exact degree of the symmetric Boolean function with this profile is $\deg F$. Indeed the sum of all squarefree $j$-fold monomials takes value $\binom{k}{j}$ on inputs of Hamming weight $k$. This identifies the unique multilinear expansion with the Newton expansion of $F$.

The von zur Gathen–Roche conjecture asks whether $n-\deg F\le3$. The known symmetric deficit-three examples motivate the sparse searches for a deficit-four witness. [Original paper](https://doi.org/10.1007/BF01215917) · [Asymptotic progress and reported search through 8,192](https://arxiv.org/html/2611.26446#S1.SS3)

## Reflection constraint on every candidate

**Proposition.** Suppose $\deg F\le n-4$. The length-$n$ prefix and suffix of the profile both have deficit at least three, and at least one is neither palindromic nor anti-palindromic. Here anti-palindromic means that each pair of reflected bits sums to one.

The same interpolating polynomial has degree $d=\deg F$ on both length-$n$ windows, since each has $n>d$ points. Neither can be constant. Write $S(x)=2F(x)-1$. If the prefix has reflection sign $\epsilon\in\{1,-1\}$, the equality $S(x)=\epsilon S(n-1-x)$ holds at its $n$ integer points. It therefore holds as a polynomial identity. If the suffix has reflection sign $\eta$, the second identity is $S(x)=\eta S(n+1-x)$. Composing gives $S(x+2)=\epsilon\eta S(x)$. Comparison of leading coefficients forces $\epsilon\eta=1$. The leading term of the finite difference $S(x+2)-S(x)$ then forces $S$ to be constant, a contradiction.

More generally any interval of more than $d$ sample points with reflection symmetry gives a polynomial reflection identity at the center of that interval. A nonconstant polynomial can have at most one such center. The two published reflection-symmetric families therefore cannot supply both windows of the same witness. In a minimum-order counterexample both windows have deficit exactly three by minimality, so at least one window gives a deficit-three profile without either reflection symmetry. The assertion that a degree deficit drops by at most one under taking a prefix or suffix also follows from Proposition 4.1 of von zur Gathen and Roche. [Original paper, Proposition 4.1](https://cosec.bit.uni-bonn.de/fileadmin/user_upload/publications/pubs/gatroc97.pdf)

## Exact moment tests

Set $w_i=(-1)^i\binom ni$. Deficit at least four is equivalent to vanishing of $\sum_i w_i b_i(n-2i)^j$ for $0\le j\le3$. The falling factorials $(n-i)_{\underline j}$ for $0\le j\le3$ form another basis for the test polynomials. In that basis, $\binom ni(n-i)_{\underline j}=(n)_{\underline j}\binom{n-j}{i}$, so each test is a nonzero multiple of one of the four highest Newton coefficients. For a nonconstant candidate $n\ge5$. The analogous test for deficit three uses $0\le j\le2$.

### Combining four-one profiles

For odd $n$, a reflected support of size four consists of $i,j,n-j,n-i$ with $i<j\le\lfloor n/2\rfloor$. Both even moments vanish. The linear moment vanishes precisely when $j-i$ is odd and

$$ (n-2i)\binom ni=(n-2j)\binom nj.$$

The left side as a sequence in $i$ first increases and then decreases, with at most one tie at its maximum. For adjacent indices, the sign of its forward difference is the sign of $(q-1)^2-(n+1)$ with $q=n-2i$, by the ratio of consecutive binomial coefficients. To enumerate equalities, scan backward from $\lfloor n/2\rfloor$, store the strictly increasing part, compare the remaining part to it, and stop when the weight drops below the central endpoint weight. The adjacent maximum tie is included. The cubic moment of each match is computed in integers. Disjoint supports with opposite cubic moments would sum to a binary deficit-four witness.

### Five ones and five transitions

Four distinct positions cannot support a nonzero vector that annihilates every polynomial of degree at most three, by Vandermonde invertibility. At five positions $t_0<\cdots<t_4$ there is just one null direction. With $A(x)=\prod_i(x-t_i)$ it has entries $1/A'(t_i)$ by interpolation of polynomials of degree at most three. Thus the signed entries alternate in sign and their absolute weights satisfy $\binom N{t_i}|A'(t_i)|=C$, a common value.

For five ones, use $N=n$ and signs $(-1)^{t_i}$. For five transitions, use the difference profile $b_{i+1}-b_i$, supported on $0,\ldots,n-1$, whose degree drops by one and whose deficit stays unchanged. Its signs at the five transitions alternate, so after multiplication by $(-1)^{t_i}$ all transition indices must have the same parity. This condition is necessary because the entries of the null direction alternate.

If the five positions contain two reflected pairs about $N/2$, compare the equal absolute weights at the endpoints of one pair. Distances to the other pair contribute identical factors, and the single remaining position must have equal distance to both endpoints. Thus it is $N/2$ and $N=2M$ is even. Conversely, reflection-symmetric five positions always consist of two pairs and the midpoint. Write them as $M-b,M-a,M,M+a,M+b$ where $0<a<b\le M$. Put $v_j=\binom{2M}{M+j}$. Evaluating the three derivative products yields

$$
v_a\,2a^2(b^2-a^2)=v_0\,a^2b^2,
\qquad
v_b\,2b^2(b^2-a^2)=v_0\,a^2b^2.
$$

If $q_a=v_a/v_0$, the first equality gives $b^2=2q_a a^2/(2q_a-1)$. Therefore the search can stop as soon as $q_a\le1/2$, since these ratios decrease. For every preceding $a$ it checks divisibility and squares in integers, followed by the second equality. The parity requirement is $a$ odd and $b$ even for five ones, or both even for five transitions. Complementing the profile applies the same test to five zeros. The identity at $M=2$, $a=1$, $b=2$ gives the constant all-ones word and serves as a positive arithmetic control.

### Searching larger central supports

The six- and eight-one search takes three or four distinct mirrored pairs on odd rows. It uses the two odd moments after folding. For three pairs, it searches for a single signature opposite to a two-pair signature. For four pairs, it searches for two disjoint two-pair signatures summing to zero. Each signature is computed modulo $2^{64}$, and all pairs with a matching signature are retained. Every surviving support is checked with all four exact integer moments.

The unrestricted five-one search allows any arrangement of five positions inside the specified central interval. It uses the alternating parity condition above. It splits the five positions into two lower and three higher indices, computes the first two moments modulo $2^{64}$, and checks all matches with the four exact moments. This also tests five-zero supports by complementation. The interval bounds specify which profiles are covered. Outside the interval, a sparse support need not satisfy the same computational exclusions.
