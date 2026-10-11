# WTW 285 Mathematics Test — In-Depth Beginner Summary
## Scope: Lectures 10–18 / Weeks 6–10 material in the supplied lecture file

> **Important scope note:** The supplied WTW 285 study guide says the module's relevant material includes modular arithmetic/cryptography, partial orders, graphs, paths/circuits, adjacency matrices, and graph isomorphisms. The supplied lecture pack L10–18 covers Lectures 10–18. The RSA proof in “Why RSA cryptography works” is explicitly excluded from the test according to the test notice, so it is marked **NOT TESTED** below.

---

# 0. What you should understand before memorising formulas

This test is not just a formula test. A lot of questions will give you a mathematical object and ask you to **apply a definition, theorem, or algorithm**.

For every topic, learn these four things:

1. **What the object means**
2. **How to recognise/test it**
3. **What theorem or algorithm lets you solve a problem**
4. **How to calculate the answer**

The most important habit is:

> **Translate the question into the definition first.**

For example:
- “Is R reflexive?” → check whether every `a` has `(a,a) ∈ R`.
- “Is this graph Eulerian?” → check connectedness and vertex degrees.
- “Does a have an inverse modulo n?” → calculate `gcd(a,n)`.
- “Are these graphs isomorphic?” → compare invariants first, then construct a bijection if possible.

---

# 1. SYMBOLS YOU MUST BE COMFORTABLE WITH

## Sets

- `A, B, C` = sets
- `a ∈ A` = a is an element of A
- `A ⊆ B` = every element of A is also in B
- `A × B` = Cartesian product
- `|A|` = number of elements in A
- `P(A)` = power set of A, the set of all subsets of A

Example:

`A = {1,2,3}`

Then:

`|A| = 3`

and

`P(A) = {∅,{1},{2},{3},{1,2},{1,3},{2,3},{1,2,3}}`

---

## Logic symbols

- `∀` = for all
- `∃` = there exists
- `⇒` = implies
- `⇔` = if and only if
- `∧` = and
- `∨` = or

Example:

`∀x ∈ A, x ≤ 10`

means:

“For every x in A, x is at most 10.”

---

## Number theory symbols

### Divisibility

`a | b`

means:

> **a divides b**

meaning:

`b = ak` for some integer `k`.

Example:

`3 | 12`

because:

`12 = 3(4)`.

It does NOT mean that `3 = 12k`.

This distinction is extremely important.

---

## Greatest common divisor

`gcd(a,b)`

means the largest positive integer that divides both `a` and `b`.

Example:

`gcd(18,24)=6`.

---

## Modular notation

`a ≡ b (mod n)`

means:

> `a` and `b` have the same remainder when divided by `n`.

Equivalent:

`n | (a-b)`.

Example:

`17 ≡ 5 (mod 12)`

because:

`17-5=12`

and `12 | 12`.

---

# 2. MODULAR ARITHMETIC

## 2.1 What does “mod” mean?

The expression

`a mod n`

means the **remainder** when `a` is divided by `n`.

Example:

`17 mod 5 = 2`

because:

`17 = 5(3)+2`.

The remainder is always in:

`0,1,...,n-1`

when the modulus is positive.

---

# 2.2 Congruence

The notation

`a ≡ b (mod n)`

does NOT mean `a=b`.

It means that `a` and `b` are equivalent with respect to remainder modulo `n`.

### THEOREM 8.4.1 — MEMORISE

For integers `a,b,n`, with `n ≥ 1`, the following are equivalent:

1. `n | (a-b)`
2. `a ≡ b (mod n)`
3. `a = b + kn` for some `k ∈ Z`
4. `a` and `b` have the same remainder when divided by `n`
5. `a mod n = b mod n`

So if you see any one of these, you may replace it with any other.

### Example

Show:

`29 ≡ 5 (mod 12)`.

Use condition 1:

`29-5 = 24`

and

`12 | 24`.

Therefore:

`29 ≡ 5 (mod 12)`.

---

# 2.3 Why congruence is useful

Instead of calculating a huge number directly, reduce numbers first.

Example:

`6002 mod 6 = 2`

`17997 mod 6 = 3`.

Therefore:

`(6002+17997) mod 6`

can be calculated using:

`(2+3) mod 6 = 5`.

This is one of the most important practical uses of modular arithmetic.

---

# 2.4 THEOREM 8.4.3 — MODULAR ARITHMETIC RULES

If:

`a ≡ c (mod n)`

and

`b ≡ d (mod n)`

then:

### Addition

`a+b ≡ c+d (mod n)`

### Subtraction

`a-b ≡ c-d (mod n)`

### Multiplication

`ab ≡ cd (mod n)`

### Powers

For every non-negative integer `m`:

`a^m ≡ c^m (mod n)`.

### Practical version

You can reduce numbers modulo `n` **before** adding, subtracting, multiplying, or raising to a non-negative integer power.

---

# 2.5 Calculating large powers modulo n

A common exam problem is something like:

`12^43 mod 713`.

Do NOT calculate `12^43` normally.

Use **repeated squaring**.

## Step 1: Write the exponent as powers of 2

`43 = 32+8+2+1`

so:

`12^43 = 12^32 × 12^8 × 12^2 × 12`.

## Step 2: Calculate powers by repeatedly squaring

Start with:

`12^2 mod 713`

then:

