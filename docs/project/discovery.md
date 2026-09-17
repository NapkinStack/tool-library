---
decision: go                # proposed | go | clarify | kill — the decider decides
decider: "@napkinstack-admin" # the human who decides, recorded at intake
decided_on: 2026-09-18      # YYYY-MM-DD, with the decision
challenger: "agent session — Claude Opus 5, challenger posture (playbooks/discovery.md §5)" # stage 5: @human, or the agent session — required for a go
idea: "docs/project/inputs/tool-library-idea.en.md"         # the idea as given, kept in docs/project/inputs/
round: 1
---

# Discovery

> Started by the engine's `discover` command, run by your agent (`playbooks/discovery.md`).
> One document, a decision at the end of each round.

## 1. Intake

> **Confirmed** by @napkinstack-admin, round 1: "confirmed as written, nothing to correct".

For people who live in the same neighbourhood — presumably in France, since the idea was
written in French — and who now and then need a tool they do not own: the tool is often
already a few doors away, asleep in a garage, but nobody knows which garage, and asking
around reaches only the neighbours one already talks to, so the neighbour buys the tool or
rents it instead. The product is a simple shared list for one neighbourhood: a neighbour
publishes a tool they are willing to lend, another neighbour sees what is available nearby,
the two agree between themselves on a date for the loan and a date for the return, and the
product keeps a clear record of who holds what and since when. No money changes hands and
nothing is delivered: what carries the exchange is the trust between neighbours who can
already recognise each other, and a history that makes an unreturned tool visible.

**Answered at intake** — @napkinstack-admin, round 1:

1. *Is the restatement right?* — Confirmed as written, nothing to correct.
2. *Which country, which neighbourhood?* — France, open to any neighbourhood: anyone can
   open theirs, with no invitation.
3. *Who runs it?* — The decider, personally.
4. *Is "no money" a principle?* — A starting point, not an unbreakable rule: a paid model
   stays possible later, by membership or with a municipality's support.

**Open questions:** none remaining at intake.

## 2. Research

**Tools used** — the research rows of `docs/tooling-profile.md` are empty, so, as the
playbook allows, the tools at hand: Claude Code's **WebSearch** (web search) and
**WebFetch** (fetch a page and read it), in September 2026. No other research tool was used,
and no paid database. Primary sources are quoted where they could be reached:
Légifrance, EUR-Lex, YouGov, the alternatives' own sites. Four sources could not be read and
are noted under *Assumptions*.

Marking: **(self-reported)** a figure a company publishes about itself · **(excerpt)** a
claim seen only in a search excerpt or a secondary article, primary source not reached.

