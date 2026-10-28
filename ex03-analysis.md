# ex03: Aristotle on the motion of the earth

Worked PTA analysis of `pta-test` document `ex03`, on Aristotle's reading.
Quotes Finocchiaro's translation of Galileo: don't commit.

## Text

> Who is so blind as not to see that the parts of the element earth and of the
> element water, being heavy bodies, move naturally downwards, namely toward the
> center of the universe, assigned by nature herself as the goal and end of
> straight downward motion… Since this can be seen clearly, and since we are
> sure that the same holds for the whole as for the parts, must we not conclude
> that the natural motion of the [whole globe] earth is straight toward the
> center…?

## Reading

Aristotle's, not Galileo's. "Downwards" means toward the center of the
_universe_, and the passage argues that the whole earth moves there: the
geocentric thesis. The website follows Galileo's critique, reading "the
center" as the center of the earth, which makes the conclusion incoherent (and
drops T2 and T5 below).

## How it was decomposed

Working principles, ours rather than ATIP's (ATIP types one triad at a time):

1. Read the author charitably: the reading the author intends.
2. One triad per reason-giving construction ("because", "since", "so", "must
   we not conclude", participles like "being", appositions like "namely").
3. A stated generalisation linking two statements is a lever candidate before
   a premise candidate.
4. Every statement that is argued for gets its own triad.
5. Add implicit statements only where a triad can't be canonicalized without
   them.

## Structure

```mermaid
flowchart BT
  S2["S2 · heavy bodies move downwards<br/>(implicit)"] -- premise --> T1((T1))
  S1["S1 · the parts are heavy bodies"] -- lever --> T1
  T1 -- conclusion --> S3["S3 · the parts move downwards"]
  S3 -- premise --> T2((T2))
  S4["S4 · downward motion is motion<br/>toward the center of the universe"] -- lever --> T2
  T2 -- conclusion --> S5["S5 · the parts move toward<br/>the center of the universe"]
  S9["S9 · nature herself assigned that goal"] -- premise --> T5((T5))
  T5 -- conclusion --> S4
  S6["S6 · this can be seen clearly"] -- premise --> T3((T3))
  T3 -- conclusion --> S5
  S5 -- premise --> T4((T4))
  S7["S7 · what holds for the parts<br/>holds for the whole"] -- lever --> T4
  T4 -- conclusion --> S8["S8 · the whole earth moves toward<br/>the center of the universe"]
```

Five triads in one chain: T1 → T2 → T4, with T3 backing T2's conclusion and
T5 backing T2's lever. Three levers (S1, S4, S7) are stated in the text; one
of them (S4) is itself argued for.

## Step 2 decisions

- **Rhetorical questions become assertions.** "Who is so blind as not to see
  that q" → q. "Must we not conclude that r" → r.
- **Illocutive markers are stripped.** "we are sure that" is the arguer's
  stance, not part of S7.
- **"downwards" and "toward the center of the universe" are kept apart.**
  Merging them would hide T2, which is the contested step.
- **"the whole earth" is universal (u), not singular (s)**: it stands for all
  its parts taken together.

## Statements

```yaml
S1:
  span: "being heavy bodies"
  subj: the parts of the element earth and of the element water
  pred: are heavy bodies
  role: lever of T1

S2:
  span: zero-width, after "heavy bodies"
  implicit: true
  subj: heavy bodies
  pred: move naturally downwards
  role: premise of T1

S3:
  span: "the parts of the element earth and of the element water, being heavy bodies, move naturally downwards"
  subj: the parts of the element earth and of the element water
  pred: move naturally downwards
  role: conclusion of T1, premise of T2

S4:
  span: "downwards, namely toward the center of the universe"
  subj: downward motion
  pred: is motion toward the center of the universe
  role: lever of T2, conclusion of T5

S5:
  span: "the parts of the element earth and of the element water … move naturally downwards, namely toward the center of the universe"
  subj: the parts of the element earth and of the element water
  pred: move naturally toward the center of the universe
  role: conclusion of T2 and T3, premise of T4

S6:
  span: "this can be seen clearly"
  subj: this [= S5]
  pred: can be seen clearly
  role: premise of T3

S7:
  span: "the same holds for the whole as for the parts"
  subj: what holds for the parts
  pred: holds for the whole
  role: lever of T4
  note: '"we are sure that" stripped as an illocutive marker'

S8:
  span: "the natural motion of the [whole globe] earth is straight toward the center"
  subj: the whole earth
  pred: moves naturally toward the center of the universe
  role: conclusion of T4

S9:
  span: "assigned by nature herself as the goal and end of straight downward motion"
  subj: that downward motion is motion toward the center of the universe [= S4]
  pred: has been assigned by nature herself
  role: premise of T5
```

## Triads

```yaml
T1:
  anchor: "being"
  formula: "S3 ∵ S2 [L: S1]"
  canonicalization: >
    the parts of earth and water move naturally downwards
    BECAUSE heavy bodies move naturally downwards
  subjects:
    delta: false
    equal: false
    reason: '"the parts of earth and water" != "heavy bodies"'
  predicates:
    equal: true
    reason: '"move naturally downwards" == "move naturally downwards"'
  form: beta
  substance: "β pu"
  substance_reason: >
    conclusion: the parts of earth and water are some heavy bodies (p);
    premise: heavy bodies in general (u)
  lever: GENUS
  lever_statement: S1
  classification: "β pu G"
  reconstruction: >
    'the parts of earth and water move naturally downwards'
    BECAUSE 'the parts of earth and water belong to the GENUS of heavy bodies'
    AND 'heavy bodies move naturally downwards'
  confidence: medium
  note: >
    The classic syllogism. If read as "all the parts" (u), the substance is uu,
    where GENUS isn't listed: novel.

T2:
  anchor: "namely"
  formula: "S5 ∵ S3 [L: S4]"
  canonicalization: >
    the parts of earth and water move naturally toward the center of the universe
    BECAUSE the parts of earth and water move naturally downwards
  subjects:
    delta: false
    equal: true
    reason: '"the parts of earth and water" == "the parts of earth and water"'
  predicates:
    equal: false
    reason: '"move toward the center of the universe" != "move downwards"'
  form: alpha
  substance: "α FF"
  substance_reason: both predicates are checkable claims about motion
  lever: novel
  lever_statement: S4
  lever_written_out: "Y (moving downwards) is IDENTICAL to X (moving toward the center of the universe)"
  classification: "α FF novel"
  reconstruction: >
    'the parts of earth and water move naturally toward the center of the universe'
    BECAUSE 'moving downwards IS moving toward the center of the universe'
    AND 'the parts of earth and water move naturally downwards'
  confidence: medium
  note: >
    The contested step: it identifies "down" with "toward the center of the
    universe". A definitional lever between two factual predicates; the PTA
    lists DEFINITION only under VF. Either a gap in the table or a step 2
    decision presented as an argument.

T3:
  anchor: "Since" (the first one)
  formula: "S5 ∵ S6"
  canonicalization: >
    that the parts of earth and water move naturally toward the center of the
    universe (q) [is acceptable (A)] BECAUSE q can be seen clearly
  subjects:
    delta: true
    reason: '"this" = S5: the premise is about the claim as a whole'
  form: delta
  substance: "δ II"
  substance_reason: >
    the source of "can be seen clearly" is anyone who looks, including the
    addressee ("who is so blind as not to see"); no listed II lever fits
  lever: novel
  lever_written_out: "Z (being plainly visible) is a PERCEPTUAL GUARANTEE for A"
  classification: "δ II novel"
  confidence: low
  note: >
    An appeal to obviousness. "Who is so blind" also jabs at anyone who denies
    q (ad hominem, δ II H), but that lever concludes U about an opponent's
    view, not A about q.

T4:
  anchor: "must we not conclude"
  formula: "S8 ∵ S5 [L: S7]"
  canonicalization: >
    the whole earth moves naturally toward the center of the universe
    BECAUSE the parts of earth and water move naturally toward the center of the universe
  subjects:
    delta: false
    equal: false
    reason: '"the whole earth" != "the parts of earth and water"'
  predicates:
    equal: true
    reason: '"moves toward the center of the universe" == "move toward the center of the universe"'
  form: beta
  substance: "β uu"
  substance_reason: >
    conclusion: the whole earth as all its parts together (u);
    premise: all the parts (u)
  lever: COMPOSED
  lever_statement: S7
  classification: "β uu Cpo"
  reconstruction: >
    'the whole earth moves naturally toward the center of the universe'
    BECAUSE 'the whole earth is COMPOSED of the parts of earth and water,
    and what holds for the parts holds for the whole'
    AND 'the parts of earth and water move naturally toward the center of the universe'
  confidence: high
  note: >
    S7 states the lever's general principle; the composition fact ("the earth
    is composed of earth and water") is implicit, recorded here rather than
    as a statement. Same type as the website's, on a different reading.

T5:
  anchor: "assigned by"
  formula: "S4 ∵ S9"
  canonicalization: >
    THE PROPOSITION 'downward motion is motion toward the center of the universe' (q)
    [IS ACCEPTABLE (A)] BECAUSE q has been assigned by nature herself
  subjects:
    delta: true
    reason: 'S9 is about S4 as a whole: where the claim comes from'
  form: delta
  substance: "δ III"
  substance_reason: nature is a third party, and the source Aristotle defers to
  lever: EPISTEMICALLY AUTHORITATIVE
  classification: "δ III Exp"
  reconstruction: >
    THE PROPOSITION 'downward motion is motion toward the center of the universe'
    IS ACCEPTABLE BECAUSE 'nature is EPISTEMICALLY AUTHORITATIVE about motion'
    AND 'nature herself has assigned it so'
  confidence: medium
  note: >
    Supports T2's lever: the lever recursion the PTA singles out. "Herself"
    marks nature as the source. If Exp is a stretch, novel: "Z is NATURALLY
    AUTHORITATIVE for A". Alternative reading: α FF Cau, nature's assigned goal
    as the final cause of the motion.
```

## Labelling in INCEpTION

| object | type | span / anchor | links |
| ------ | ---- | ------------- | ----- |
| S1, S3–S9 | Statement | as listed above (S3 and S5 overlap) | — |
| S2 | Statement | zero-width (Shift+click), wording in `note` | — |
| T1 | Connector | "being" | conclusion S3, premise S2, lever statement S1 |
| T2 | Connector | "namely" | conclusion S5, premise S3, lever statement S4 |
| T3 | Connector | first "Since" | conclusion S5, premise S6 |
| T4 | Connector | "must we not conclude" | conclusion S8, premise S5, lever statement S7 |
| T5 | Connector | "assigned by" | conclusion S4, premise S9 |

Only T4 has a website answer (`β uu Cpo`, on Galileo's reading).