`12^4 = (12^2)^2`

then:

`12^8 = (12^4)^2`

then:

`12^16 = (12^8)^2`

then:

`12^32 = (12^16)^2`.

Reduce modulo 713 after every step.

## Step 3: Multiply only the required powers

Then:

`12^43 ≡ 12^32 × 12^8 × 12^2 × 12 (mod 713)`.

Reduce again.

### Exam habit

Always reduce after each multiplication/square. This prevents huge numbers.

---

# 2.6 Last digits

Modulo arithmetic is also how you find final digits.

### Last digit

Calculate:

`N mod 10`.

### Last two digits

Calculate:

`N mod 100`.

### Last three digits

Calculate:

`N mod 1000`.

Example:

If:

`N mod 1000 = 352`

then the final three digits are `352`.

The lecture demonstrates this idea with a very large power and modulus `1000`.

---

# 3. GCD AND THE EUCLIDEAN ALGORITHM

## 3.1 gcd

`gcd(a,b)` is the largest positive integer dividing both `a` and `b`.

Example:

Factors of 18:

`1,2,3,6,9,18`

Factors of 24:

`1,2,3,4,6,8,12,24`

Therefore:

`gcd(18,24)=6`.

---

# 3.2 Euclidean Algorithm

The Euclidean algorithm gives the gcd efficiently.

Use repeated division:

`a = qb+r`

Then:

`gcd(a,b)=gcd(b,r)`.

Continue until the remainder is 0.

The last non-zero remainder is the gcd.

### Example

Find `gcd(330,156)`.

`330 = 2(156)+18`

`156 = 8(18)+12`

`18 = 1(12)+6`

`12 = 2(6)+0`

Therefore:

`gcd(330,156)=6`.

---

# 3.3 Bézout's Identity

### THEOREM — MEMORISE

For integers `a,b`, not both zero, there exist integers `s,t` such that:

`gcd(a,b)=sa+tb`.

This is extremely important because the Extended Euclidean Algorithm gives you these `s` and `t`.

Example:

`gcd(330,156)=6`

and:

`6 = 9(330)-19(156)`.

That is a Bézout representation.

---

# 3.4 Relatively prime / coprime

Two integers `a` and `b` are relatively prime if:

`gcd(a,b)=1`.

Example:

`gcd(8,15)=1`

so 8 and 15 are relatively prime.

Important:

Relatively prime does NOT mean both numbers are prime.

For example, 8 is not prime and 15 is not prime, but they are relatively prime.

---

# 4. LINEAR DIOPHANTINE EQUATIONS

A linear Diophantine equation has the form:

`ax+by=c`

where `x` and `y` must be integers.

---

## 4.1 Existence theorem — MEMORISE

The equation

`ax+by=c`

has an integer solution **if and only if**

`gcd(a,b) | c`.

### Example

`85x+34y=51`.

First:

`gcd(85,34)=17`.

Since:

`17 | 51`

solutions exist.

If the gcd did not divide 51, there would be no integer solutions.

---

# 4.2 Finding all solutions

Suppose:

`ax+by=c`.

### General strategy

1. Calculate `d=gcd(a,b)`.
2. Check `d|c`.
3. Divide the whole equation by `d`.
4. Find one solution.
5. Express the complete set of integer solutions using a parameter `t ∈ Z`.

### Example from the lecture

`85x+34y=51`.

Divide by 17:

`5x+2y=3`.

The lecture obtains:

`x = 3+2t`

`y = -6-5t`

for `t ∈ Z`.

Every integer value of `t` gives another integer solution.

---

# 5. LINEAR CONGRUENCE EQUATIONS

A linear congruence has the form:

`ax ≡ c (mod n)`.

---

## Existence theorem — MEMORISE

`ax ≡ c (mod n)`

has an integer solution **if and only if**

`gcd(a,n) | c`.

This is one of the most useful tests in modular arithmetic.

---

# 6. MULTIPLICATIVE INVERSES

## 6.1 Definition

`b` is an inverse of `a modulo n` if:

`ab ≡ 1 (mod n)`.

We often write:

`a^{-1} ≡ b (mod n)`.

### Example

If:

`43(307) ≡ 1 (mod 660)`

then 307 is the inverse of 43 modulo 660.

---

# 6.2 When does an inverse exist?

### COROLLARY — MEMORISE

`a` has an inverse modulo `n`

**if and only if**

`gcd(a,n)=1`.

This is one of the most important facts for RSA.

---

# 6.3 How to calculate an inverse

To find the inverse of `a mod n`:

1. Calculate `gcd(a,n)`.
2. If gcd ≠ 1, no inverse exists.
3. If gcd = 1, use the Extended Euclidean Algorithm.
4. Write:

`1 = sa+tn`.

5. Then:

`sa ≡ 1 (mod n)`.

Therefore `s` is the inverse of `a` modulo `n`.

### Example

Find inverse of 43 modulo 660.

Euclidean algorithm:

`660 = 15(43)+15`

`43 = 2(15)+13`

`15 = 1(13)+2`

`13 = 6(2)+1`

Back substitute:

`1 = 13-6(2)`

`=13-6(15-13)`

`=7(13)-6(15)`

`=7(43-2(15))-6(15)`

`=7(43)-20(15)`

`=7(43)-20(660-15(43))`

`=307(43)-20(660)`.

Therefore:

