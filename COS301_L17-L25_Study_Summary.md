# COS 301 — Class Test Prep: L17–L25 Comprehensive Summary

> Guest-lecture "advertising" slides (company intros, career pitches, team bios) have been stripped out.
> What's left is exam-relevant theory + the practical/industry content each guest actually taught, plus
> real-world application notes so you can answer "why" questions, not just "what" questions.

---

# L17 — Design Systems and CI

This lecture has two distinct halves: **(A) Design Systems** (brand/product design theory) and **(B) CI/CD Industry Best Practices** (a review of real mistakes seen in your mini-projects vs. what production pipelines actually do). The CI/CD half is the exam-heavy, application-heavy part.

## A. Design Systems

**The Golden Thread**: a continuous chain of decisions — Values → Voice → Visual → Patterns → Code. Break the thread anywhere (e.g. marketing says one thing, the UI looks like another) and the user feels the seam.

**Brand Style Guide vs. Design System** — the classic exam distinction:
| | Brand Style Guide | Design System |
|---|---|---|
| Nature | Strategic | Operational |
| Lives in | PDF / microsite | Code, Figma, Storybook |
| Contains | Mission, voice, tone, logo rules, colour palette | Design tokens, reusable components, patterns, versioning |
| Audience | Marketers, writers, designers | Designers, engineers, PMs |

**Design tokens** = named decisions (e.g. `color.action`) shared across Figma, CSS, Swift, Kotlin. Benefit: change the token once, every consuming platform updates. Naming by **role, not hue** (`color.action` not `color.blue`) means a rebrand doesn't require touching code.

**Atomic Design** (Brad Frost): Atoms (Button, Input) → Molecules (Search field) → Organisms (Header, Card) → Templates (page layout) → Pages (real content). Mirrors good software engineering: build small tested pieces, compose upward.

**A component is a contract**: e.g. a Button documents all its states (default/hover/active/focus/disabled/loading/danger/ghost), its props API, and accessibility requirements (real `<button>`, visible focus ring, `aria-label` if icon-only).

**Accessibility = POUR**: Perceivable, Operable, Understandable, Robust (WCAG). Not bolted on at the end — baked into every token/component.

### Real-world application
- When building your capstone frontend, define tokens (colours, spacing, type scale) once in a config/CSS-variables file instead of hardcoding hex values in every component — this *is* a mini design system.
- If your team has "three blues, five button styles" in the UI, that's the textbook symptom of no design system — the fix is a shared token file + component library (e.g. shadcn/ui, MUI theme).
- Exam angle: expect a "distinguish X from Y" question (Brand Style Guide vs Design System; Tokens vs. Components) or "explain why a design system improves maintainability/modifiability" (ties back to L11/L12 quality attributes — one source of truth = lower coupling in the UI layer).

## B. CI/CD Industry Best Practices

This section is a list of **anti-patterns actually seen in student projects**, each paired with the industry-correct approach. This is *very* testable because it's phrased as "problem → why it's wrong → fix."

### 1. CI must be a contract, not decoration
A green build should mean "mergeable." Ways students silently break this:
- `yarn test || true` — forces exit code 0 regardless of failures.
- `continue-on-error: true` at the workflow level.
- `jest --passWithNoTests` — an empty suite reports as passing.

**Fix**: never suppress failures; require the check.

### 2. Branch protection is where CI gets its teeth
A passing build with no *required* status checks is just a notification, not a gate.
- GitHub: Settings → Branches → require status checks (build, lint, type-check, unit, integration) before merge.
- Require linear history + review; no force-push to `main`.
- Rule of thumb: **if a check isn't required, assume it will eventually be ignored.**

### 3. "Integration tests" that mock the database aren't integration tests
Mocking Prisma/Supabase/the DB client only tests controller routing — it never exercises real SQL, migrations, transactions, or unique constraints.
**Industry pattern — Testcontainers**: spin up a real, ephemeral Postgres container in CI, run migrations, seed data, test against it, tear down.

### 4. "E2E tests" that intercept every network call aren't E2E
If Cypress/Playwright stubs every API response, you're testing your UI against your *imagination* of the backend. Real E2E hits a real deployed/local stack (real DB, real auth). Only stub genuine third parties you don't control in CI (e.g. Stripe).

### 5. A test that cannot fail is not a test
Vacuous patterns to watch for: `expect(true).toBe(true)`, missing `()` on `.not.toThrow` (a property reference that never runs), or asserting on brittle implementation details (CSS class names) instead of behaviour (what the user sees/what the API returns).

### 6. The testing pyramid (shape of a healthy suite)
```
        E2E          few · slow · highest fidelity
     Integration      real DB/services, in-process
        Unit          many · ms-fast · isolated logic
```
Unit tests catch the most bugs per second of CI time; integration tests catch wiring problems; E2E proves it works end-to-end but is slow/flaky, so keep it small. A suite shaped like an "ice-cream cone" (mostly E2E, few units) makes CI slow and unreliable.

### 7. Multi-stage Docker builds
Single-stage images ship the compiler/build tools/source/devDependencies into production — 2-3× the size and a bigger attack surface. **Fix**: build in a `builder` stage, copy only the compiled artefact into a slim `runner` stage.

### 8. Containers should never run as root
By default every process in a container is UID 0. If the container escapes its isolation (a container-escape CVE, e.g. runc/kernel bugs), a root container gives the attacker root on the host for free. Add `USER node` (or similar) — one line. Kubernetes' restricted PodSecurity and the CIS Docker Benchmark both reject root containers.

### 9. Secrets never belong in the repo
Plaintext DB passwords/JWT secrets in compose files get scanned continuously by bots (Shodan, GitHub scanning, script kiddies). **Fix**: inject secrets at runtime from a real secret store (GitHub Actions secrets for CI; Vault/AWS Secrets Manager/Doppler for prod). **Fail closed** — if a required secret is missing, crash on boot rather than falling back to a default (`postgres`/`admin`).