| Claim | What it changes for the idea | Source |
|---|---|---|
| **Today** — Asked whether they would ask a next-door neighbour to borrow something such as a tool or an ingredient, 24 % of US adults say very likely and 29 % somewhat likely; 19 % not very and 21 % not at all (35 878 adults, 18 March 2024) | The competitor is not "nothing", it is asking directly — the product has to beat a knock on the door. And about 40 % would not ask at all: that is the ceiling of the neighbourhood, not a discovery problem | [YouGov Daily Question, 18 Mar 2024](https://yougov.com/en-us/daily-results/20240318-75fbc-2) |
| **Today** — 89 % of French people say they would give an hour a month to help a neighbour and 87 % think neighbourhood solidarity matters (BVA fieldwork 6–10 May 2019); a secondary article reports over 75 % gave or received a neighbourly service in the year, "lending a tool" among them **(excerpt)** | Willingness is not the constraint; the constraint is knowing who has what. The idea addresses discovery, not goodwill — so the product must be judged on whether it surfaces tools, not on whether neighbours are nice | [BVA Xsight, Les Français et les relations de voisinage](https://www.bva-xsight.com/sondages/francais-relations-de-voisinage/) · excerpt: [voisinsvigilants.org](https://www.voisinsvigilants.org/actualites/pourquoi-sentendre-avec-ses-voisins-change-la-vie-au-quotidien) |
| **Today** — Renting is cheap and immediate: Leroy Merlin about €10/day for a cordless drill and €38–39/day for a pressure washer; Kiloutou lists drills from €4/day, insurance included **(excerpt)** | For a cheap tool, the money saved is small: the switch has to come from proximity and immediacy, not from price. Rental also ships with insurance, which a neighbour loan does not | [Leroy Merlin location de matériel](https://www.leroymerlin.fr/services/location/location-de-materiel/) · [Kiloutou, location perceuse](https://www.kiloutou.fr/c/perceuse/) |
| **Today** — Nextdoor reports 110 million verified neighbours across 350 000 neighbourhoods, an 80 % rise in monthly listings on its buy/sell/give product since the start of 2020, and 25 % of items listed as free **(self-reported)** | The generic neighbourhood app already carries free-item traffic where it exists. What it does not model is a *return* — the idea's distinct object is the loan with two dates and a history, not the listing | [Nextdoor press release, Free Finds](https://about.nextdoor.com/press-releases/nextdoor-expands-its-buy-sell-and-give-feature-with-the-launch-of-free-finds) |
| **Alternatives** — Tool libraries exist and are cheap: over 140 worldwide as of 2023; in France, *outilthèques* typically charge €5–10 membership (Paris as low as €6/year), borrowing free or €1–5 for larger kit **(excerpt)** | A neighbourhood that wants shared tools has an institutional option already, with one owner, one place and maintenance. The idea's claim has to be that no single place or budget is needed | [Grassroots Economic Organizing, The Evolution of the Tool Library](https://geo.coop/story/evolution-tool-library) · [Ville de Paris, 5 lieux où emprunter des outils](https://www.paris.fr/pages/5-lieux-ou-emprunter-des-outils-a-paris-26692) |
| **Alternatives** — Peerby (NL, since 2011) is the closest existing product: borrow from neighbours, free for members who also offer items, about €19/year for borrow-only membership; it reports profitability, 1 in 4 Amsterdam households as members and over 500 000 shared products **(self-reported)** | The idea has been built and it works — but only after a 2017 near-failure and a pivot to paid membership in 2019. Free-for-everyone is precisely the version that did not hold | [Peerby newsroom](https://press.peerby.com/214840-peerby-profitable-raises-2-3-million-euros/) · [Silicon Canals, 2022](https://siliconcanals.com/peerby-bags-2-3m/) |
| **Alternatives** — France already has a paid peer-to-peer tool marketplace: Bricolib, listing free, commission on rentals, claiming 148 000+ members and 80 000+ tools, and about €480/month average for an owner **(self-reported)** | In France the "lend your tool to a neighbour" slot is taken by a *paid* product. The idea's differentiator is therefore the absence of money, not the listing — and that has to be worth something to a user | [bricolib.net](https://bricolib.net/) |
| **Alternatives** — AlloVoisins (FR, 4 million members) monetises by freemium subscription and removed its 15 % transaction commission | The French leader in neighbour-to-neighbour services concluded that taking a cut of each exchange does not work. A no-money product is closer to the direction of travel than it looks | [Le Journal des Entreprises](https://www.lejournaldesentreprises.com/article/allovoisins-supprime-les-commissions-pour-ses-4-millions-de-membres-1889375) |
| **Alternatives** — Library of Things (UK) rents from kiosks at £1/day for hand tools up to about £20/day for a carpet cleaner, with a 25 % low-income discount, part-funded by London councils' carbon-offset funds | An alternative that removes peer risk entirely: one owner, many borrowers, public money. If the neighbourhood's real problem is trust and breakage, this model beats peer-to-peer | [Library of Things, How Borrowing Works](https://www.libraryofthings.co.uk/how-borrowing-works) · [Brighton & Hove City Council](https://www.brighton-hove.gov.uk/news/2022/why-buy-when-you-can-borrow-free-library-things) |
| **Alternatives** — Software to run exactly this already exists: myTurn (used by 130+ lending libraries), Lend Engine, Local Tools, and Sharetribe as a general marketplace base | Building is a choice, not a necessity. Before any code, the decider should say why an existing tool is not enough — otherwise the project has no reason to exist | [myTurn](https://myturn.com/library-of-things/) · [Lend Engine](https://www.lend-engine.com/software-for-library-of-things) · [Local Tools](https://localtools.org/) · [Sharetribe](https://www.sharetribe.com/) |
| **Alternatives, counter-signal** — Streetbank (UK), free neighbour sharing, launched July 2010 and closed 1 March 2024: "our community stopped growing several years ago and doesn't justify continuing". NeighborGoods, SnapGoods and Ecomodo also closed **(excerpt for the last three)** | The failure mode of the free model is documented and repeated: it stalls below critical density rather than collapsing. Density in one neighbourhood — not total users — is the number to watch | [Wikipedia, Streetbank](https://en.wikipedia.org/wiki/Streetbank), citing the closure notice · [Fast Company, NeighborGoods](https://www.fastcompany.com/2682702/what-happens-now-that-sharing-economy-pioneer-neighborgoods-has-been-acquired) |
| **Business models** — The field's models, observed: paid membership for borrowers, free for lenders (Peerby, ~€19/yr); freemium subscription (AlloVoisins); commission on both sides (Fat Llama, about 15 % + 15 %, then 20 % + 10 % after being folded into Hygglo on 24 Nov 2025) **(excerpt)**; per-day rental plus municipal funding (Library of Things); cheap membership plus volunteers and grants (*outilthèques*); SaaS sold to the operator (myTurn, Lend Engine) | Every surviving model charges *someone*: the borrower, the lender, a council or the operator. A no-money product is viable only if it also costs almost nothing to run — that is a constraint on the build, not a detail | [Hygglo, Fat Llama is now Hygglo](https://hygglo.com/uk/fatllama) · sources above for the others |
| **Business models** — **Not found**: no sourced example of a money-free neighbour-to-neighbour lending platform that sustains itself without membership fees, commission or public funding | The absence is itself the finding. If the decider wants no money at all, the running cost has to be near zero and someone has to absorb it knowingly | — (searched; see *Assumptions*) |
| **Legal, FR** — Code de la consommation art. L111-7 defines an "opérateur de plateforme en ligne" as anyone offering "à titre professionnel, de manière rémunérée ou non" an online public communication service based on "la mise en relation de plusieurs parties en vue de […] l'échange ou le partage d'un contenu, d'un bien ou d'un service", with duties of loyal, clear and transparent information on terms, ranking, and the parties' civil and tax rights and obligations | Being free does not put the product outside French platform law — the text says "rémunérée ou non" and names sharing explicitly. The trigger is "à titre professionnel". A neighbourhood association running it may well be in scope | [Légifrance, art. L111-7 C. consommation](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033219601/2016-10-09) |
| **Legal, EU** — DSA (Reg. (EU) 2022/2065): art. 16 notice-and-action applies to *every* hosting provider whatever its size; art. 19 exempts micro and small enterprises from the online-platform obligations (complaint handling, out-of-court settlement, trusted flaggers, advertising and recommender transparency, trader traceability) | A small project still owes a usable way to report an illegal listing, with an answer. That is a small, concrete deliverable — not a reason to stop, but not free either | [EUR-Lex, Regulation (EU) 2022/2065](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065) |
| **Legal, EU** — GDPR art. 2(2)(c) exempts "processing of personal data by a natural person in the course of a purely personal or household activity", and recital 18 extends this to "social networking and online activity undertaken within the context of such activities" | Running the service for other people is not a household activity: names, a location precise enough to find a neighbour, and a loan history need a lawful basis, a retention limit and deletion — designed in, not added later | [EUR-Lex, Regulation (EU) 2016/679](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679) |
| **Legal, FR** — A loan with no money is a *prêt à usage* (commodat), Code civil arts. 1875–1891. Art. 1880 requires the borrower to look after and preserve the thing and to use it only as intended; misuse or keeping it too long makes the borrower liable for loss even by force majeure; and if the thing was **valued at the time of the loan**, the loss falls on the borrower unless agreed otherwise | Money-free is not liability-free, and one design choice decides who pays: if a listing records a value, the law shifts the loss onto the borrower. This belongs in the product's decisions, not in a footnote | [Légifrance, art. 1880 C. civ.](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006444712/2009-05-14) · [Légifrance, prêt à usage arts. 1875–1891](https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006070721/LEGISCTA000006136396/) |
| **Legal, FR** — Home-insurance civil liability covers damage the borrower causes to third parties, but damage to the *borrowed object itself* is generally not covered: the borrower pays, unless a specific guarantee or a waiver-of-recourse clause applies **(excerpt)** | The most common incident — a tool comes back broken — has no insurer behind it. The product will host disputes it cannot settle: either it says so plainly, or it declares it out of scope | [MAIF, location ou prêt de matériel entre particuliers](https://www.maif.fr/habitation/guide-assurance-habitation/location-materiel-particuliers) · [lesfurets, objets loués ou empruntés](https://www.lesfurets.com/assurance-habitation/guide/assurance-pour-objets-loues-ou-empruntes) |
| **Legal, EU/FR** — DAC7 platform reporting targets "relevant activities" carried out **for consideration** that the operator knows or can reasonably determine; rental of goods is in scope when paid. **Not found**: an official statement that gratuitous lending is excluded | If no money ever passes, tax reporting very probably does not apply — but the inference is mine. Keeping money out of the product also keeps this obligation away, which is an argument for the no-money rule | [European Commission, DAC7](https://taxation-customs.ec.europa.eu/taxation/tax-transparency-cooperation/administrative-co-operation-and-mutual-assistance/dac7_en) · [impots.gouv.fr, DPI-DAC7](https://www.impots.gouv.fr/transfert-dinformations-en-application-des-dispositifs-dpi-dac7-plateformes-deconomie-collaborative) |

**Assumptions** — what could not be sourced:

- **The country is France.** The idea file is a translation of a French original; nothing in
  the idea itself names a country. Every legal row above assumes France and the EU.
- **"Many tools sleep in garages."** The claim is plausible and is the idea's premise, but
  the figure usually quoted for it (a drill used a few minutes in its lifetime) has no
  primary source I could reach. Under-use of household tools is an assumption, not a fact.
- **Listing valuable tools with a location may create a burglary or targeting risk.**
  Searched; no source, no police advisory and no press case found either way. Recorded as an
  assumption because it would change the design if true.
- **Mutum** (French free object-lending platform, active around 2017) — its site did not
  resolve; whether it still exists is unknown. Its disappearance, if confirmed, would be a
  second French data point on the free model.
- **Pages that could not be read**, so their content is absent from the table: the ADEME page
  on lending between neighbours (HTTP 403), `myturn.com/pricing` (HTTP 404, so the cost of
  the SaaS alternative is unknown), the CREDOC report on second lives of objects (unreadable
  PDF), `mutum.com` (DNS failure).
- **No figure was found** for how many households in a French neighbourhood own a tool they
  would be willing to lend — the supply side of the idea is entirely unmeasured.

**Answered by the decider** — @napkinstack-admin, round 1:

5. *What does this do that Peerby and Bricolib do not?* — "It is free, with no financial
   intermediary: no payment, no commission, no membership; the service does not live off
   the exchange."
6. *Why build rather than adopt myTurn, Lend Engine or Sharetribe?* — "This is a validation
   project for the NapkinStack framework: the real goal is to put a full development cycle
   through it, not to beat those products." The decider states this plainly and accepts that
   it is a reason outside the product.
7. *A tool comes back broken and the two disagree?* — "The product records without
   arbitrating": state declared at the start and at the return, photographs, a timestamped
   history. The neighbours settle it between themselves.
8. *Should a listing carry the tool's value?* — Optional, the lender's choice; the product
   will have to explain what it implies.

**Open questions:** none remaining on the research itself. The answers change neither the
users nor the model, so stage 2 is not reopened — but three of them sit against the evidence
above, and that is recorded in section 3 under *Where the answers meet the evidence*.

## 3. Define

> Everything below comes from @napkinstack-admin, round 1. It is recorded as the decider's
> answer, not as an established fact.

**Users and their problem**

> **No user has been interviewed, and none will be before the first cycle.** Asked whether
> they had talked to a neighbour about this, the decider answered: "none. The problem is the
> decider's own reading, not a user's words." Asked whether they would interview three
> neighbours before the first cycle, the decider answered **no**: the problem stays an
> assumption, unconfirmed by any user, and the charter will carry it as one.
>
> The playbook is explicit — words reported by the decider alone are an assumption. So the
> problem statement below is an **assumption held knowingly**, not an oversight, and it is
> the single largest thing this document does not know.

- **Who** — people living in one neighbourhood in France, on two sides at once: the one who
  owns a tool and is willing to lend it, and the one who needs it for an afternoon. Nobody
  is only a borrower or only a lender by design.
- **How many** — unknown. No count exists for the first neighbourhood, and stage 2 found no
  figure for how many households own a tool they would lend. The supply side is unmeasured.
- **The problem, as the decider reads it** — the tool is often already a few doors away and
  unused, but nobody knows which garage it is in; asking around reaches only the neighbours
  one already talks to, so the neighbour buys or rents instead.
- **What the evidence says about that problem** — it does not confirm it, and it does not
  refute it. Willingness is high (YouGov: 53 % of US adults would be at least somewhat
  likely to ask a next-door neighbour to borrow a tool), but so is refusal (about 40 %
  would not ask at all), and nothing found measures the gap between *would ask a neighbour I
  know* and *would ask a stranger two streets away* — which is exactly the gap the product
  claims to close.

**Constraints**

| Constraint | What the decider said | What it implies |
|---|---|---|
| Who runs it | The decider, personally | One person, so no support rota and no out-of-hours answer. It also keeps the service below "à titre professionnel", which is the trigger of French art. L111-7 — but not below the DSA or the GDPR, which have no professional threshold |
| Budget | "Close to nothing" | Rules out paid hosting at scale, paid moderation and paid insurance. Stage 2 found no free model that sustains itself except by costing almost nothing to run, so this constraint and the no-money rule have to hold each other up |
| Time | "A few hours a week" | The first cycle has to be small enough to finish in that, including whatever answering a user takes |
| Platform | "It must work on a phone: the use happens in the garage or on the doorstep" | Phone-first, and the two moments that matter — declaring a tool's state at hand-over and at return — happen standing up, outdoors, possibly one-handed |
| Scope | France, any neighbourhood, anyone can open theirs, no invitation | Open registration: no gatekeeper, no vouching, and no guarantee that the people in a neighbourhood know one another. This is the point where the idea's "trust between neighbours who can already recognise each other" stops being automatic |
| Money | Free to start; a paid model stays possible later (membership, municipal support) | Nothing in the first cycle may assume a payment rail, but nothing should make one impossible either |
| Regulation | Not raised by the decider | France and the EU, from stage 2: DSA art. 16 (a usable way to report an illegal listing, whatever the size), GDPR (the decider is the controller: names, locations and loan history need a basis, a retention limit and deletion), *prêt à usage* C. civ. 1875–1891, and art. L111-7 if the service ever becomes professional |
| Purpose | "A validation project for the NapkinStack framework: the real goal is to put a full development cycle through it" | Stated by the decider, and outside the product. It is why the build-versus-adopt answer is not a reason to stop. It does **not** blur the product's own bar: the decider has separated the two criteria below, and a framework success with a missed product signal stops the product |

**Success signals** — the decider's. **There are two criteria, and they are separate.** Asked
what a missed product signal would mean once the framework cycle had run end to end, the
decider answered: "a success for the framework, a stop for the product."

| Criterion | What it measures | What it is | Who it judges |
|---|---|---|---|
| **A — the framework** | Did a full NapkinStack development cycle run properly, end to end: discovery, charter, cycle, deliverables, closure, fitness functions | The reason this project exists at all. It is met or missed on the *process*, whatever the product does | NapkinStack |
| **B — the product** | At three months, in one neighbourhood: **twenty loans made *and returned*** — not twenty listings — and **half of them second loans by a neighbour who came back**. The bad sign the decider named: listings with no loan at all | Whether the idea takes with real people | The product |

**The twenty loans measure B, and only B.** They say nothing about A, and A does not rescue
B. The decider's rule, in their words: if the cycle ran properly, the validation succeeded
even when the product does not take, and **the product is then stopped rather than dragged
along**.

The numbers in B are the decider's, kept as given. Two things they do not yet fix: which
neighbourhood is the first one, and how many tools must be listed before the count starts.
Both stay open below, on purpose.

**Where the answers meet the evidence** — three tensions, recorded, not resolved:

1. **Free is the differentiator, and free is what has repeatedly died.** The decider's answer
   to "what does this do that Peerby and Bricolib do not" is precisely the feature stage 2
   found no surviving example of: Streetbank, free, closed in 2024 on "our community stopped
   growing"; Peerby survived only by introducing paid membership in 2019. The decider's own
   constraints are the only thing that makes it survivable here — one person, near-zero cost,
   nothing to keep alive — and answer 7 keeps a paid model open for later. Worth naming, not
   a contradiction.
2. **Open to every neighbourhood, but measured in one.** Stage 2's failure mode is density
   inside a single neighbourhood, not total users. The scope answer spreads the product
   across France with no invitation; the success signal counts one neighbourhood. They can
   coexist, but only if the first cycle concentrates on one place — which is a proposed
   no-go in section 4.
3. **"Records without arbitrating" lands on a gap the law leaves open.** Stage 2 found that
   home-insurance civil liability generally does not cover damage to the borrowed object
   itself: the borrower pays out of pocket. "The neighbours settle it between themselves" is
   therefore accurate, and it means the product's history will be the only evidence in a
   dispute nobody insures. That raises the bar on the state-at-hand-over and
   state-at-return record, rather than lowering it.

**Answered by the decider** — round 1:

9. *Interview three neighbours before the first cycle?* — **No.** The problem stays an
   assumption, unconfirmed by any user; the charter will carry it as one.
13. *If the product signal is missed but the framework cycle ran end to end?* — "A success
    for the framework, a stop for the product." Two separate criteria, recorded above.

**Open questions** — left open on purpose by the decider, most decision-changing first:

10. Which neighbourhood is the first one, and how would you reach its households?
11. How many tools must be listed before the twenty-loan count starts?
12. As the controller under the GDPR you have to be reachable and to answer a deletion
    request. Are you willing to publish a contact and answer one?

## 4. Shape

**Value hypothesis**

> In a neighbourhood where tools are already listed, a neighbour who needs one for an
> afternoon will ask a household they do not know, two streets away, rather than buy the
> tool or rent it from a DIY store — because the tool is a hundred metres away and free to
> ask for, and because there is no payment, no commission and no membership to weigh up
> before asking.

The switch it claims is not from *nothing* to the product — stage 2 rules that out, since
asking a neighbour directly is what people already do. It is from **the neighbours you
already talk to** to **the neighbourhood you do not**, and the thing said to make that
possible is the absence of any money in the exchange.

**Proven wrong if**, three months after a first neighbourhood is live:

- fewer than **twenty loans have been made and returned** there (the decider's number); or
- fewer than **half of them are second loans by the same neighbour** (the decider's number);
  or
- the loans that do happen stay inside the circle of neighbours who already knew each other
  — the product would then be a convenience for existing relationships, not a way into new
  ones, and the hypothesis above would be false even while the counters looked healthy.
  *Proposed by the framer, **adopted by the decider** in round 1: it is now theirs.*

The decider also named the bad sign directly: **listings with no loan at all**.

This hypothesis is the object of **criterion B** in section 3 — the product. It has nothing
to say about **criterion A**, the framework cycle, and a refutation here stops the product
without touching the validation.

**Press release** — *imagined, for shaping only. No launch date is set;* `<launch day>` *is a
placeholder. Nothing below has happened.*

> **`<launch day>` — Tool Library opens in `<neighbourhood>`, France.**
>
> Somewhere on the street, a wallpaper stripper is needed for one afternoon. Three doors
> away, one has been sitting in a garage for years. Until today neither household knew about
> the other, so the first one bought a stripper, or drove to a rental counter, or put the job
> off.
>
> Tool Library is a free list of the tools a neighbourhood is willing to lend. A neighbour
> photographs a tool and says they are willing to lend it. Another sees what is available
> nearby, and the two agree between themselves on a day to hand it over and a day to give it
> back. The product records the state of the tool when it leaves and when it comes back, with
> photographs and a timestamped history, so that who holds what — and since when — is never
> in doubt.
>
> There is no payment, no commission, no membership, no delivery and no deposit. The product
> never stands between the two neighbours and never takes anything from what passes between
> them. It does not insure the tool and it does not settle disagreements: it records, and the
> neighbours settle it themselves.
>
> *"I wasn't going to buy a stripper for one afternoon, and I wasn't going to drive across
> town to rent one either. I knocked on a door I'd never knocked on. We agreed on Saturday,
> and I brought it back on Sunday."* — **imagined quote, from an imagined neighbour. No such
> person has been interviewed.**

**Convinces the decider?** **Yes**, as written — @napkinstack-admin, round 1.

**No-gos**

All ten are **the decider's**. The first four came from their answers; the last six were
proposed by the framer and **all six were kept** in round 1, so they carry the same weight.

*Given by the decider:*

- **No payment, no commission, no membership** at launch. The service does not live off the
  exchange. (Not permanent: the decider keeps a paid model open for later — membership or a
  municipality's support.)
- **No arbitration.** The product records — state at hand-over, state at return,
  photographs, timestamps — and never judges who is right.
- **No delivery and no logistics.** The two neighbours hand the tool over themselves.
- **No gatekeeping of who may open a neighbourhood.** No invitation, no vouching.

*Proposed by the framer, **kept by the decider** in round 1 — all six, unchanged:*

- **No insurance, no guarantee and no deposit handled by the product** — and this
  said in plain words at the moment of the loan, not buried in terms. Stage 2 found that
  home-insurance civil liability generally does not cover damage to the borrowed object
  itself; the borrower pays. Neighbours should learn that before the tool leaves, not after
  it breaks.
- **No exact address in public.** An approximate location until both neighbours
  have agreed on the loan. GDPR data minimisation asks for it, and the targeting risk of a
  public list of valuable tools with addresses is an assumption serious enough not to test
  in production.
- **No value shown without its consequence shown.** The decider made the value
  optional and the lender's choice, and asked that the product explain what it implies. The
  no-go is narrower: the field must not exist without the explanation next to it. Under
  C. civ. art. 1880, a thing valued at the time of the loan puts the loss on the borrower
  even by force majeure, unless otherwise agreed — a lender should not flip that switch
  without knowing.
- **No reputation score on a person.** A record of loans, yes; a public rating
  attached to a named neighbour, no. It turns a neighbour into a rated stranger, and it
  makes a one-person service the holder of a published judgement about an identified
  individual.
- **No second neighbourhood counted as success before the first reaches twenty
  returned loans.** Stage 2's failure mode is density inside one neighbourhood, not total
  users; Streetbank died of a community that stopped growing, not of a lack of countries.
- **No native mobile application in the first cycle.** One phone-first web page.
  A few hours a week and a near-zero budget do not carry two app stores.

**Answered by the decider** — round 1:

14. *Does the press release convince you?* — **Yes, as written.** Recorded above.
15. *Keep the six proposed no-gos?* — **All six kept**, including "no second neighbourhood
    before the first reaches twenty returned loans". They are the decider's now.
16. *Adopt the third refutation condition?* — **Adopted.** The *proposed* mark is dropped.

**Open questions:** none remaining in this section.

## 5. Challenge

**Challenger:** agent session — Claude Opus 5, challenger posture (`playbooks/discovery.md`
§5); did not write stages 1 to 4 and did not speak to the decider · 2026-09-17

> Section 1 is confirmed, so this challenges the document as written. Every question I would
> have put to the decider is below as an objection, not as a question. Research: the same
> tools as stage 2 — Claude Code's **WebSearch** and **WebFetch** — the same marking,
> **(self-reported)** and **(excerpt)**, an unsourced claim marked *assumption*, and one
> addition: **(fetched)** marks a page I retrieved myself on 2026-09-17. Same stopping rule:
> stop when what contradicts the value hypothesis and what contradicts the riskiest
> assumptions each have at least one sourced finding, or an explicit "not found".

**Pre-mortem** — it is 17 September 2027. One neighbourhood went live, the cycle closed, the
product is dead. The plausible reasons, most likely first, each tagged with its risk:

1. **The neighbourhood never filled.** Fourteen households joined, thirty tools were listed,
   four loans happened, three of them between people who already spoke to each other. Nothing
   broke: it stayed below the density at which a stranger's drill is worth a message.
   *Value.* This is Streetbank's recorded ending in §2 — "our community stopped growing" —
   and the success signal is built to catch it three months after it has already happened.
2. **The listings were there and nobody asked.** The decider's own bad sign. The product
   solved discovery, which was never the hard part: what stops a person is knocking on the
   door, not knowing which door. *Value.*
3. **The street's WhatsApp group answered first.** "Anyone got a wallpaper stripper?" got a
   reply in four minutes, from a group everyone was already in, with no account, no listing
   and no return date. The product was a second place to look. *Value.*
4. **Nobody performed the ritual.** Two photographs and a declared state at hand-over, two
   more at return — the thing that makes this a lending product rather than a list — had to
   happen on a doorstep, outdoors, with a drill in one hand. After three loans the history
   was partial, so "who has what" went back to memory and the product lost its reason to
   exist. *Usability.*
5. **The first broken tool ended the street's appetite.** A grinder came back with a cracked
   guard. The product recorded and did not arbitrate, exactly as designed; the two neighbours
   settled nothing; everyone else read the episode as the price of lending and quietly
   deleted their listings. *Viability.* At this size, one incident per neighbourhood is
   enough.
6. **Someone was hurt, and the record pointed at the lender.** C. civ. art. 1891 makes the
   lender liable for a defect they knew of and did not disclose. The product's signature
   feature is a timestamped, photographed declaration of the tool's state by its owner — that
   is written evidence of what the lender knew. The first injury turned the product's record
   against the person who made it. *Viability.*
7. **The operator ran out of Saturdays.** A deletion request, a reported listing, two people
   who could not log in, one "he still has my ladder". "A few hours a week" was the build
   budget; nobody costed the answering. *Feasibility.*
8. **"Free" was never the differentiator.** In France the free slot was already taken — by an
   associative clone of this exact product, by Geev for giving, by Facebook and WhatsApp
   groups for everything else. No neighbour ever compared the product with Bricolib's
   commission, because no neighbour was ever going to pay another neighbour. *Value.*
9. **Criterion B was never measured.** The first neighbourhood was never chosen (open
   question 10), the cycle closed on time, the framework was validated, and the product was
   neither proved nor stopped — it was left running with four loans in it. *Viability.* On
   the evidence of this document this is the likeliest ending of all: it is the only one that
   requires nothing to go wrong.
10. **A deletion request broke the history.** One neighbour asked to be erased; their name
    sat inside the only record of a loan the other neighbour was still waiting to get back.
    The product could obey the law or keep the evidence, not both. *Feasibility.*

**The four risks**

Every threshold below is **proposed, for the decider to set**. All four tests run before any
code and none of them needs the product to exist.

| Risk | Riskiest assumption | Cheapest test — and the result that refutes it |
|---|---|---|
| Value | That the missing thing is *knowing which garage*. The hypothesis needs a neighbour to ask a household they have never spoken to; §3 admits nothing found measures that gap, and it is the whole switch being claimed | **A paper list, no product.** Knock on ~30 doors of one street, list the tools of whoever agrees, print one sheet with one phone number, drop it in every letterbox (~100). Two evenings of work, then count for **4 weeks**. **Refuted if** fewer than **5 requests** arrive in 4 weeks, or fewer than **3** of them go to a household the asker says they had never spoken to. A zero-friction free list that produces no request across the stranger gap will not produce one behind a login |
| Usability | That both neighbours will record a state — photographs and a line — at hand-over *and* at return, standing outdoors, with nothing but the product asking them to | **Wizard of Oz on ten real loans.** No software: a human asks both parties by SMS for two photographs and one sentence at hand-over, and again at return. **3 weeks.** **Refuted if** fewer than **7 of 10** loans come back with a complete record at *both* ends, or the median delay between a return and its record exceeds **24 hours**. A record people will not produce for a person asking by SMS is not one a screen will extract |
| Feasibility | That one person, at "a few hours a week" and "close to nothing", can build *and then run* a service carrying photographs, a controller's duties, a reporting route and disputes — and that building it beats adopting one of the products §2 already found | **Run a neighbourhood on someone else's software for three weeks, with a timesheet.** Open one neighbourhood on `entrevoisins.eu`, or a free myTurn / Lend Engine trial; log every minute of operations; have a friend send one deletion request and one abuse report, and answer both for real. **3 weeks.** **Refuted if** operations alone exceed **2 hours a week**, or any of the three duties — deletion, report, a published contact — cannot be answered within **72 hours**. The same three weeks answer question 6 with evidence rather than with a framework reason |
| Viability | That the product can be honest about liability and still have supply, and that "no money" survives the running bill | **The disclosure doorstep, plus a priced bill.** (a) Read the no-gos' own words to 5 households owning a tool worth more than €150 — no insurance, no deposit, no arbitration, the borrower pays out of pocket, and a declared value shifts the loss onto them under art. 1880 — then ask them to list it. One afternoon. (b) Price 12 months of one neighbourhood — 50 users, 500 photographs, backups, domain, mailbox — from the actual providers, in writing. Two hours. **Refuted if** fewer than **3 of 5** still list after hearing it, which leaves supply only in the €4–10/day band where Leroy Merlin and Kiloutou already rent *with* insurance; or if (b) exceeds **€50 a year**, where "close to nothing" stops being true |

**Counter-evidence**

| What was found | What it contradicts | Source |
|---|---|---|
| **Smiile is gone.** `smiile.com` today serves a domain-sale page: "smiile.com for sale", "Buy now $19,999", listed with spaceship.com **(fetched, 2026-09-17)**. Smiile was created in 2014 in Saint-Malo and described as the French reference for mutual aid between neighbours, 100 % free for residents, gathering "more than 500,000 neighbours", with object lending among its features **(excerpt)** | Stage 2 does not mention Smiile at all. The largest French free neighbourhood network — with B2B revenue from social landlords and municipalities that the decider will not have — has disappeared. "Free + neighbourhood + objects" did not just fail abroad and long ago; it failed in France, recently, at 500,000 members | [smiile.com](https://www.smiile.com/) · excerpt: [startup-story.fr](https://www.startup-story.fr/entrepreneurs/ecocollab-smiile-reseau-dentraide-entre-voisins.html) |
| **The exact product already exists in France, free.** `entrevoisins.eu`, live **(fetched, 2026-09-17)**: "Prêt d'objets entre voisins — Gratuit, local, sans pub", "un projet associatif de prêt d'objets entre voisins d'un même quartier", invitation by SMS or e-mail with no password, objects "triés par proximité", a request with "un message pré-rempli et un créneau", "Pas de note, pas de score", "Pas de location, pas de commission, pas d'abonnement", "Créer mon quartier", and a first category reading perceuse, ponceuse, scie sauteuse, échelle, nettoyeur haute pression. **Not found**: any usage figure, any named operator, any legal notice — `/mentions-legales`, `/cgu`, `/a-propos` all return the same page | The decider's answer 5 — "It is free, with no financial intermediary" — is not a differentiator against this. The product, the scope (anyone opens their neighbourhood), and four of the ten no-gos (no money, no score, no delivery, no gatekeeping) are already shipped by someone else, for nothing, in French. That a free associative clone can exist with no visible operations and no legal notice is also a warning about what this project becomes by default | [entrevoisins.eu](https://entrevoisins.eu/) |
| **Mutum, the French free lending platform, was liquidated.** Liquidation at the end of 2017 despite 68,800 "voisins engagés" and 113,000 objects in September 2017, and 81,658 / 153,682 in April 2019 after the founders left; the co-founder's stated subject was "les difficultés, pour un entrepreneur social, de concilier solidarité, écologie et activité économique". A later count of "environ 1 000 membres" appears in a secondary blog **(excerpt)**. `mutum.com` does not resolve **(fetched, 2026-09-17)** | Stage 2 left Mutum open as an assumption ("whether it still exists is unknown"). It resolves against the idea, and worse than a closure: 113,000 objects listed alongside a collapsing membership is the decider's own bad sign — "listings with no loan at all" — observed at scale, in France, on the money-free model | [Solidarum](https://www.solidarum.org/vivre-ensemble/entreprise-ou-solidarite-mutum-lecons-d-echec) · excerpt: [duclair-environnement.org](https://www.duclair-environnement.org/pretoo-site-pret-gratuit-existe-plus/) |
| **Pretoo**, a French free object-lending site, "malheureusement fermé ses portes quelques années après sa création"; no date and no figures given **(excerpt)** | A third French death on the free model, after Mutum and Smiile. Weak as a source, but it points the same way as every other French data point found | [duclair-environnement.org](https://www.duclair-environnement.org/pretoo-site-pret-gratuit-existe-plus/) |
| **Peerby now sells renting.** Its landing page leads with "rent goods from neighbors — Borrow tools, party gear, electronics, bikes and lots more" **(fetched, 2026-09-17)** | §2 reads Peerby as "the idea has been built and it works", on a 2022 self-reported source. The version that survived a 2017 near-failure, a 2019 paid membership and four more years leads with money in the exchange. The surviving Peerby is not the one the decider is describing | [peerby.com](https://www.peerby.com/en-us) |
| **In France the free peer product that scales is giving, not lending.** Geev: more than 6 million registered users in 2025, about 2 million active, 55 million objects posted; model = advertising in the free version plus a €25/year subscription **(excerpt)** | Giving has no return, no date, no state at hand-over and no liability. The one French free-exchange success removes every mechanic the value hypothesis depends on — and still needs ads and a subscription to exist. It is evidence that what French neighbours will do at scale for free is *give away*, not *lend and get back* | [echos-judiciaires.com](https://www.echos-judiciaires.com/actualites/geev-leconomie-du-don/) · [geev.com](https://www.geev.com/fr) |
| **The incumbent is the neighbourhood WhatsApp group, and it already lends.** France Info, 27 March 2026: neighbour WhatsApp groups born under Covid have persisted; "Les Hyper Voisins" in the 14th arrondissement of Paris counts nearly 2,000 members; a participant describes "trocs party, where we give things to each other, we lend things" **(fetched, 2026-09-17)** | §4's switch is "from the neighbours you already talk to, to the neighbourhood you do not". The free, zero-install, already-open competitor for that switch is the street group — which also crosses the stranger gap, at 2,000 members, without a product. §2 never looked at it | [franceinfo, 27 Mar 2026](https://www.franceinfo.fr/societe/j-ai-multiplie-par-dix-mes-amis-en-l-espace-d-une-annee-les-groupes-whatsapp-une-maniere-de-faire-tomber-les-murs-pour-de-nombreux-voisins_7898915.html) |
| **The market leader sets the minimum neighbourhood at 10 verified households.** Nextdoor keeps a new neighbourhood in "pilot" until 10 members have joined and confirmed their address, inside a 21-day pilot period, after which an unlaunched neighbourhood expires **(excerpt — help.nextdoor.com could not be fetched, certificate error; wording from a search result)** | A company with paid growth treats 10 verified households in 21 days as the floor below which a neighbourhood is not viable. The document has no recruitment plan, and which neighbourhood comes first is open question 10 | [help.nextdoor.com](https://help.nextdoor.com/s/article/Create-a-new-neighborhood-on-Nextdoor) |
| **Loans per member are low even where the tools are pooled and staffed.** North Portland Tool Library, about 5,000 members and 7,364 tool loans in 2013; West Seattle, about 700 members and over 1,000 tools **(excerpt, primary not reached)** | Roughly 1.5 loans per member-year with a central stock, opening hours and staff. Twenty returned loans in three months, in one neighbourhood, with none of those advantages, implies on the order of fifty active households — five times Nextdoor's launch floor. The arithmetic is mine, *assumption* | search excerpt; collected at [USDN, Tool Lending Libraries](https://sustainableconsumption.usdn.org/initiatives-list/tool-lending-libraries) |
| **The DSA may not apply at all, and size is not the reason.** DSA art. 3(a) defines "information society service" by reference to Directive (EU) 2015/1535 art. 1(1)(b): "any service **normally provided for remuneration**, at a distance, by electronic means and at the individual request of a recipient of services" **(fetched, primary)**. **Not found**: Commission guidance or case law applying the DSA to a free, non-commercial service run by a natural person | §2 states art. 16 "applies to *every* hosting provider whatever its size". The threshold question is remuneration, not size, and a strictly money-free service run by one individual sits on the wrong side of an untested line. This does not license skipping a reporting route — build it anyway — but the document records as settled a question that is open, and it is the same "no money" that DAC7 was said to keep away | [EUR-Lex, Directive (EU) 2015/1535](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32015L1535) |
| **The lender's liability is missing from the document.** C. civ. art. 1891: "Lorsque la chose prêtée a des défauts tels qu'elle puisse causer du préjudice à celui qui s'en sert, le prêteur est responsable, s'il connaissait les défauts et n'en a pas averti l'emprunteur." Art. 1888: the lender cannot take the thing back before the agreed term, or before it has served its purpose **(fetched, primary)** | Stages 2 to 4 carry only the borrower's side — art. 1880, breakage, who pays. The incident that kills a neighbourhood tool project is an injury, and the law puts that on a lender who knew of the defect. The product's central artefact, a declared and photographed state at hand-over, is exactly the proof of what the lender knew: the signature feature increases the exposure of the people it is asking to supply the tools. Art. 1888 also means the two recorded dates are a term the lender cannot unilaterally shorten — not a convenience | [Légifrance, prêt à usage arts. 1875–1891](https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006070721/LEGISCTA000006136396/) |

**Assumptions — mine, unsourced, marked as such:**

- **Fifty active households for twenty loans.** My arithmetic from tool-library loan rates,
  applied to a setting with no central stock. *Assumption.*
- **A search excerpt attributed "57 % of French people use digital tools to talk to their
  neighbours" to the Ined.** The article I fetched carries no such figure and cites no
  institute. Dropped: *assumption*, not evidence.
- **The age and activity of `entrevoisins.eu` are unknown.** Domain lookups failed in this
  environment (no WHOIS resolution, RDAP 404). It is live and it is the same product; whether
  anybody uses it, I could not establish — which is itself the point about free clones.
- **Burglary or targeting risk** from a public list of valuable tools: searched again, still
  no source either way. Stage 2's assumption stands unresolved, and the no-go that answers it
  is the right call anyway.

**Flaws in stages 1 to 4**

1. **§2 searched the world and missed France.** Objection to the row *"**Alternatives** —
   Software to run exactly this already exists: myTurn … Lend Engine, Local Tools, and
   Sharetribe"* and to the alternatives rows around it. The two findings that decide this
   project were not found: a live French associative product that already is the idea, free
   and ad-free (`entrevoisins.eu`), and the collapse of the French leader of free
   neighbourhood mutual aid (Smiile, domain now for sale). Stage 2 met its stopping rule —
   one sourced finding per point — with an Anglo-Dutch sample plus two French *paid*
   products. The rule was satisfied and the question was not answered.
2. **The one constraint the document says must hold is never priced.** Objection to *"**Not
   found**: no sourced example of a money-free neighbour-to-neighbour lending platform that
   sustains itself … the running cost has to be near zero and someone has to absorb it
   knowingly"* (§2) and to *"Budget | 'Close to nothing'"* (§3). No figure appears anywhere
   for what one neighbourhood costs for a year, with photographs and backups. A product whose
   viability is stated to depend on near-zero cost contains no cost.
3. **Criterion B cannot be passed or failed as written.** Objection to *"At three months, in
   one neighbourhood: **twenty loans made and returned**"* (§3) read against *"**How many**
   — unknown. No count exists for the first neighbourhood"* (§3) and open questions 10 and
   11. There is no neighbourhood, no population, no start date and no listing prerequisite. A
   threshold with no denominator and no clock is not a success signal; it is a number.
4. **B has no owner, so it will not be measured.** Objection to *"a success for the
   framework, a stop for the product"* (§3). The separation is honest and it is also the
   failure mode: the framework cycle has a plan, deliverables, fitness functions and a
   closure; B has none of these. Nothing in the document schedules recruiting households, and
   the cycle will close before three months of loans could exist. The likeliest outcome is
   that A is declared and B is never run — which the document explicitly forbids as an
   outcome, and implicitly arranges.
5. **Tension 2 is recorded as resolved, and is not.** Objection to *"They can coexist, but
   only if the first cycle concentrates on one place — which is a proposed no-go in section
   4"* (§3). The no-go it points to is *"No second neighbourhood **counted as success**
   before the first reaches twenty returned loans"* (§4). That constrains the counting, not
   the opening. *"anyone can open theirs, no invitation"* (§1, answer 2) stays in force, and
   thin membership spread over many neighbourhoods is precisely the failure mode §2
   documented. Either the first cycle opens one neighbourhood and no other, or the tension is
   live.
6. **The value hypothesis bundles two causes and cannot tell them apart.** Objection to
   *"because the tool is a hundred metres away and free to ask for, and because there is no
   payment, no commission and no membership to weigh up before asking"* (§4). The second
   clause is almost certainly false as a cause: nobody weighs a payment before asking a
   neighbour, because asking a neighbour has never had a price. The absence of money
   separates the product from Bricolib, not from what a neighbour does today. All three
   refutation conditions count loans, so a refutation would not tell the decider which clause
   failed — and the surviving clause, proximity, is not something this product supplies.
7. **Three doorstep conversations were refused against a three-month bet.** Objection to
   *"**No user has been interviewed, and none will be before the first cycle**"* (§3) and
   answer 9. Holding an assumption knowingly does not make it cheap. The problem statement,
   criterion B, the value hypothesis and the press-release quote all rest on one person's
   reading of their own street; the document says so and proceeds. The stated alternative is
   to learn the same thing in three months, after a build. That is not a trade-off between
   speed and rigour — the interview is faster than the cycle.
8. **The DSA row overstates a point that is open.** Objection to *"art. 16 notice-and-action
   applies to **every** hosting provider whatever its size"* (§2) and its echo in the
   Regulation row of §3. The gate is "normally provided for remuneration" (Directive
   2015/1535 art. 1(1)(b)), not size. Build the reporting route regardless — but a document
   that marks its uncertainties this carefully elsewhere should not settle this one in
   passing.
9. **Only half of the legal truth reaches the user.** Objection to the no-go *"No insurance,
   no guarantee and no deposit handled by the product — and this said in plain words at the
   moment of the loan … Neighbours should learn that before the tool leaves"* (§4). What the
   lender is told is that the borrower pays. What the lender is not told is art. 1891 — that
   a defect they knew of and did not disclose puts the injury on them — while the product is
   simultaneously asking them to photograph and declare the tool's state. A no-go built on
   candour that omits the half affecting the person supplying the tool is not candid.
10. **"Below 'à titre professionnel'" is an unsourced inference, and it rests on something
    the decider has already said may change.** Objection to *"It also keeps the service below
    'à titre professionnel', which is the trigger of French art. L111-7"* (§3). Nothing
    sourced supports that reading, and §2's own row says "A neighbourhood association running
    it may well be in scope". Worse, §1 answer 4 keeps membership fees and municipal support
    open: the day money arrives, the trigger question reopens on a service run under a
    private individual's name — with open question 12 still asking whether that individual
    will publish a contact at all.
11. **The only behavioural number in the document is from the wrong country.** Objection to
    *"Willingness is high (YouGov: 53 % of US adults would be at least somewhat likely to ask
    a next-door neighbour to borrow a tool)"* (§3), drawn from a survey of 35,878 **US**
    adults (§2). The French rows measure goodwill (BVA) and prices (Leroy Merlin, Kiloutou),
    not borrowing behaviour. The document flags "The country is France" as an assumption in
    §2 and then reasons about French users from American data in §3.
12. **The press release is validated by the two people who cannot judge it.** Objection to
    *"**Convinces the decider?** **Yes**, as written"* (§4). It was written by the framer and
    approved by the decider, both of whom already believe the idea; no neighbour has read it.
    It also describes the heaviest part of the product — *"records the state of the tool when
    it leaves and when it comes back, with photographs"* — as though it were weightless,
    which is the usability risk stated as a benefit.
13. **"A clear history" and the right to erasure are in direct conflict, and the conflict is
    not named.** Objection to §1's *"a history that makes an unreturned tool visible"* read
    against §3's *"names, locations and loan history need a basis, a retention limit and
    deletion"*. A deletion request from one party lands inside the record the other party
    depends on — most acutely when the tool has not come back. The document treats deletion
    as a duty to implement; it is also a design decision about what the history is for.

## 6. Decision

**go** — @napkinstack-admin, 2026-09-18, end of round 1. In the decider's words:
**"go — an acknowledged rehearsal, criterion A only."**

This go authorises the charter and one bounded cycle. It does **not** authorise a
deployment. The software is built for real, under the framework's own rules; the market is
not entered. No neighbourhood will be opened, no household approached, nothing shipped to a
real user.

### The reasons, as the decider gives them

**1. The product objections are held to be right, and they do not block, because the product
will not be deployed.** The pre-mortem endings and the eleven counter-evidence rows —
`entrevoisins.eu` shipping the same product free in French, Smiile's domain for sale after
500,000 neighbours, Mutum liquidated with 113,000 objects listed, Pretoo closed, Geev
scaling on giving, Peerby leading with renting, the street's WhatsApp group — are accepted
as accurate. They would block a product that sought users. This one will not seek any.

**2. Criterion B is dropped, not deferred.** The decider's own rule said a missed B stops the
product rather than dragging it along; the challenger's likeliest ending was "A declared, B
never measured". Rather than arrange that ending, the decider removes B: **the twenty loans,
the second-loan share and the third refutation condition are withdrawn as a success
criterion of this project.** The value hypothesis stays in section 4 as what was believed and
what the evidence says of it — it is not being tested here. Open questions 10 and 11 fall
with B; 12 stays, since it is about the operator, not the market.

**3. The method flaws are accepted.** Flaws 1 to 13 stand as written. The factual corrections
— the DSA's threshold being remuneration rather than size, Mutum resolved against the idea,
the YouGov figure being American — carry into the charter's constraints rather than being
argued with. The framer's stage 2 missing France is recorded as the finding it is.

**4. No test is kept as a spike.** All four need real neighbours or a real deployment;
keeping them would create deliverables this project could never close honestly. The decider
keeps none — including the pricing exercise.

**5. What remains, and why the go is worth anything.** The software is built for real, under
the framework's own rules: a charter, one bounded cycle, modules with owners, a contract
between two teams, test sheets run by a verifier with evidence, and a closure on the cycle's
end date. **Criterion A is what this project measures: that a full NapkinStack cycle runs end
to end, and that its barriers hold.** The product is the material, not the goal.

### Why each objection does not block the go

The answer is structural and it is the same for every product objection: **accepted as true,
and not blocking because the product is not being deployed.** Recorded group by group, so
that a reader can check that nothing in section 5 is left out.

| Objections in section 5 | How many | Why they do not block |
|---|---|---|
| **Pre-mortem**, endings 1 to 10 | 10 | Every one of them is an ending of a *deployed* product with users — a neighbourhood that never filled, listings nobody asked for, the WhatsApp group answering first, the ritual not performed, a broken grinder, an injury, the operator's Saturdays, "free" not being a differentiator, a deletion request breaking the history. Accepted as accurate; none can occur, because no neighbourhood is opened. Ending 9 is of another kind and is answered individually below |
| **The four risks** and their tests | 4 | All four tests need real neighbours or a real deployment, so none is kept (reason 4). Their assumptions are not being tested — and therefore not relied on: nothing in this project's claim rests on them. One half of one survives: the *feasibility* assumption splits, the "can one person **run** it" half falling away with the deployment, and the "can one person **build** it under the framework" half remaining — which is exactly what criterion A measures |
| **Counter-evidence**, rows 1 to 9 | 9 | The market and the model: Smiile, `entrevoisins.eu`, Mutum, Pretoo, Peerby, Geev, the WhatsApp group, Nextdoor's ten-household floor, tool-library loan rates. Accepted as accurate. They bear on whether the product should be deployed, and that question is now answered: it will not be |
| **Counter-evidence**, rows 10 and 11 | 2 | Legal corrections, not market objections: the DSA's gate is remuneration and not size, and C. civ. art. 1891 puts an injury from a known undisclosed defect on the lender while art. 1888 makes the agreed term binding on them. Not disputed — carried into the charter's constraints (reason 3) |
| **The challenger's own assumptions** | 4 | Marked unsourced by the challenger itself. Nothing in this decision relies on any of them being true or false; the burglary-risk one already has a no-go answering it whichever way it falls |
| **Flaws in stages 1 to 4**, 1 to 13 | 13 | Accepted as written, all thirteen (reason 3). Three are answered individually below; the factual corrections inside flaws 8, 10 and 11 carry into the charter; flaws 1, 2, 5, 7, 9, 12 and 13 are recorded as defects of this document that the framing inherits rather than arguments to rebut |

The six the decision turns on, individually:

- **Pre-mortem 9 — "criterion B was never measured."** The challenger called it "the likeliest
  ending of all: the only one that requires nothing to go wrong." Not disputed, and not
  arranged: rather than declare A and quietly never run B, **B is withdrawn**. The predicted
  ending is removed by removing the criterion it predicted would go unmeasured — not by a
  promise to measure it.
- **Counter-evidence 2 — `entrevoisins.eu`.** The same product, free, ad-free, in French,
  already shipped, with four of the ten no-gos already in it. Accepted. It removes the reason
  to *deploy*. It does not remove the reason to *build*, because what is being validated is
  the framework's cycle, not the product's originality.
- **Counter-evidence 1 — Smiile.** 500,000 neighbours, domain now for sale; with Mutum and
  Pretoo, the French base rate for the money-free model. Accepted. It would block a product
  seeking users. It does not block a rehearsal.
- **Flaw 3 — "criterion B cannot be passed or failed as written."** Accepted: no
  denominator, no clock, no listing prerequisite. The response is not to supply them but to
  drop B. Open questions 10 and 11 fall with it.
- **Flaw 4 — "B has no owner, so it will not be measured."** Accepted, and it is the flaw
  that produced this decision. The separation of A and B was honest, and the document
  arranged B's neglect. Removing B removes the arrangement.
- **Flaw 6 — "the value hypothesis bundles two causes and cannot tell them apart."**
  Accepted. The hypothesis stays in section 4 as what was believed at round 1 and what the
  evidence says of it. It is not being tested here, so the bundling is recorded as a defect
  of the reading, not carried forward as a measurement.

### What the first cycle carries

**Spikes: none.** All four of the challenger's tests need real neighbours or a real
deployment. Keeping any would create a deliverable this project could not close honestly —
the pricing exercise included.

**No-gos.** The ten of section 4 stand, and the decision adds one that overrides them where
they overlap:

- **No deployment to a real user** — no neighbourhood opened, no household approached,
  nothing shipped. From the decision itself, and the reason every product objection is
  accepted without blocking.
- The sixth framer no-go, *"no second neighbourhood counted as success before the first
  reaches twenty returned loans"*, loses its measure when B is withdrawn. It is subsumed by
  the no-go above — no neighbourhood is opened at all. **The framing settles the wording.**

**Criterion A is the only criterion**, and it is what the cycle must show: a charter; one
bounded cycle with an appetite and an end date; modules with owners; a contract between two
teams; test sheets run by a verifier with evidence; a closure on the end date; the fitness
functions green. A is missed if the cycle runs past its end date with no recorded decision,
if a barrier is bypassed, or if a deliverable is closed without its evidence.

**Carried into the charter as constraints, not as arguments** (reason 3): the DSA's gate is
remuneration, not size (counter-evidence 10, flaw 8); the lender's liability under C. civ.
art. 1891 and the binding term under art. 1888 (counter-evidence 11, flaw 9); the only
behavioural figure in this document is American (flaw 11); *"below à titre professionnel"*
is an unsourced inference (flaw 10); stage 2's research missed France (flaw 1); no cost
figure appears anywhere (flaw 2); the problem itself is an assumption no user has confirmed
(§3), and it stays one.

**Open questions.** 10 and 11 fall with criterion B. **12 stays** — whether the operator
publishes a contact and answers a deletion request — because it is about the operator, not
the market, and software that is built still processes whatever data its own testing puts
into it.