`307(43) ≡ 1 (mod 660)`.

So:

`43^{-1} ≡ 307 (mod 660)`.

---

# 6.4 Cancellation warning

Normal algebra says:

`ca = cb ⇒ a=b`

but modular arithmetic is different.

You CANNOT automatically cancel a common factor.

Example from the lecture:

`2(3) ≡ 2(5) (mod 4)`

but:

`3 ≢ 5 (mod 4)`.

So cancellation failed.

### Cancellation theorem — MEMORISE

If:

`ca ≡ cb (mod n)`

and:

`gcd(c,n)=1`

then:

`a ≡ b (mod n)`.

The condition `gcd(c,n)=1` is essential.

---

# 7. EUCLID'S LEMMA

### THEOREM — MEMORISE

If:

`a | bc`

and:

`gcd(a,c)=1`

then:

`a | b`.

Intuition:

If `a` divides a product `bc`, but `a` shares no factor with `c`, then the divisibility must come from `b`.

This theorem is used in modular proofs and RSA.

---

# 8. FERMAT'S LITTLE THEOREM

### THEOREM — MEMORISE

If `p` is prime and:

`p ∤ a`

then:

`a^(p-1) ≡ 1 (mod p)`.

Equivalent useful form:

`a^p ≡ a (mod p)`.

Be careful: the first version requires `p ∤ a`.

### Example

For prime `p=7` and `a=3`:

`3^6 ≡ 1 (mod 7)`.

---

# 9. CHINESE REMAINDER THEOREM

The study guide explicitly lists the Chinese Remainder Theorem as required knowledge.

The key idea is:

If you have simultaneous congruences with **pairwise coprime moduli**, such as

`x ≡ a (mod m)`

`x ≡ b (mod n)`

where:

`gcd(m,n)=1`,

then there is a solution, and the solution is unique modulo:

`mn`.

### What you should be able to do

Given two compatible congruences, combine them into one congruence.

Example structure:

`x ≡ 2 (mod 3)`

`x ≡ 3 (mod 5)`.

Try numbers congruent to 2 mod 3:

`2,5,8,11,14,...`

14 is 3 mod 5.

So:

`x ≡ 14 (mod 15)`.

---

# 10. CRYPTOGRAPHY BASICS

The lecture uses these terms:

- **plaintext** = original readable message
- **ciphertext** = encrypted message
- **encryption** = converting plaintext to ciphertext
- **decryption** = recovering plaintext from ciphertext

The course represents uppercase letters as:

`A=01, B=02, ..., Z=26`.

Example:

`HI = 08 09`.

---

# 11. RSA

RSA is a public-key cryptosystem.

There are two keys:

- public key → used for encryption
- private key → used for decryption

---

## 11.1 RSA key generation

Choose two distinct primes:

`p` and `q`.

Set:

`n=pq`.

Then calculate:

`φ(n)=(p-1)(q-1)`.

Choose `e` such that:

`gcd(e,(p-1)(q-1))=1`.

Then calculate `d` such that:

`ed ≡ 1 (mod (p-1)(q-1))`.

So:

`d = e^{-1} mod ((p-1)(q-1))`.

### Keys

Public key:

`(n,e)`.

Private key:

`(n,d)`.

---

# 11.2 RSA encryption

Given plaintext `M`:

`C ≡ M^e (mod n)`.

`C` is the ciphertext.

---

# 11.3 RSA decryption

Given ciphertext `C`:

`M ≡ C^d (mod n)`.

---

# 11.4 RSA calculation procedure

If given:

`p, q, e`

do this:

### Step 1

`n=pq`.

### Step 2

`φ(n)=(p-1)(q-1)`.

### Step 3

Check:

`gcd(e,φ(n))=1`.

### Step 4

Find:

`d=e^{-1} mod φ(n)`.

### Step 5

Public key:

`(n,e)`.

Private key:

`(n,d)`.

### Step 6: encrypt

`C=M^e mod n`.

### Step 7: decrypt

`M=C^d mod n`.

---

# 11.5 RSA and repeated squaring

RSA often produces enormous exponents.

Example:

`C=17^27 mod 55`.

Write:

`27=16+8+2+1`.

Therefore:

`17^27 = 17^16 × 17^8 × 17^2 × 17`.

Calculate:

`17^2 mod 55`

then repeatedly square:

`17^4`

`17^8`

`17^16`.

Then multiply the required residues.

---

# 11.6 RSA proof

The supplied test notice says:

> The proof that RSA correctly decrypts ciphertext in the section “Why RSA cryptography works” in Lecture 13 **will not be tested**.

Therefore:

**DO NOT spend your limited memorisation time learning the RSA correctness proof.**

You should still understand how RSA is constructed, encrypted, and decrypted.

---

# 12. PARTIAL ORDERS

A relation is a way of describing a connection between elements.

A **partial order** is a relation that behaves like a notion of “comes before”, “is below”, “is contained in”, or “divides”, but does not necessarily compare every pair.

---

# 12.1 Reflexive

A relation `R` on `A` is reflexive if:

`∀a∈A, (a,a)∈R`.

Plain English:

> Every element is related to itself.

Example:

`≤` is reflexive because:

`a≤a`.

---

# 12.2 Antisymmetric

A relation `R` is antisymmetric if:

If:

`aRb`

and:

`bRa`

then:

`a=b`.