### 10. Pin your dependencies
`:latest` and even `node:20-alpine` are moving targets — the same Dockerfile builds a different image every week. **Fix**: pin to a content-addressed digest (`node:20.11.1-alpine3.19@sha256:...`) for reproducible builds; pin GitHub Actions to a commit SHA, not `@v4`. Renovate/Dependabot keep pinned digests updated via PR.

### 11. Resource limits + health checks
No memory limit → one leaking container can OOM the whole host. No health check → orchestrators think the container is "ready" the instant it starts, not when it's actually serving traffic. **Liveness** (am I alive?) and **readiness** (am I ready for traffic?) are separate checks in Kubernetes.

### 12. Build once, promote the same artefact
Anti-pattern: rebuild the image separately for staging and production — the thing you tested isn't the thing you shipped. **Fix**: build one immutable image tagged by git SHA, promote *that exact digest* through environments (never `:latest`). Scan (`trivy`/`grype`), sign (`cosign`), and generate an SBOM (`syft`) before promotion.

### 13. Supply-chain security
- **SBOM** (Software Bill of Materials): a machine-readable inventory of every dependency — required by US Executive Order 14028 for federal vendors.
- **Image signing** (cosign) stops registry tampering.
- **Dependency scanning**: Dependabot/Renovate (source deps), Trivy/Grype (container images) — run on every PR, block on Critical CVEs.
- **Commit lockfiles** (`yarn.lock`, `package-lock.json`) — without them, two builds an hour apart can silently pull different transitive dependency versions.
- Real incidents to remember: SolarWinds (2020), event-stream npm (2018), xz-utils backdoor (2024).

### The full healthy pipeline
```
Lint + Type-check → Unit → Integration + Build → Scan + Sign → Deploy (staging → prod)
```
Every stage runs on every PR and is a required check. The image is built **once** (in the integration stage), scanned/signed, then that exact digest is promoted — never rebuilt. If a stage flakes, fix or quarantine the test; never add `continue-on-error`.

### Real-world application
- Directly usable in your capstone: set up GitHub branch protection, add a Testcontainers-based integration test, write a multi-stage Dockerfile, add `USER node`, and never commit a `.env` with real secrets.
- Exam angle: expect a scenario question like "a team's CI is green but bugs reach production — list 3 possible causes and fixes" → pull straight from the anti-pattern list above (suppressed failures, mocked integration tests, no required checks).

---

# L18 — Domain Modelling and Architectures

## A. Domain Modelling recap

**Core building blocks**: Class (abstraction/type), Attribute (property), Operation (behaviour), Object (instance), Encapsulation (bundling data+behaviour), Polymorphism (many forms).

**UML class diagram vs. domain model**: a class diagram is a structural diagram showing classes, attributes, operations, and relationships. A **domain model is a class diagram without the operations** — it shows *what things are and how they relate*, not *what they do*.

**Relationship summary (classic exam table)**:
| Relationship | Notation | Meaning |
|---|---|---|
| Inheritance (IS-A) | arrow points from subclass to superclass | Employee → Manager |
| Aggregation (part-of, shared) | diamond at aggregate side | Car ◇— Engine |
| Composition (part-of, exclusive ownership) | filled diamond, part cannot exist without whole | Building ◆— Room |

**Domain modelling process (4 steps)**:
1. Collect application-domain information (functional requirements, business descriptions).
2. Brainstorm — list concepts, attributes, relationships.
3. Classify into classes / attributes / relationships (association, inheritance, aggregation).
4. Visualize using a UML class diagram.

**Bad domain model pitfalls (symptom → root cause table)**:
| Symptom | Actual cause |
|---|---|
| Every feature touches 10 files | Boundaries drawn around database tables, not concepts |
| Two devs use the same word differently | Vocabulary is technical, not the language users actually use |
| "Ship quickly" but the codebase says no | Rules scattered across services/helpers |
| Bugs cluster in the same area for months | Data flow modelled, behaviour ignored |
| Rewrites keep getting pitched | Architecture chosen before the domain was understood |

