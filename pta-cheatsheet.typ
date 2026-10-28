// PTA 3.1 form and substance cheat sheet (Wagemans, ATIP v6, 2026).
#import "@preview/merman:0.3.0": show-mermaid-blocks
#set page("us-letter")

#set text(size: 12pt, font: "Libertinus Serif")
#show raw.where(lang: "mermaid"): show-mermaid-blocks(
  typography: (font: ("Libertinus Serif",), size: "13px"),
  width: 100%,
)

#let fill = (
  alpha: rgb("#dbeafe"),
  beta: rgb("#dcfce7"),
  gamma: rgb("#f3e8ff"),
  delta: rgb("#ffedd5"),
)

= PTA: form and substance

#table(
  columns: (auto, auto, auto, 1fr),
  inset: 8pt,
  stroke: 0.5pt + luma(170),
  align: (center + horizon, left + horizon, left + horizon, left + horizon),
  table.header([*form*], [*schema*], [*shared*], [*substance*]),
  table.cell(fill: fill.alpha)[*α*], [a is X because a is Y], [p1.subj = p2.subj],
  [_subjects are..._ #linebreak()  #strong[F]act  #linebreak() #strong[V]alue  #linebreak() #strong[P]olicy ],
  table.cell(fill: fill.beta)[*β*], [a is X because b is X], [p1.subj != p2.subj #linebreak() p1.pred == p2.pred],
  [_subjects are ..._ #linebreak() #strong[s]ingular #linebreak() #strong[p]articular #linebreak() #strong[u]niversal],
  table.cell(fill: fill.gamma)[*γ*], [a is X because b is Y], [p1.subj != p2.subj #linebreak() p1.pred != p2.pred],
  [_in $s R p$, $R_1$ and $R_2$ are..._#linebreak() #strong[i]dentical #linebreak() #strong[d]ifferent -- try a middle step "a is Y"],
  table.cell(fill: fill.delta)[*δ*], [q is \<A or U> because q is Z], [subj = q #linebreak() pred = A or U],
  [ _Z is reported by..._ #linebreak() *I* - the speaker #linebreak() *II* - the hearer #linebreak() *III* - a third party ],
)

#pagebreak()

= Flow chart

```mermaid
flowchart TB
  c(["rewrite: conclusion because premise"]) --> d{"premise about the<br/>whole conclusion q?"}
  d -- yes --> D["δ · person of Z:<br/>I · II · III"]
  d -- no --> s{"same subject?"}
  s -- yes --> p1{"same predicate?"}
  s -- no --> p2{"same predicate?"}
  p1 -- no --> A["α · predicate types:<br/>F · V · P"]
  p1 -- yes --> X["rephrase / begs<br/>the question"]
  p2 -- yes --> B["β · subject quantities:<br/>s · p · u"]
  p2 -- no --> G{"γ · a→b same<br/>relation as X→Y?"}
  G -- yes --> Gi["γ i"]
  G -- no --> m{"middle step<br/>a is Y works?"}
  m -- yes --> Gm["split: α + β"]
  m -- no --> Gd["γ d · Non"]
  classDef alpha fill:#dbeafe,stroke:#1d4ed8
  classDef beta fill:#dcfce7,stroke:#15803d
  classDef gamma fill:#f3e8ff,stroke:#7e22ce
  classDef delta fill:#ffedd5,stroke:#c2410c
  classDef bot fill:#e5e7eb,stroke:#4b5563
  class A alpha
  class B beta
  class G,Gi,Gm,Gd gamma
  class D delta
  class X bot
```

#pagebreak()

= Labels
#table(
  columns: (auto, auto, auto, auto, auto),
  table.header([form], [substance], [lever], [name], [symbol]),
  [α], [FF], [Y is a SIGN of X], [argument from sign], [Sig],
  [α], [FF], [Y is a CAUSE of X], [argument from cause], [Cau],
  [α], [FF], [Y is an EFFECT of X], [argument from effect], [Ef],
  [α], [FF], [Y is CORRELATED with X], [argument from correlation], [Cor],
  [α], [FF], [Y is a MOTIVE for X], [argument from motive], [Mot],
  [α], [FF], [Y EXCLUDES X], [argument from incompatibility], [Inc],
  [α], [VF], [Y is a CRITERION for X], [argument from criterion], [Cr],
  [α], [VF], [Y is the DEFINITION of X], [argument from definition], [Def],
  [α], [VF], [Y can be SUBSUMED under X], [argument from subsumption], [Su],
  [α], [VV], [Y is a NORM for X], [argument from norm], [Nor],
  [α], [VV], [Y is an INSTANTIATION of X], [argument from instantiation], [Ins],
  [α], [VV], [Y is a DISQUALIFIER of X], [argument from disqualifier], [Dis],
  [α], [PF], [Y is a PRAGMATIC MOTIVATION for X], [pragmatic argument], [Pra],
  [α], [PF], [Y is a PRIOR INVESTMENT in X], [argument from waste], [W],
  [α], [PF], [Y is the FEASIBILITY of X], [argument from possibility], [Pos],
  [α], [PV], [Y is a PRINCIPLED MOTIVATION for X], [argument from principle], [Pri],
  [α], [PV], [Y is an EVALUATIVE MOTIVATION for X], [argument from evaluation], [Ev],
  [α], [PP], [Y is a DEONTIC MOTIVATION for X], [deontic argument], [Deo],
  [α], [PP], [Y is a TELEOLOGIC MOTIVATION for X], [teleologic argument], [Tel],
  [β], [ss, pp, uu], [a is ANALOGOUS to b], [argument from analogy], [A],
  [β], [ss, pp, uu], [a is SIMILAR to b], [argument from similarity], [Sim],
  [β], [ss, pp, uu], [a is COMPARABLE to b], [argument from comparison], [Cpa],
  [β], [ss, pp, uu], [a is EQUAL to b], [argument from equality], [Eq],
  [β], [ss, pp, uu], [a is described METAPHORICALLY as b], [metaphoric argument], [Me],
  [β], [ss, pp, uu], [a is COMPOSED of b], [argument from composition], [Cpo],
  [β], [ss, pp, uu], [a is a PART of b], [argument from division], [Div],
  [β], [ss, pp, uu], [a RANKS BELOW b], [_argumentum a maiore_], [Ma],
  [β], [ss, pp, uu], [a RANKS ABOVE b], [_argumentum a minore_], [Mi],
  [β], [ss, pp, uu], [a OWES RECIPROCITY to b], [argument from reciprocity], [R],
  [β], [ps, us, up], [b is an EXAMPLE of a], [argument from example], [Exa],
  [β], [ps, us, up], [b is a SPECIES of a], [argument from species], [Sp],
  [β], [sp, su, pu], [a belongs to the TOTALITY of b], [argument from totality], [To],
  [β], [sp, su, pu], [a belongs to the GENUS of b], [argument from genus], [G],
  [γ], [i], [b is SYNONYMOUS to a and Y is SYNONYMOUS to X], [argument from synonyms], [Sy],
  [γ], [i], [b is the OPPOSITE of a and Y is the OPPOSITE of X], [argument from opposites], [Op],
  [γ], [i], [b is DERIVATIVE of a and Y is DERIVATIVE of X], [argument from derivatives], [Der],
  [γ], [i], [b is INTEGRATIVE of a and Y is INTEGRATIVE of X], [argument from integratives], [Int],
  [γ], [i], [b is the CONVERSE of a and Y is the CONVERSE of X], [argument from converses], [Cve],
  [γ], [d], [—], [non sequitur], [Non],
  [δ], [I], [Z is ETHOTICALLY AUTHORITATIVE for A], [ethotic argument], [Eth],
  [δ], [II], [Z is CHARACTERALLY AUTHORITATIVE for U], [_argumentum ad hominem_], [H],
  [δ], [II], [Z is a NEGATIVE MOTIVATION for A], [_argumentum ad baculum_], [B],
  [δ], [II], [Z is an OFFERED REWARD for A], [_argumentum ad carotam_], [Car],
  [δ], [II], [Z COMMITS the addressee to A], [argument from concession], [Cce],
  [δ], [II], [Z is an UNDESIRABLE IMPLICATION supporting U], [_argumentum ad consequentiam_], [Cse],
  [δ], [III], [Z is EPISTEMICALLY AUTHORITATIVE for A], [argument from expert opinion], [Exp],
  [δ], [III], [Z is MORALLY AUTHORITATIVE for A], [argument from moral authority], [Mor],
  [δ], [III], [Z is TESTIMONIALLY AUTHORITATIVE for A], [argument from testimony], [Tes],
  [δ], [III], [Z is POPULARLY AUTHORITATIVE for A], [_argumentum ad populum_], [Pop],
  [δ], [III], [Z is a PRESUMPTION in favor of A], [_argumentum ad ignorantiam_], [Ig],
)

*Connector fields.* The canonical form goes in four fields, matching the
template letters; `note` is for remarks. `transformations` lists each wording
change once, with its statement, in any order.
```text
conclusion subject    Socrates           a  (δ: q)
conclusion predicate  is mortal          X  (δ: [is acceptable] / [is unacceptable])
premise subject       all men            b  (α: a again; δ: q)
premise predicate     are mortal         Y  (β: X again; δ: Z)
transformations       —
```