Important:

Antisymmetric does NOT mean “not symmetric”.

It means:

> Two different elements cannot relate to each other in both directions.

Example:

`≤` is antisymmetric.

If:

`a≤b` and `b≤a`

then:

`a=b`.

---

# 12.3 Transitive

A relation is transitive if:

`aRb` and `bRc`

implies:

`aRc`.

Example:

If:

`a≤b`

and:

`b≤c`

then:

`a≤c`.

---

# 12.4 Partial order

A relation is a **partial order** if it is:

1. reflexive
2. antisymmetric
3. transitive

Memorise:

> **R + A + T = Partial Order**

A set together with a partial order is called a **partially ordered set (poset)**.

Notation often looks like:

`(A, ⪯)`.

---

# 12.5 Total order

A partial order becomes a **total order** when every pair of elements is comparable.

For every `a,b∈A`:

`a⪯b` OR `b⪯a`.

Example:

The usual `≤` on numbers is a total order.

But divisibility is generally only a partial order because some numbers cannot be compared.

---

# 13. HASSE DIAGRAMS

A Hasse diagram is a simplified picture of a partial order.

You start with the directed graph of the relation, then remove:

1. self-loops caused by reflexivity
2. arrows implied by transitivity
3. arrowheads

Then arrange smaller elements below larger elements.

---

## 13.1 Example idea

Suppose:

`a ⪯ b`

and:

`b ⪯ c`.

Then transitivity tells us:

`a ⪯ c`.

The Hasse diagram only needs:

`a`

above/below

`b`

above/below

`c`.

You do NOT draw the direct `a-c` edge because it is already implied.

---

# 13.2 How to construct a Hasse diagram

1. List all elements.
2. Determine which pairs satisfy the relation.
3. Remove `(a,a)` relationships.
4. Remove transitive relationships.
5. Draw the remaining cover relationships.
6. Put smaller elements lower and larger elements higher.

---

# 14. LEAST, MINIMAL, GREATEST, MAXIMAL

These are frequently confused.

## Least element

`a` is least if:

`a ⪯ x` for EVERY `x∈A`.

Think:

> “a is below everybody.”

There can be **at most one** least element.

---

## Minimal element

`a` is minimal if there is no different element below it.

Formally:

`x ⪯ a ⇒ x=a`.

Think:

> “Nothing is strictly below a.”

There can be multiple minimal elements.

---

## Greatest element

`a` is greatest if:

`x ⪯ a` for EVERY `x∈A`.

Think:

> “a is above everybody.”

At most one greatest element.

---

## Maximal element

`a` is maximal if there is no different element above it.

Think:

> “Nothing is strictly above a.”

There can be multiple maximal elements.

---

## Critical distinction

Least ⇒ minimal.

Greatest ⇒ maximal.

But:

minimal does NOT necessarily mean least.

maximal does NOT necessarily mean greatest.

---

# 15. CHAINS AND ANTICHAINS

## Chain

A subset `B` of a poset is a chain if every pair of elements in `B` is comparable.

So a chain behaves like a total order.

---

## Antichain

A subset is an antichain if all distinct elements are non-comparable.

---

## Chain length

The lecture defines the length of a chain `B` as:

`|B|-1`.

---

# 16. LEXICOGRAPHICAL ORDER

Lexicographical order is essentially dictionary order.

Compare two strings from left to right.

At the first position where they differ, use the underlying order to decide which comes first.

If one string is an initial segment of the other, the shorter one comes first.

Example with ordinary numerical/dictionary-style ordering:

`abc < abd`

because `a=a`, `b=b`, but `c<d`.

The lecture also considers lexicographical orders built from another partial order, such as divisibility.

---

# 17. TOPOLOGICAL SORTING

A topological sorting takes a partial order and produces a **total order compatible with it**.

In simple terms:

> Put the objects into a valid sequence without violating any “must come before” relationships.

---

## Algorithm

1. Choose any minimal element.
2. Put it first.
3. Remove it.
4. Choose another minimal element.
5. Put it next.
6. Repeat until no elements remain.

If several minimal elements exist, different valid topological orderings may be possible.

---

# 18. GRAPHS

A graph is a mathematical structure used to represent connections.

Write:

`G=(V,E,f)`.

Where:

- `V` = set of vertices
- `E` = set of edges
- `f` = edge-endpoint function

---

# 18.1 Vertex

A vertex is a point/node.

Examples:

People in a social network, cities on a map, computers in a network.

---

# 18.2 Edge

An edge represents a connection between vertices.

If:

`f(e)={v1,v2}`

then `e` connects `v1` and `v2`.

---

# 18.3 Adjacent

Two vertices are adjacent if an edge connects them.

Two edges are adjacent if they share a vertex.

---

# 18.4 Incident

An edge is incident on a vertex if that vertex is one of its endpoints.

---

# 18.5 Isolated vertex

A vertex with no incident edges.

So:

`deg(v)=0`.

---

# 18.6 Loop

An edge whose two endpoints are the same vertex.

The lecture writes:

`f(e)={v}`.

---

# 18.7 Parallel edges

Two distinct edges are parallel if they connect the same endpoints.

---

# 18.8 Directed graph

A directed graph has edges with direction.

An edge can go:

`v1 → v2`

without necessarily having:

`v2 → v1`.

---

# 18.9 Simple graph