**Entity vs. Value Object — the identity test**: *"If I changed every field, would it still be the same thing?"* Yes → **Entity** (has an ID, e.g. `Customer` — can change email and remain the same customer). No → **Value Object** (no ID, interchangeable, e.g. `Money` — R100 is R100; you replace it, you don't mutate it; equality compares fields, not identity).

## B. Architecture recap (styles/decomposition)

**Definition**: Software architecture is the fundamental organization of a system — the high-level blueprint of structures, components, and relationships that meets technical *and* business requirements. **An architecture is technology-neutral** — no framework/vendor names belong in an architecture diagram.

**Four concerns of architecture**: Structural elements (modules/subsystems/DBs), Communication (APIs, messaging, data buses), Quality attributes ("ilities" — scalability, maintainability, security, reliability), Trade-offs (speed of dev vs. performance, etc.).

**How to choose an architecture — 4 diagnostic questions**:
1. How well do you understand the domain? Unclear → monolith. Stable → start splitting.
2. How many teams work on it concurrently? 1-2 → one deployable. 5+ → microservices may pay off.
3. Where's the read/write asymmetry? Roughly equal → same model. Reads >> writes → consider CQRS.
4. Does history matter as much as current state? Audit/finance/healthcare → event sourcing earns its place.

**Architectural styles (know the mechanism, not just the name)**:
- **N-Layer (horizontal decomposition)**: organizes concerns into logical layers (Presentation, Business, Data). Layers only talk to *adjacent* layers → good modifiability, independent development.
- **N-Tier (vertical decomposition)**: same idea but tiers are **physically separated** (e.g. 3-tier: client, app server, DB server on different machines).
- **Microservices**: decentralized control — small autonomous services communicating over REST/gRPC; independent deployment per service.
- **Event-Driven Architecture**: asynchronous — producers publish events, consumers subscribe. Pros: true decoupling, add consumers without touching producers, buffers absorb spikes. Cons: eventual consistency by default, harder cross-service debugging/tracing, schema evolution is hard once many consumers depend on event v1. Use when: high-throughput pipelines, multiple consumers care about the same fact, you want to add capability later without redeploying.
- **SOA**: interoperability via an Enterprise Service Bus, coarse-grained services (compared to microservices), often SOAP/WSDL with formal contracts.
- **CQRS**: separates read (Query) from write (Command) operations — allows independent scaling and different data models per side. Fits: read patterns wildly different from write patterns, reporting/dashboards crushing the OLTP DB, audit/history matters. Doesn't fit: plain CRUD apps, teams uncomfortable with eventual consistency, no proven bottleneck yet.
- **MVC**: Model (data + business logic, notifies view of changes) / Controller (receives input, updates model, picks view) / View (renders model into UI).
- **MVVM vs MVT**: MVVM (ViewModel, data-binding, client-side — Angular/Vue/React) vs MVT (View acts like a controller, server-side — Django).

### Real-world application
- When designing your capstone's database + API, sketch the domain model **before** picking a framework — this catches vocabulary mismatches early (e.g. does "Customer" mean the same thing to frontend and backend teams?).
- Use the Entity/Value Object test on your actual data: things with IDs and mutable state (User, Order) are Entities; small immutable descriptive values (Address, Money, DateRange) should be Value Objects — this directly improves your class design and avoids anemic/bloated models.
- Exam angle: expect a diagram-labelling question (identify aggregation vs composition), a "classify this as Entity or Value Object and justify" question, and a "which architectural style fits this scenario and why" style question (this connects directly into L22's structured method).

---

# L19 — Software Testing in Practice

(Guest lecture, but the testing content is directly exam-relevant — anchored in a real "horror story.")

## The horror story: what goes wrong without testing
An HR portal deployed with no local dev environment, painfully slow releases, and issues only caught in production. Root causes: business logic tightly coupled to the platform, inefficient dev environment, hard to collaborate as a team, negative compounding effect (small problems snowball).

**Lesson**: your reputation is tied to software quality; the hard part of engineering isn't writing code once, it's *keeping it working as it changes over time*. Automated tests would have: caught issues early, forced abstraction of external dependencies, sped up dev-environment iteration, prevented teammates' changes from silently breaking each other's code.

## Testing attitude
Good tests **accelerate** development rather than slow it down: fast feedback loop, safe refactoring, keeps a growing codebase maintainable. **Tests are not an afterthought — they are development.**

## Testing levels (know these definitions cold)
- **Unit** → does this one piece of logic do what it claims?
- **Integration** → do these pieces work together?
- **Functional** → does this feature behave as intended?
- **E2E** → does the whole user journey work, from the user's perspective?
- **Load** → does it hold up when real user volume shows up?

## Implementation practices
- Design code to be testable (small, decoupled units).
- Name tests so the name alone tells you what failed — tests double as living documentation.
- **Code coverage**: a metric for how much code is executed by tests (line/branch coverage). High coverage ≠ good tests, but low coverage is a red flag.

## Test-Driven Development (Red-Green-Refactor)
1. Write a failing test (**Red**).
2. Write the minimum code to make it pass (**Green**).
3. Clean up the code (**Refactor**).
Benefit: eliminates premature optimisation — you only build what's needed to satisfy a real requirement.

## Testing strategy
- **Continuous Integration**: tests run on every code change; PRs cannot merge unless tests pass.
- **User Acceptance Testing (UAT)**: not everything can be automated — humans break things in unexpected ways; catching it in UAT beats catching it in production.
- **Advanced**: Smoke tests (verify critical paths post-deploy), Feature flags/dark features (ship code without exposing it — decouples deploy from release), Canary releases (expose to a small % of users first to reduce risk / gauge reaction).

### Real-world application
- Adopt TDD for at least the tricky business-logic parts of your capstone (e.g. pricing/validation rules) — write the test describing the expected behaviour first.
- Name your tests descriptively: `should_reject_booking_when_seat_already_taken` not `test1`.
- Use feature flags if your capstone has a risky feature you want to deploy without immediately exposing to all users.
- Exam angle: "explain the levels of testing and give an example each" or "explain TDD and its benefit" are classic short-answer questions; also expect application questions asking you to classify a given test snippet by level (unit/integration/E2E).

---

# L20 — Designed for Humans (UI/UX for Developers)

## Why this matters to developers
Developers default to asking "does it work / is it fast / are the features there," but users experience the *feel* of software. Good design is invisible; bad design is frustrating enough that users quit.

**Properties of a good product**: Useful + Usable → Desirable → great user experience.

## Designing usable products ("Don't Make Me Think")

**User-centred mindset** (the biggest shift): stop thinking about how the system works internally; start thinking about the user's goal. Move from the **implementation model** (how the code works) to the **user's mental model** (how the user *thinks* it works). Your product is not the goal — the user's goal is.

**Constraints**: prevent invalid actions before they happen rather than showing an error after (e.g. a date picker instead of a free-text date field that can be typed wrong). Reduces confusion and decision effort, makes the interface feel safer.

**Discoverability**: make possible actions visually obvious so users don't have to stop and think, and can predict what will happen before clicking (e.g. clearly-labelled icon buttons vs. mystery icons).

**Feedback**: every action needs a visible response (skeleton screens while loading, spinners on click, confirmation after completion). Users shouldn't have to remember state — the interface should show it.

**The Paradox of Choice**: intuitively "more options = more freedom," but in practice more options → fewer actions taken → less effective power for the user. Fix: **progressive disclosure** — show only the most relevant choices, reveal more on demand.

## Designing desirable products ("Make It Easy on the Eyes")

- **Hierarchy**: create structure via spacing, size, weight, colour. If everything is emphasized, nothing is.
- **Whitespace**: gives the interface room to breathe; groups related content.
- **Proximity/ambiguous spacing**: related items should be spaced closer than unrelated items (a subtle but common exam/practical point).
- **Typography**: pick 1-2 fonts that pair well; line-height ~1.3–1.5× for body text (too tight = 1.0×, too loose = 2.0×); keep line length to roughly 50-80 characters — long unbroken lines hurt comprehension.
- **Colour**: use sparingly with a limited palette; ensure contrast — WCAG AA requires 4.5:1 for normal text, 3:1 for large text (AAA is stricter: 7:1 / 4.5:1).
- **Style guides**: limit choices → easier decisions → faster, more consistent development (this directly connects back to L17's Design Systems).

### Real-world application
- Concretely apply this to your capstone: add loading spinners/skeletons for async actions, use a consistent 4px/8px spacing scale, run your colour choices through a contrast checker (e.g. WebAIM), and constrain form inputs (date pickers, dropdowns) instead of free text where the format matters.
- Progressive disclosure example: don't show 15 filter options by default in a search UI — show 3 common ones plus an "advanced filters" toggle.
- Exam angle: definition/short-answer on "user-centred design," "the paradox of choice," or "why constraints improve usability" — and possibly a "critique this UI screenshot" style application question, since much of this lecture is visual comparisons (bad vs. good example side-by-side).

---

# L21 — DevOps and DevSecOps

This lecture is largely diagram-driven (the pipeline stages appear as visuals in the slides), so combine the slide skeleton below with the standard industry definitions.

## DevOps
**Definition**: DevOps combines **Dev**elopment and IT **Op**erations into one continuous, collaborative lifecycle, aiming to shorten the development cycle and deliver features/fixes/updates frequently and reliably, in close alignment with business goals.

**The DevOps lifecycle (8 steps, as presented)**:
1. **Plan** — define requirements/backlog.
2. **Code** — write the software.
3. **Build** — compile/package the code (this is where CI's build stage lives).
4. **Test** — automated tests (unit/integration/E2E — ties directly to L17 & L19).
5. **Release** — package a versioned, deployable artefact.
6. **Deploy** — ship the artefact to an environment (this is the CD half — Continuous Delivery/Deployment).
7. **Operate** — run the system in production.
8. **Monitor** — observe logs/metrics/traces; feed learnings back into Plan (the loop closes — this is why it's usually drawn as an infinity loop).

Key DevOps principles: automation at every stage, infrastructure as code, fast feedback loops, and shared ownership between developers and operations (no more "throw it over the wall to Ops").

## DevSecOps
**Definition**: extends DevOps by embedding **security** as a first-class, continuous concern across the *same* lifecycle, rather than as a final gate before release ("shift-left security").

Core idea: security checks run automatically and early — in the same pipeline as build/test — rather than being a manual audit performed right before (or after) deployment. Typical tooling that fits into each stage:
- **Plan/Code**: threat modelling, secure coding guidelines, IDE security linting.
- **Build**: **SCA** (Software Composition Analysis — scanning dependencies for known CVEs, e.g. Dependabot/Snyk), secret scanning.
- **Test**: **SAST** (Static Application Security Testing — scans source code without running it) and **DAST** (Dynamic Application Security Testing — attacks a running instance, e.g. OWASP ZAP).
- **Release/Deploy**: container image scanning (Trivy/Grype — same tools from L17), image signing (cosign), infrastructure-as-code scanning.
- **Operate/Monitor**: runtime security monitoring, intrusion detection, incident response.

### Real-world application
- The 8-step DevOps loop is literally the shape of a mature CI/CD pipeline — map your own capstone pipeline stages onto it (Plan = your sprint backlog, Build/Test = your GitHub Actions workflow, Deploy = your hosting platform, Monitor = your logging/error tracking).
- DevSecOps in practice for a student project: enable Dependabot (SCA), add a `trivy` scan step to your CI (from L17), and never commit secrets (also from L17) — these three items alone demonstrate shift-left security.
- Exam angle: expect to be asked to name and order the DevOps lifecycle stages, define DevSecOps vs DevOps, and possibly map a security tool (SAST/DAST/SCA) to the correct pipeline stage.

---

# L22 — Practical Architectural Design

**This is explicitly flagged in the slides as exam-critical**: *"This will be in your semester test. The walkthrough at the end is the exact format of the 15-mark question."* Master this lecture's 7-step method above all else.

## The Two Laws
- **First Law**: *Everything in software architecture is a trade-off.*
- **Second Law**: *The "why" is more important than the "how."*
(Richards & Ford, *Fundamentals of Software Architecture*)

The job of an architect: turn fuzzy requirements into testable targets, make and record defensible decisions, communicate them to different audiences, keep them alive against drift, and evolve inherited systems.

## The 7-step chain (learn this table — it's the whole exam)

| # | Step | Question it answers |
|---|------|----------------------|
| 1 | **NFR** | What must be true, as a *number*? |
| 2 | **Quality attribute** | Which "-ility" is it? (decides which tactics are candidates) |
| 3 | **Tactic** | What is the design move? (still technology-free) |
| 4 | **Pattern** | What *named structure* implements that move? |
| 5 | **ADR** | What did you decide, what did you reject, what trade-off did you accept? |
| 6 | **Architectural design** | The diagram, for whoever has to act on it |
| 7 | **NFR test** | What automated check keeps it true after you stop looking? |

Rows 1 and 7 are a pair: the test is the NFR turned back into a question. *If you cannot write row 7, row 1 was never a real requirement.*

### Step 1 — Quantify: "scalable" is not a requirement
You cannot design against, or test, "the system must be scalable." Everything must become a measurable number (e.g. "200ms → 5s checkout latency during a flash sale").

**The six-part quality attribute scenario** (memorize this structure):
1. Source of stimulus
2. Stimulus
3. Environment
4. Artifact
5. Response
6. Response measure ← this is what makes it testable and derives your SLO.

### Step 2 — Which "-ility"? (ISO 25010 characteristics)
Functional suitability · Performance efficiency (time behaviour / resource utilisation / capacity) · Compatibility · Interaction capability (was "usability") · Reliability (faultlessness, availability, fault tolerance, recoverability) · Security (confidentiality, integrity, accountability, authenticity, resistance) · Maintainability (modularity, reusability, analysability, modifiability, testability) · Flexibility (adaptability, scalability, installability, replaceability) · Safety (new in 2023).

**Two exam traps**:
- "Scalable" is *not* performance — since the 2023 ISO revision, **scalability sits under Flexibility**, not Performance efficiency.
- "Fast" and "fits in 1GB" are two *different* sub-characteristics (time behaviour vs. resource utilisation) → two separate requirements, two separate tests.

**The utility tree**: refine a business driver down to a measurable, tagged (importance, difficulty) leaf. (H,H) items are where your real design effort/trade-offs go; (H,L) you just do; (L,H) you push back on — don't spend a year on something the business doesn't need.

### Step 5 — The Architecture Decision Record (ADR, Nygard 2011)
Structure: **Title + status** (proposed → accepted → superseded-by) · **Context** (the problem, forces, alternatives considered) · **Decision** (crisp enough to check compliance) · **Consequences** (trade-offs, *including the negative ones* — "an ADR with no downsides is marketing, not engineering"). Lives in the repo, version-controlled next to the code.

**What a bad ADR looks like**: "Decision: we will use Kafka. Consequences: better scalability." → nothing checkable, no negative consequences, no alternatives considered. You must be able to defend a choice you actually compared against others.

**Industry practice — the design review**: nearly every major tech org (Amazon, Airbnb, LinkedIn, Spotify, Uber, Monzo, GitLab) reviews architecture as written RFCs/design docs: draft → seniors comment → revise → ratify into an ADR. The value is in the comment/revise loop.

### Step 3-4 — Why tactics exist: The Eight Fallacies of Distributed Computing (Deutsch et al., 1994)
1. The network is reliable
2. Latency is zero
3. Bandwidth is infinite
4. The network is secure
5. Topology doesn't change
6. There is one administrator
7. Transport cost is zero
8. The network is homogeneous

Every one is false and still causes outages. Map fallacy → tactic: e.g. "network is reliable" → retries + idempotency, circuit breakers, dead-letter queues; "latency is zero" → caching, coarse-grained requests; "network is secure" → zero trust, service-to-service auth; "one administrator" → version internal APIs, contract tests.

**What ignoring them produces**: the **distributed monolith** (separately deployed but tightly coupled — all the cost of microservices, none of the benefit); **premature distribution** (splitting before the domain is understood just spreads your problems across a network — Fowler's "monolith-first"); **the operational tax** (day-one microservices can burn ~40% of engineering time on infrastructure rather than features, worst when the team is smallest). Pragmatic default: **modular monolith** with clean internal boundaries until scale (or Conway's Law) forces a split.

### Step 4 — Tactic vs. Pattern (the distinction the exam loves)
A **tactic** is a technology-free design decision addressing one quality attribute (usually one sentence, e.g. "cache the read path"). A **pattern** is a *named, reusable structure* that implements one or more tactics (patterns are "bundles of tactics" — Bass). The tactic follows almost automatically from the quality attribute; the pattern follows from *your* context, so it's the actual choice you argue about and record in the ADR.

| Tactic | Patterns that implement it |
|---|---|
| Cache the read path | Cache-aside · Read-through · Write-through · Refresh-ahead (+ Proxy/Decorator) |
| Tolerate a failing dependency | Circuit Breaker · Bulkhead · Retry with backoff · Fallback |
| Decouple producer from consumer | Queue · Publish-Subscribe · Observer |
| Isolate the volatile part | Adapter · Strategy · Dependency Inversion |
| Restrict what may call what | Layers · package boundary with public API · Facade |

Common mis-map trap: the **State pattern** varies behaviour by internal state — it is *not* a cache-consistency pattern (that's cache-aside/write-through + invalidation).

### Step 5 continued — Sensitivity points, trade-off points, risk
- **Sensitivity point**: a property critical to *one* quality attribute — a yellow flag, change with caution.
- **Trade-off point**: a sensitivity point for *more than one* attribute — turning it up helps one, hurts another (e.g. Cache TTL improves time-behaviour/DB load but degrades consistency; Retry count improves fault tolerance but degrades latency/duplicate risk; Layers of abstraction improve modifiability/testability but degrade simplicity/performance).
- **Risk**: a potentially problematic decision, or one not yet made.
- **Non-risk**: a good decision resting on an assumption — stays a non-risk only while the assumption holds.

*None of the trade-off knobs has a single "correct" setting — the ADR's consequences section is the record of which side you chose and what you accepted in exchange.*

### The worked exercises (this IS the semester-test format — practice all three types)
- **Exercise A (Reliability)**: "must not lose bookings when the payment gateway goes down" → Circuit Breaker + Bulkhead (isolate the failing dependency) + Queue with idempotency key (defer work) + Retry with backoff behind the breaker.
- **Exercise B (Security)**: "user payment data must be protected" (POPIA) → strongest answer is usually **"we do not hold the data"** — tokenisation with a vault, an Adapter isolates all crypto/token code, RBAC on the rest. The diagram's *absence* of an arrow carrying card data into your system boundary IS the security design.
- **Exercise C (Maintainability/Modifiability)**: "add a new payment provider quickly" → interface/Adapter per provider + Strategy to select at runtime + dependency inversion (domain never imports a provider SDK directly). The forbidden arrow (domain package → provider package) must never appear on the diagram — its absence is the design.

**General method for any NFR exam question**: (1) quantify it into a 6-part scenario, (2) name the ISO 25010 quality attribute + sub-characteristic, (3) name a technology-free tactic, (4) name the pattern(s) that implement it, (5) write a mini-ADR (decision + one real cost), (6) sketch what changes on the architecture diagram, (7) state an automatable test/fitness function that would catch a regression.

## Organizational reality
**Conway's Law** (1968): a system's structure mirrors the organization's communication structure — team boundaries *become* service boundaries whether you intend it or not. ("Team assignments are the first draft of the architecture" — Nygard.) **Inverse Conway maneuver**: reshape the teams first to get the architecture you want. **Cognitive load**: draw service boundaries a single team can actually hold in their head — overloaded teams slow down and make mistakes. "Should we use microservices?" starts with "how many teams do you have?"

**Other real-world constraints**: Cost (every tactic is a monthly bill — cost is itself a quality attribute), Time (defer what's cheap to reverse; decide early only what's expensive to reverse, e.g. data ownership, sync vs async boundaries), Team skill (tech your team can't operate at 2am is an availability decision), Compliance (POPIA — encryption is necessary but not sufficient; also need key management, auditing, access control), Legacy (most real work is inherited, not greenfield).

**The Strangler Fig pattern** (Fowler, 2004) — evolving inherited systems without a big-bang rewrite: (1) front the legacy system with a façade/indirection layer, behaviour unchanged; (2) replace one capability at a time, each cycle self-contained and reversible; (3) decommission the legacy once nothing routes to it. Real examples: Shopify (monolith → services while revenue grew $100M→$1B+), Netflix (datacenter → AWS). The catch: **data migration is the hardest part** of every slice.

## Enforcement — fitness functions
Documentation alone does not stop architectural drift; **running checks** do. A **fitness function** (from *Building Evolutionary Architectures*) is any automated check of an architectural constraint, run in CI next to your unit tests. Examples: ArchUnit rule ("no class in `web.*` may depend on `persistence.*`"), contract tests (a breaking API change without a version bump fails the build), a CI performance test asserting a latency budget. **Litmus test for any ADR**: "Can I describe what a violation looks like?" If yes, write the check.

## Synthesis case studies (memorize the pattern of these — they're model answers)
- **Netflix / Availability**: Circuit Breaker + Bulkhead + defined fallback for every remote call, historically implemented as Hystrix (now migrating to resilience4j — "they traded a mature library for a better fit and accepted the migration cost," an example of the First Law in action). Fitness function: Chaos Monkey randomly kills production instances to prove resilience continuously.
- **Shopify / Modifiability**: modular monolith with declared public APIs per package (L11's low coupling + information hiding, at package scale) rather than splitting into microservices. Fitness function: Packwerk, a static analyser checking dependency violations (coupling) and privacy violations (information hiding) — ~48 packages, ~30 enforced rules.

## Postscript: AI in architecture
Two points worth remembering: (1) an LLM component makes a previously deterministic system non-deterministic — that's now a quality-attribute problem you already have the vocabulary for (timeouts, fallbacks, validation layers, circuit breakers around model calls, a QAS for accuracy/latency). (2) AI accelerates the "how" but the "why" — the trade-off reasoning across code, infra, people, regulation, cost, failure — is still your job; that's precisely what an ADR captures.

### Real-world application
- Use the 7-step method on your **own capstone's** non-functional requirements right now — pick one ("the system must handle concurrent registrations," "user data must be secure") and walk it through NFR → quality attribute → tactic → pattern → ADR → diagram → test. This is exact exam practice *and* genuinely improves your project.
- Write at least one real ADR for your capstone (e.g. "why we chose PostgreSQL over MongoDB") including negative consequences — this is a skill "industry will pay you for," verbatim from the slides.
- Exam angle: **expect a 15-mark application question** giving you a vague NFR and asking you to walk the full 7-step chain, likely plus a short conceptual question on Conway's Law, tactic-vs-pattern, or fitness functions.

---

# L23 — Architecture in Practice (Case Studies)

Guest lecture with two real case studies applying architecture concepts to actual systems — useful for "how would you design X" application questions.

## General design considerations & best practices
**Design considerations** to weigh on every project: Security, Maintainability, Scalability, Reliability & Availability, Extensibility, Teams and collaboration.

**Best practices**:
- Determine non-functional requirements *early* (echoes L22 — quantify before you design).
- Architecture design first, technology choices later (architecture is tech-neutral, per L18).
- Avoid over-engineering.
- Consider the implementation team's structure (Conway's Law, per L22).

## Case Study 1 — Road Security System
**Domain**: license-plate lookups against a warning database; SAPS can subscribe to vehicle-sighting notifications.
**Success factors**: performance and scalability.
**Design challenges**: sub-second, asynchronous response times; scalability under increasing request volume; compatibility across varied client environments.
**Design decisions applied per concern**:
- Overall: high-performance, scalable, **event-driven architecture** (direct application of L18's EDA).
- Client communication: WebSockets (bi-directional, low-latency); clients choose their own tech stack.
- Connection handling at scale: thousands of simultaneous connections require certificate-based authentication and a **Redis cache** to share state across multiple instances of the communication service (classic horizontal-scaling problem — stateless instances + shared cache).
- Fan-out queries: one incoming request spawns parallel messages to multiple sources, tagged with a unique correlation ID so responses can be recombined.
- Notifications: sent in parallel to avoid impacting response times; new notification channels can be added as new services without touching existing ones (this is the **Open/Closed**-style extensibility you'd also justify via the Adapter/Strategy patterns from L22).

## Case Study 2 — Financial Services (multi-subsidiary org)
**Domain**: a large organisation with multiple subsidiaries needing a unified user experience across separate subsystems/data/security domains.
**Success factors**: maintainability, availability, resilience.
**Design considerations**: security & data protection, maintainability, resilience, availability (deployment/DevOps).
**Overall architecture**: highly-available, resilient, modular **service-oriented architecture**.
**Design decisions per concern**:
- Sensitive user data → Identity management + **Single Sign-On** across subsidiaries.
- Maintainability (multiple dev teams/subsystems) → modularisation / micro-frontends.
- Resilience (susceptible to integration failures) → caching, timeouts/retries/backoff strategies (straight out of L22's "tolerate a failing dependency" tactic).
- Availability (24/7 portal, cannot go down) → **blue/green deployment** strategy.

## Tools & Techniques
**Design & modelling tools**: UML, sequence diagrams, C4 Model, infrastructure diagrams.
**Why use them**: communicate structure/data/infrastructure/tech choices/scope; visualize system structure; identify risks *early*; ensure consistency across the solution.

### Real-world application
- Both case studies are essentially L22's 7-step method applied without the explicit table — practice re-deriving the table from a case study description (this is likely exam-question shaped: "given this scenario, identify the quality attribute, tactic, and pattern used").
- If your capstone needs real-time updates (e.g. notifications, live dashboards), the Road Security case study's WebSocket + Redis pattern is a directly reusable blueprint.
- If your capstone spans multiple modules/teams needing one login experience, the Financial Services case study's SSO + modular SOA approach applies directly.
- Use C4 diagrams (Context → Container → Component → Code) for your own capstone documentation — it's the industry-standard way to show "structure at the right level of abstraction" mentioned here and echoed throughout L22's diagrams.

---

# L24 — Security Testing

⚠️ This lecture (delivered by Integrity360, a cybersecurity company) was almost entirely a company/careers pitch with a live **Red Team vs. Blue Team** demo — there was minimal explicit theory slide content to extract. Below is the demo concept plus the standard security-testing theory you'll need to know for the class test (consistent with what a COS301 architecture/testing course expects and complementary to L21's DevSecOps).

## What was actually covered
- **Red Team vs. Blue Team live demo**: Red Team = attackers, simulating real-world adversarial attacks to find and exploit vulnerabilities. Blue Team = defenders, detecting, responding to, and mitigating those attacks in real time. This is the practical embodiment of **penetration testing** and **incident response**.
- Integrity360 profile: a managed security services provider covering the full cyber-risk lifecycle — identification, prevention, detection, response, recovery — across SOCs (Security Operations Centres) in multiple regions.

## Core security testing theory to know (standard industry knowledge, ties directly to L21's DevSecOps)
- **SAST (Static Application Security Testing)**: analyses source code without executing it — finds issues like SQL injection patterns, hardcoded secrets, insecure function use. Runs early (Build/Test stage of DevSecOps).
- **DAST (Dynamic Application Security Testing)**: tests a *running* application from the outside, simulating attacks (e.g. OWASP ZAP) — finds runtime issues SAST can't see (auth bypass, misconfigurations).
- **SCA (Software Composition Analysis)**: scans third-party dependencies for known CVEs (Dependabot, Snyk — same tools as L17's supply-chain security).
- **Penetration Testing**: authorized, simulated attack against a system to evaluate its security (what the Red Team demo represents) — can be black-box (no internal knowledge), white-box (full knowledge), or grey-box (partial knowledge).
- **Threat Modelling**: proactively identifying what could go wrong (assets, attackers, attack vectors) *before* building, to design defences in from the start (shift-left, same spirit as L21).
- **OWASP Top 10**: the standard reference list of the most critical web application security risks (e.g. injection, broken authentication, security misconfiguration) — commonly examinable as a concept even if not memorised item-by-item.
- **Red Team / Blue Team / Purple Team**: Red = offense, Blue = defense, Purple = collaboration between both to improve detection and response together.

### Real-world application
- For your capstone: run a free SAST tool (e.g. `npm audit`, Semgrep) and a dependency scan (Dependabot) — this is a concrete, gradeable way to demonstrate security testing practice.
- If handling any user data (even a login form), think like a threat modeller: what's the worst thing that could happen if this endpoint were abused (e.g. no rate limiting → brute force login)?
- Exam angle: expect this content to be tested lightly and generically (e.g. "what is penetration testing," "differentiate SAST and DAST," "what is the purpose of a Red Team exercise") rather than deep case-study application, given the guest lecture's thin slide content — but confirm with your own lecture notes/recording since the guest content was sparse in the deck itself.

---

# L25 — Service Contracts

## The problem it solves
**Integration Nightmare**: frontend and backend teams build separately; the night before a demo, nothing connects. Without an upfront agreement, teams rely on assumptions and "he said, she said" arguments about how the application should communicate.

## What is an API Service Contract?
A **formal agreement** that defines the rules, inputs, outputs, and behaviours, in a **machine-readable format**, for communication between software systems/components.

Two framings:
- **The Blueprint**: formally defines endpoint URLs, allowed HTTP methods, required payloads, and the exact shape of response data — eliminates guesswork.
- **The Agreement**: a strict agreement between backend provider and frontend consumer — if both sides adhere to it, integration works on the first try.

**Why use contracts (capstone-relevant benefits)**:
- **Parallel development**: backend and frontend work simultaneously; frontend uses mock data generated from the contract while the backend builds real logic.
- **Single source of truth**: eliminates arguments about endpoint behaviour — the written contract is the absolute authority on data structures.
- **Reliable testing**: enables automated **contract testing** to ensure neither side inadvertently breaks the agreement during later changes.

## OpenAPI vs. Swagger (classic exam distinction — don't mix these up)
- **OpenAPI**: the official, vendor-neutral **specification** — the rules for writing the API document (JSON/YAML). *It is the blueprint itself.*
- **Swagger**: a *suite of tools* (Swagger UI, Editor, Codegen) that process an OpenAPI spec to generate docs/interactive interfaces.
- **Analogy given in lecture**: OpenAPI is like the universal USB-C standard; Swagger is a specific brand of tools that use that standard.
- You *write* an OpenAPI file; you *view/use* it with Swagger tools.

## Anatomy of an OpenAPI document
- **Paths & Operations**: defines specific endpoints (e.g. `/users`, `/orders`), the HTTP method (GET/POST/PUT/DELETE), and required query params/path variables/security headers.
- **Components & Schemas**: reusable data models (e.g. a `User` object must contain an integer `id` and string `email`) — guarantees data integrity, prevents malformed exchanges.

Minimal example structure:
```yaml
openapi: 3.0.4
info:
  title: Sample API
  version: 0.1.9
servers:
  - url: http://api.example.com/v1
paths:
  /users:
    get:
      summary: Returns a list of users.
      responses:
        "200":
          description: A JSON array of user names
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
```

## Mock Servers
A **mock server** is a simulated backend automatically generated from the API contract (e.g. from an OpenAPI spec). The frontend sends requests to it and receives predefined example responses conforming to the agreed contract — this is *how* parallel development actually works day-to-day.

## Contract-First vs. Code-First
| Contract-First | Code-First |
|---|---|
| Design API first | Write backend first |
| Frontend can start immediately | Frontend waits |
| Better collaboration | Easier for small/solo projects |
| Preferred for teams | Common for prototypes |

## Integration Workflow (4 steps — likely diagram/labelling question)
1. **Design** — team agrees on the API contract before writing any code; write the OpenAPI YAML together.
2. **Mocking** — frontend uses tools like Swagger to mock backend responses and starts building UI immediately.
3. **Development** — simultaneously, backend builds actual server logic to fulfil the agreed contract.
4. **Integration** — because both teams strictly followed the blueprint, connecting frontend to backend is seamless.

## Breaking the Contract → Versioning
Changing the contract means everyone depending on it must update. **Use versioning** to avoid breaking existing consumers:
```
// GET /v1/users          // GET /v2/users
{ "name": "Alice" }       { "fullName": "Alice" }
```

## Capstone Best Practices (directly from the slides — likely to appear as a "list best practices" question)
- **Design-first**: never write the backend then generate the contract as an afterthought — design the API, agree on it, *then* implement.
- **Version control**: store `openapi.yaml` in your main Git repo, treat it as critical production code.
- **Descriptive errors**: define standard error formats (400 Bad Request, 404 Not Found) in the contract so the frontend can catch and display helpful messages.
- **Communicate changes**: if the backend must alter the contract, the frontend team must be consulted and agree *beforehand*.

### Real-world application
- This is the single most directly-applicable lecture to your capstone group project: write an `openapi.yaml` for your team's API *before* either side starts coding, commit it to your repo, and use a mock server (or a tool like Prism/Swagger UI) so frontend work isn't blocked on backend progress.
- When you need to change an endpoint's response shape later, version it (`/v2/...`) instead of silently breaking existing frontend calls — this is also a **fitness function** concept from L22 (contract tests failing the build on an unversioned breaking change).
- Exam angle: expect a "differentiate OpenAPI and Swagger" question, a fill-in-the-integration-workflow-steps diagram question, and possibly a short scenario ("two teams are integrating late and things break — what practice would have prevented this?").

---

# Cross-Lecture Threads (things that connect L17–L25 — great for synthesis/essay questions)

- **The 7-step method (L22)** is the backbone that L18 (architecture styles feed step 3-4), L23 (case studies are worked examples of the method), L19 (testing = step 7's NFR test), L17 (CI/CD enforces step 7 automatically), and L21 (DevSecOps embeds security NFR tests into the pipeline) all plug into.
- **"Technology-free until step 3/4"** (L22) mirrors L18's "an architecture is technology-neutral."
- **Fitness functions (L22)** = the conceptual umbrella over L17's required CI checks, L21's automated security scans, and L25's contract tests — they're all "automated checks that keep an architectural/contractual decision true over time."
- **Conway's Law (L22)** explains *why* L18's microservices-vs-monolith choice is really an org-design question, and why L23's Financial Services case study needed modular/SOA boundaries matching subsidiary team structure.
- **Design Systems (L17) and UI/UX (L20)** are two halves of the same idea: L20 is the *principles* (usability, discoverability, hierarchy), L17 is the *system* that encodes those principles as reusable, enforceable tokens/components.
- **Security is threaded through everything**: L17 (secrets, supply chain), L21 (DevSecOps shift-left), L22 (Exercise B — "we do not hold the data"), L24 (security testing/pen testing), L25 (contract-defined error handling avoids leaking internals).

---

# Suggested Study Priority (given your CT covers L17–L27)

1. **L22** — highest priority; explicitly stated to match the semester-test format. Practice the 7-step method on 3-4 different made-up NFRs until it's automatic.
2. **L18** — foundational vocabulary (entity/value object, architectural styles) that L22 and L23 both assume you already know.
3. **L17 (CI/CD half) and L25** — very concrete, very examinable, very capstone-applicable (likely to appear as scenario/best-practices questions).
4. **L19 and L20** — solid conceptual short-answer material (testing levels, TDD, usability principles).
5. **L21** — know the 8-stage DevOps loop and the DevOps vs DevSecOps distinction cold; the rest is largely diagram recall.
6. **L23** — practice re-deriving L22's table from these case studies; useful worked examples more than new theory.
7. **L24** — lightest guest-lecture content; know the standard definitions (SAST/DAST/pen testing/Red-Blue team) as a safety net, but don't over-invest here relative to L22/L18.