A simple graph is:

- undirected
- has no loops
- has no parallel edges

---

# 19. COMPLETE GRAPHS

`K_n` is the complete graph on `n` vertices.

Every pair of distinct vertices has exactly one edge between them.

### Number of edges in `K_n`

MEMORISE:

`|E(K_n)| = n(n-1)/2`.

Why?

Each of the `n` vertices connects to `n-1` others, giving `n(n-1)` incidences, but each edge was counted twice.

---

# 20. COMPLETE BIPARTITE GRAPHS

`K_{m,n}` has two groups of vertices:

- group 1 has `m`
- group 2 has `n`

There are:

- no edges within the first group
- no edges within the second group
- every possible edge between the groups

Therefore:

`|E(K_{m,n})|=mn`.

---

# 21. SUBGRAPHS

`H` is a subgraph of `G` when:

- `V(H) ⊆ V(G)`
- `E(H) ⊆ E(G)`
- the endpoint relationships agree.

In simple terms:

> A subgraph is made by taking some vertices and/or edges from the original graph without inventing new edges.

---

# 22. DEGREE

The degree of a vertex `v` is:

`deg(v)` = number of edges incident on `v`.

### Important:

A loop counts **twice** toward degree.

---

# 22.1 Handshake Theorem

### MEMORISE

For every graph:

`Σ deg(v) = 2|E|`.

Meaning:

> The total of all vertex degrees is twice the number of edges.

Therefore:

> The total degree is always even.

---

# 22.2 Odd-degree consequence

### MEMORISE

Every graph has an **even number of vertices of odd degree**.

Possible numbers of odd-degree vertices:

`0,2,4,6,...`

Never:

`1,3,5,...`

This is a powerful way to show that a proposed graph cannot exist.

---

# 23. WALKS, TRAILS, PATHS AND CIRCUITS

This terminology is extremely important.

## Walk

A sequence of vertices/edges where consecutive vertices are connected.

Edges and vertices may repeat.

---

## Trail

A walk that does **not repeat edges**.

Vertices may repeat.

---

## Path

A walk that does not repeat vertices.

Therefore a path also does not repeat edges.

---

## Circuit

A closed walk:

Starts and ends at the same vertex.

---

## Simple circuit

A circuit that does not repeat vertices except for the starting/ending vertex.

---

# 23.1 Easy memory trick

Think about what is forbidden:

- Walk → almost nothing forbidden
- Trail → **no repeated edges**
- Path → **no repeated vertices**
- Simple circuit → closed + no repeated vertices except start/end

---

# 24. CONNECTED GRAPHS

Two vertices are connected if there is a walk between them.

A graph is connected if every pair of vertices is connected.

---

## Connected component

A connected component is a maximal connected subgraph.

Think:

> One “island” of connected vertices.

A disconnected graph can have several connected components.

---

# 25. EULER CIRCUITS

An Euler circuit is a circuit that uses:

> **every edge exactly once.**

Vertices may appear multiple times.

This is about **EDGES**.

---

## Euler circuit theorem — MEMORISE

For the course's undirected connected-graph setting:

A graph has an Euler circuit iff:

1. it is connected, and
2. every vertex has positive even degree.

The lecture presents the necessary direction and the sufficient condition separately.

### Necessary condition

If an Euler circuit exists, every vertex has positive even degree.

### Sufficient condition

If the graph is connected and every vertex has positive even degree, an Euler circuit exists.

---

# 25.1 Euler trail

An Euler trail uses:

> every edge exactly once

but does not have to finish where it started.

For a connected undirected graph:

- **0 odd vertices** → Euler circuit exists
- **2 odd vertices** → Euler trail exists, but not an Euler circuit
- **more than 2 odd vertices** → no Euler trail

---

# 26. EULER VS HAMILTONIAN

This is a very common conceptual trap.

## Euler

Focuses on:

> **edges**

Euler circuit = use every edge exactly once.

## Hamiltonian

Focuses on:

> **vertices**

Hamiltonian circuit = visit every vertex exactly once and return to the start.

### Memory:

**Euler = Edges**

**Hamiltonian = Homes/vertices**

---

# 27. HAMILTONIAN CIRCUITS

A Hamiltonian circuit:

- starts and ends at the same vertex
- visits every vertex
- visits every vertex exactly once, except the starting vertex appears again at the end

It does NOT require every edge to be used.

---

# 27.1 Proposition 10.1.6

If a graph has a Hamiltonian circuit, then it has a subgraph `H` such that:

1. `H` is connected
2. `V(H)=V(G)`
3. `|V(H)|=|E(H)|`
4. every vertex has degree 2 in `H`

### How to use it

If you can prove that no such subgraph can exist, then the original graph cannot have a Hamiltonian circuit.

This is a **necessary condition**, not a guarantee that a Hamiltonian circuit exists.

---

# 28. ADJACENCY MATRICES

For a graph with vertices:

`v1,v2,...,vn`

the adjacency matrix is an `n×n` matrix:

`A=(aij)`.

---

## Undirected graph

`aij` = number of edges connecting `vi` and `vj`.

For a simple graph:

- `1` = connected
- `0` = not connected

Because the graph is undirected:

`A` is symmetric.

So:

`aij = aji`.

---

## Directed graph

For a directed graph:

`aij` records the number of directed edges from `vi` to `vj`.

The matrix does not have to be symmetric.

---

# 29. CONSTRUCTING AN ADJACENCY MATRIX

Suppose the vertex order is:

`(v1,v2,v3)`.

To build the matrix:

1. Label rows by the source vertex.
2. Label columns by the destination vertex.
3. Put the appropriate number of edges in each cell.

For an undirected simple graph:

`Aij=1` if `vi` and `vj` are adjacent.

Otherwise:

`Aij=0`.

---

# 30. MATRIX POWERS AND WALKS

This is one of the most important applications of matrices.

### THEOREM

If `A` is the adjacency matrix of a graph, then:

> The `(i,j)` entry of `A^k` gives the number of walks of length `k` from `vi` to `vj`.

So:

`(A^2)ij`

= number of walks of length 2 from `vi` to `vj`.

`(A^3)ij`

= number of walks of length 3.

And so on.

---

## Example

If:

`(A^4)_{2,5}=7`

then there are exactly:

> 7 walks of length 4 from vertex `v2` to vertex `v5`.

---

# 31. ISOMORPHISM OF GRAPHS

Two graphs are **isomorphic** if they have the same structure, even if the vertex labels look different.

Notation:

`G ≅ G'`.

Think:

> Same graph structure, renamed vertices.

---

# 31.1 Function terminology

A function is:

### Injective / one-to-one

Different inputs give different outputs.

`x≠y ⇒ f(x)≠f(y)`.

### Surjective / onto

Every element in the target is hit.

### Bijective

Both injective and surjective.

For finite sets of equal size:

> injective ⇔ surjective.

---

# 31.2 Isomorphism definition

For general graphs, an isomorphism consists of bijections between:

- vertices
- edges

that preserve incidence.

For simple graphs, it is enough to find a bijection:

`g:V(G)→V(G')`

such that:

`{v,w}∈E(G)`

iff

`{g(v),g(w)}∈E(G')`.

---

# 31.3 How to prove two graphs are isomorphic

### Step 1

Check they have the same number of vertices.

### Step 2

Check they have the same number of edges.

### Step 3

Compare degree patterns.

### Step 4

Try to match vertices with the same structural roles.

### Step 5

Give an explicit bijection `g`.

### Step 6

Verify adjacency is preserved.

---

# 32. ISOMORPHIC INVARIANTS

An invariant is a property that must be the same for isomorphic graphs.

Useful invariants include:

- number of vertices
- number of edges
- degree sequence
- number of vertices of each degree
- connectedness
- number of connected components
- existence of certain cycles
- existence of Euler circuits
- existence of simple circuits of particular lengths
- number of certain structural features

### Critical rule

If an invariant differs:

> The graphs are definitely NOT isomorphic.

But if all the invariants you checked agree:

> That does NOT automatically prove they are isomorphic.

You may still need to construct an isomorphism.

---

# 33. HOW TO SHOW GRAPHS ARE NOT ISOMORPHIC

Look for the easiest invariant that differs.

Example:

Graph G:

degree sequence:

`1,1,2,2,4`

Graph H:

degree sequence:

`1,2,2,2,3`.

Since the degree sequences differ, the graphs cannot be isomorphic.

You do NOT need to try to construct an isomorphism.

---

# 34. HOW TO THINK ABOUT APPLICATION QUESTIONS

Your lecturer warned that the test is application-focused. Here is the decision process.

## If you see:

### `a ≡ b (mod n)`

Think:

- same remainder?
- does `n | (a-b)`?
- can I reduce both numbers modulo `n`?

---

### `ax ≡ c (mod n)`

Think:

`d=gcd(a,n)`.

Then:

- if `d ∤ c` → no solution
- if `d | c` → solutions exist

---

### “Find inverse”

Think:

`gcd(a,n)=1?`

- no → inverse does not exist
- yes → Extended Euclidean Algorithm

---

### “RSA”

Think:

`n=pq`

`φ(n)=(p-1)(q-1)`

choose `e` coprime to `φ(n)`

find:

`ed ≡ 1 (mod φ(n))`

encrypt:

`C=M^e mod n`

decrypt:

`M=C^d mod n`.

---

### “Is this a partial order?”

Check:

1. reflexive?
2. antisymmetric?
3. transitive?

All three → partial order.

---

### “Is it a total order?”

First partial order, then:

> Are every two elements comparable?

---

### “Find least/greatest/minimal/maximal”

Remember:

- least = below **everyone**
- minimal = nobody strictly below
- greatest = above **everyone**
- maximal = nobody strictly above

---

### “Draw Hasse diagram”

Remove:

- self-loops
- transitive edges
- arrowheads

Then arrange lower elements below higher elements.

---

### “Topological sort”

Repeatedly choose a minimal element and remove it.

---

### “Does an Euler circuit exist?”

Check:

1. connected?
2. all degrees even?

Yes to both → Euler circuit.

---

### “Does an Euler trail exist?”

For a connected undirected graph:

- 0 odd → Euler circuit
- 2 odd → Euler trail
- >2 odd → neither

---

### “Hamiltonian?”

Think:

> visit every vertex exactly once and return.

Try Proposition 10.1.6 to rule one out.

---

### “Adjacency matrix”

Rows/columns correspond to vertices.

For undirected graphs, the matrix is symmetric.

---

### “How many walks of length k?”

Calculate `A^k`.

Then read the required `(i,j)` entry.

---

### “Are graphs isomorphic?”

Compare invariants first.

If they survive, construct a bijection preserving adjacency.

---

# 35. FORMULA / THEOREM SHEET — MEMORISE THIS

## Modular arithmetic

### Congruence equivalence

`a ≡ b (mod n)`

iff

`n | (a-b)`

iff

`a=b+kn` for some `k∈Z`

iff

`a mod n=b mod n`.

---

### Modular operations

If:

`a ≡ c (mod n)`

and:

`b ≡ d (mod n)`

then:

`a+b ≡ c+d (mod n)`

`a-b ≡ c-d (mod n)`

`ab ≡ cd (mod n)`

`a^m ≡ c^m (mod n)`.

---

### GCD / Bézout

`gcd(a,b)=sa+tb`.

---

### Diophantine existence

`ax+by=c` has integer solutions iff:

`gcd(a,b)|c`.

---

### Linear congruence existence

`ax≡c (mod n)` has a solution iff:

`gcd(a,n)|c`.

---

### Inverse

`b=a^{-1} (mod n)` iff:

`ab≡1 (mod n)`.

Inverse exists iff:

`gcd(a,n)=1`.

---

### Cancellation

If:

`ca≡cb (mod n)`

and:

`gcd(c,n)=1`

then:

`a≡b (mod n)`.

---

### Fermat

If `p` is prime and `p∤a`:

`a^(p-1)≡1 (mod p)`.

---

### RSA

`n=pq`

`φ(n)=(p-1)(q-1)`

`gcd(e,φ(n))=1`

`ed≡1 (mod φ(n))`

Encryption:

`C≡M^e (mod n)`

Decryption:

`M≡C^d (mod n)`.

---

## Partial orders

Partial order:

> reflexive + antisymmetric + transitive.

Total order:

> partial order + every pair comparable.

---

## Graphs

Handshake theorem:

`Σ deg(v)=2|E|`.

Therefore:

> number of odd-degree vertices is even.

Complete graph:

`|E(K_n)|=n(n-1)/2`.

Complete bipartite:

`|E(K_{m,n})|=mn`.

---

## Euler

Euler circuit:

> every edge exactly once, return to start.

Connected undirected graph has Euler circuit iff every vertex has even degree.

Euler trail:

> every edge exactly once, endpoints may differ.

Connected undirected graph has an Euler trail iff it has 0 or 2 odd-degree vertices.

---

## Hamiltonian

Hamiltonian circuit:

> every vertex exactly once, return to start.

If Hamiltonian circuit exists, there is a spanning subgraph where every vertex has degree 2 and:

`|V|=|E|`.

---

## Adjacency matrices

`A^k`:

> entry `(i,j)` = number of walks of length `k` from `vi` to `vj`.

---

# 36. DEFINITIONS YOU SHOULD MEMORISE WORD-FOR-WORD ENOUGH TO RECOGNISE

## Number theory

- divides
- congruent modulo
- gcd
- relatively prime
- linear combination
- multiplicative inverse
- linear Diophantine equation

## Partial orders

- reflexive
- antisymmetric
- transitive
- partial order
- total order
- comparable
- Hasse diagram
- least
- minimal
- greatest
- maximal
- chain
- antichain
- lexicographical order
- topological sorting

## Graphs

- vertex
- edge
- endpoint
- adjacent
- incident
- isolated vertex
- loop
- parallel edges
- directed graph
- simple graph
- complete graph
- bipartite graph
- subgraph
- degree
- connected
- connected component
- walk
- trail
- path
- circuit
- simple circuit
- Euler circuit
- Euler trail
- Hamiltonian circuit
- adjacency matrix
- graph isomorphism
- invariant

---

# 37. COMMON EXAM TRAPS

## Trap 1: Divisibility

`a|b` means:

`b=ak`

NOT:

`a=bk`.

---

## Trap 2: Antisymmetric

Antisymmetric does NOT mean “not symmetric”.

It means:

`aRb` and `bRa` ⇒ `a=b`.

---

## Trap 3: Minimal vs least

Minimal:

> no smaller element directly exists below it.

Least:

> smaller than EVERY element.

---

## Trap 4: Maximal vs greatest

Maximal:

> nothing strictly above it.

Greatest:

> above EVERY element.

---

## Trap 5: Euler vs Hamiltonian

Euler → edges.

Hamiltonian → vertices.

---

## Trap 6: Walk vs trail vs path

Walk:

> edges can repeat.

Trail:

> edges cannot repeat.

Path:

> vertices cannot repeat.

---

## Trap 7: Modular cancellation

You cannot simply cancel.

Check:

`gcd(common factor,n)=1`.

---

## Trap 8: RSA correctness proof

The RSA correctness proof is explicitly excluded from the test.

Do not waste study time memorising that proof.

---

## Trap 9: Isomorphic graphs

Same number of vertices and edges is NOT enough.

You need the same structure.

---

# 38. WHAT I WOULD PRIORITISE FOR STUDY

## Tier 1 — MUST KNOW COLD

1. `a|b`
2. `a≡b (mod n)`
3. Theorem 8.4.1
4. Modular addition/subtraction/multiplication/powers
5. Euclidean algorithm
6. Extended Euclidean algorithm
7. Bézout identity
8. gcd and relatively prime
9. Inverse criterion
10. Linear congruence existence criterion
11. Fermat's Little Theorem
12. RSA key generation
13. RSA encryption/decryption
14. Reflexive/antisymmetric/transitive
15. Partial order
16. Hasse diagram
17. least/minimal/greatest/maximal
18. topological sorting
19. graph/vertex/edge/degree
20. Handshake theorem
21. walk/trail/path/circuit
22. Euler circuit theorem
23. Euler trail condition
24. Hamiltonian circuit
25. adjacency matrix
26. `A^k` = walks of length k
27. graph isomorphism
28. invariants

---

# 39. PROOF PRIORITY

The WTW 285 study guide specifically identifies proofs that students should know.

For the modular arithmetic section, it explicitly lists proofs of:

- Theorem 8.4.1
- Theorem 8.4.2
- Theorem 8.4.3

For graph introduction:

- Theorem 4.9.1
- Proposition 4.9.3

For paths/circuits:

- Theorem 10.1.2
- Theorem 10.1.3

However, the supplied L10–18 lecture PDF does not contain the complete statements of all of these earlier-numbered textbook results. Therefore, use your lecturer's exact proof notes/textbook statements when memorising those proofs rather than relying on a reconstructed version here.

---

# 40. A PRACTICAL TEST-SOLVING CHECKLIST

When you receive a question:

## Step 1 — Identify the topic

Ask:

“Is this modular arithmetic, partial orders, or graphs?”

## Step 2 — Identify the mathematical object

Examples:

- congruence
- relation
- poset
- graph
- matrix

## Step 3 — Write the relevant definition/theorem

Do not immediately calculate.

## Step 4 — Apply it mechanically

Examples:

`gcd(a,n)=1?`

or:

“All degrees even?”

or:

“Is every pair comparable?”

## Step 5 — Check your answer

Ask:

- Does the result make sense?
- Did I confuse a definition?
- Did I accidentally cancel modulo `n`?
- Did I confuse Euler and Hamiltonian?
- Did I forget connectivity?
- Did I remove all transitive edges from a Hasse diagram?

---

# 41. ULTRA-SHORT NIGHT-BEFORE CHEAT SHEET

```text
DIVISIBILITY
a | b  <=>  b = ak, k ∈ Z

CONGRUENCE
a ≡ b (mod n)
<=> n | (a-b)
<=> same remainder mod n

MODULAR RULES
Reduce first.
Add/subtract/multiply/power safely.

GCD
Euclidean Algorithm:
a = qb+r
gcd(a,b)=gcd(b,r)

BEZOUT
gcd(a,b)=sa+tb

COPRIME
gcd(a,b)=1

DIOPHANTINE
ax+by=c has integer solution
iff gcd(a,b)|c

LINEAR CONGRUENCE
ax ≡ c (mod n) has solution
iff gcd(a,n)|c

INVERSE
ab ≡ 1 (mod n)
inverse exists iff gcd(a,n)=1

CANCELLATION
ca ≡ cb (mod n)
can cancel c only if gcd(c,n)=1

FERMAT
p prime, p∤a:
a^(p-1) ≡ 1 (mod p)

RSA
n=pq
φ=(p-1)(q-1)
gcd(e,φ)=1
ed ≡ 1 (mod φ)
C=M^e mod n
M=C^d mod n

PARTIAL ORDER
Reflexive + Antisymmetric + Transitive

TOTAL ORDER
Partial order + every pair comparable

LEAST
below everyone

MINIMAL
nothing strictly below

GREATEST
above everyone

MAXIMAL
nothing strictly above

HASSE
remove loops
remove transitive edges
remove arrows
lower = smaller

TOPOLOGICAL SORT
repeatedly choose minimal element

GRAPH
G=(V,E,f)

DEGREE
number incident edges
loop counts twice

HANDSHAKE
Σdeg(v)=2|E|

ODD DEGREES
number of odd-degree vertices is even

K_n
edges = n(n-1)/2

K_m,n
edges = mn

WALK
edges/vertices may repeat

TRAIL
no repeated edges

PATH
no repeated vertices

CIRCUIT
starts = ends

EULER
EVERY EDGE exactly once

EULER CIRCUIT
connected + all degrees even

EULER TRAIL
connected + exactly 0 or 2 odd vertices

HAMILTONIAN
EVERY VERTEX exactly once + return

ADJACENCY MATRIX
A_ij = edges from vi to vj
(undirected: A symmetric)

A^k
(i,j) entry = number of walks length k

ISOMORPHISM
same structure under relabelling
bijection preserving adjacency

INVARIANT
property preserved by isomorphism
different invariant => NOT isomorphic
same invariants => NOT automatically isomorphic
```

---

# 42. FINAL STUDY STRATEGY

Do NOT try to memorise every line of the lectures.

Instead:

### First pass
Understand every definition.

### Second pass
Memorise the theorem/formula sheet.

### Third pass
Practise one application of every algorithm:

- Euclidean algorithm
- Extended Euclidean algorithm
- modular exponentiation
- inverse calculation
- RSA
- Hasse diagram
- topological sorting
- degree/Handshake calculations
- Euler test
- Hamiltonian reasoning
- adjacency matrix
- matrix powers
- graph isomorphism

### Fourth pass
Do mixed questions where you must decide **which theorem or algorithm applies**.

That last stage is especially important because the lecturer described the assessment as application-focused.

