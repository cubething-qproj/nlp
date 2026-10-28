#set page(numbering: "1")

#let decide(body) = block(fill: luma(235), inset: 8pt, radius: 3pt, width: 100%)[*Decision needed (lead):* #body]

= Labelling philosophical texts: a guide for labellers

*What this is for.* Quell is a game in which players read in-world texts (excerpts of real philosophy), highlight passages, and write notes. The game works out which concepts a highlight or note is about, and NPCs respond when the right ones come up. Your labels are how the game knows what each passage is about and what it's doing. They are a careful reader's reading of the text, not a summary of it.

*Confidentiality.* The texts are excerpts from published books. Don't copy, export or share them outside the INCEpTION project. Made-up examples, like the ones in §9, are fine.

How the project is run (evaluation, automation, setup) is in `methods.typ`. You don't need it to label.

== 1. Glossary

/ Span: a stretch of text you've marked. Spans can overlap and nest.
/ Layer: one kind of question asked of the text (§3). Each span belongs to one layer.
/ Label, feature: a span's values. Each layer has a main label plus a few features (e.g. `voice`, `unsure`).
/ Relation: an arrow from one span to another, e.g. claim A is an `inference` to claim B.
/ Concept id: a short stable name for a concept, e.g. for "the Nothing". Players' notes are matched against these.
/ Pass: one read through a document for one layer.
/ Guideline version: the version of this guide you're labelling under. It changes when a rule changes.
/ Lead: the person who runs the project and reviews (curates) your work.

== 2. How the work runs

+ *Learn the tool.* Do INCEpTION's 20–30 minute Getting Started tutorial in a scratch project (ask the lead for one), then read §7.
+ *Calibrate.* You and the lead label the same one or two sections separately, then go through the differences together. Expect the guide to change afterwards.
+ *Label.* For each text: read it through, then do one pass per layer (§8). Mark each document finished when all four passes are done.
+ *Review.* The lead curates each finished document and tells you what changed in the guide. Re-read the changelog before your next session.
+ *Re-label.* At least a week later, you re-label a few documents the lead picked in advance, under a second account (`<you>-reread`). Don't look at your earlier labels first: the point is to see where the guide leaves room for two answers.

== 3. The scheme

A starting point, not an answer: expect labels to merge, split and get renamed after the first text. Every layer has an `unsure` flag, a free-text `note`, and a `continues` link for interrupted passages (§5). The closed-label layers (argument, move, reference) also have an `other` label.

=== concept: what is this about?

Unit: phrase to paragraph.

#table(
  columns: (auto, 1fr),
  [*feature*], [*values*],
  [`concept`], [the most specific matching entry in the knowledge base (§7); add it if it's missing],
  [`use`],
  [`defined` (the text says what X is or redefines it) · `discussed` (says something about X) · `mentioned` (X only appears)],
)

Concepts form a tree in the knowledge base. A broad concept (`nothing`) has narrower senses under it (Carnap's nothing as logical negation, Heidegger's nothing as what grounds the question of being). Tag the narrowest one that fits: the tree already says that both senses are kinds of `nothing`. A sense belongs to whoever holds it, not to the text it appears in: when Carnap quotes "the Nothing nothings", that span gets Heidegger's sense.

Describe each sense in its owner's own terms. What Carnap thinks of Heidegger's nothing goes on the argument and reference layers, not in the description of Heidegger's concept. Concepts about concepts (`meaning`, `pseudo-concept`) are ordinary entries.

#decide[concept naming in the knowledge base, and how deep the tree goes before the pilot.]

=== argument: what is it doing logically?

Unit: clause or sentence.

#table(
  columns: (auto, 1fr),
  [*label*], [*meaning*],
  [`thesis`], [the main claim of the text or section; few per text],
  [`claim`], [any other asserted proposition],
  [`example`], [a case offered as illustration or evidence],
  [`other`], [argumentative, but none of the above],
)

Premise and conclusion are roles, not labels: the same claim can be the conclusion of one step and a premise of the next. The relations say which. An objection is a claim with `voice: reported` that conflicts with another; a reply is a claim that conflicts with the objection.

Features: `voice` (`author` · `reported`), `reconstructed` (yes if you inferred the claim rather than read it off the page).

Relations, from one argument span to another. The names follow Inference Anchoring Theory (IAT), so our data maps onto its corpora and models.

#table(
  columns: (auto, 1fr),
  [*relation*], [*meaning*],
  [`inference`], [A is a reason for B],
  [`conflict`], [A is a reason against B],
  [`rephrase`], [A says B again in other words; common in continental texts],
)

Relation features:
- `strength` (on `inference`): `deductive` if B follows from A (with its linked partners) necessarily; `defeasible` if A only makes B plausible: induction, analogy, authority.
- `kind` (on `conflict`): `rebut` (B is false) · `undercut` (B doesn't follow from its reasons) · `dismiss` (B is meaningless or ill-formed: neither true nor false). Carnap's case against metaphysics is mostly `dismiss`.
- `group` (on `inference`): premises that only support B _together_, as in a syllogism, share a group name (`g1`, `g2`, …). Leave it empty for independent reasons.

Equivocation shows up across layers: the two sides of the argument link to different senses on the concept layer, and the conflict is an `undercut`.

=== move: what is it doing rhetorically?

Unit: sentence to paragraph.

#table(
  columns: (auto, 1fr),
  [*label*], [*meaning*],
  [`question`], [a real question that drives the text; a rhetorical question is not one (it's an `appeal` or an assertion)],
  [`distinction`], [splits one notion into two],
  [`analysis`], [takes a sentence or concept apart: logical or linguistic],
  [`wordplay`], [etymology, puns, playing a word against itself],
  [`appeal`], [to experience, mood, or intuition rather than reasons],
  [`concession`], [grants a point before turning],
  [`summary`], [gathers up what came before],
  [`other`], [a deliberate move, but none of the above],
)

=== reference: what does it point to?

Unit: the quoted or referring words.

#table(
  columns: (auto, 1fr),
  [*label*], [*meaning*],
  [`quote`], [words quoted from another text],
  [`citation`], [names an author or work],
  [`allusion`], [points to another text without naming it],
  [`other`], [points elsewhere, but none of the above],
)

Features: `target` (the work or author pointed to), `stance` (`agrees` · `disagrees` · `neutral`). Relations can't cross documents, so the link to another text lives in `target`.

#decide[does an example sentence the author invented (e.g. a sample of "metaphysical" talk) count as a reference?]

== 4. When to label something

There is no established scheme for philosophical texts; we're making one. These are rules of thumb, not rules. When one stops helping, say why in a `note`.

- *The margin-note test.* If you'd write something in the margin, there's a span. What you'd write tells you the layer:
  - "what is X?" or "so X means…" → *concept*
  - "why?", "so…", "but…" → *argument*
  - "what is he _doing_ here?" → *move*
  - "cf. Y", "this is aimed at Z" → *reference*
- *The summary test.* Write a 3–5 sentence summary of a section before labelling it. Every passage the summary relies on should carry a label; each summary sentence is roughly one thesis or claim.
- *The player test.* Players will highlight memorable lines, definitions and provocations. If you can picture someone highlighting it, label it in some layer, even if only `other`.
- *Concepts: does it change what a reader thinks X is?* If yes, it's `defined` or `discussed`. If X only appears, it's `mentioned`: tag mentions only when cheap, e.g. the first one in a section.
- *Arguments: can you say "because" or "therefore" between two spans?* If you can state the link, it's argument structure. If you can't, but the passage still persuades, it's probably a move.
- *Moves: does the force come from how it's said rather than what?* Questions, wordplay, appeals to experience, sudden redefinitions.
- *Whose view is it?* Philosophers constantly voice positions they reject. Always set `voice`: the author's own view, or one they report or attack.
- *Explicit or reconstructed?* Carnap states his premises; with Heidegger you'll often be inferring them. If you write in a premise the text doesn't state, set `reconstructed` (§7 shows how).
- *Density check.* If more than about half of a page's text is covered in one layer, your unit is too big or you're labelling everything. If a page of an argumentative text has no argument labels, look again.

== 5. Boundaries

- Each layer snaps to a fixed unit (word, clause, sentence); the tool enforces part of this (§7).
- Leave discourse markers ("therefore", "but", "yet") out of argument spans: they're evidence for the relation, not part of the claim. The move layer can tag them if they matter.
- Leave out trailing punctuation and surrounding quotation marks, unless the quote itself is the point (reference layer).
- An interrupted passage is one annotation, not two: label the first part, and link the other parts to it with `continues`.
- When unsure where a span ends, take the shortest span that still makes sense alone.
- If the text shows emphasis markup, spans nest cleanly with it. A span covering a whole emphasised phrase includes the delimiters (`_nothing_`, not `nothing`); a span inside one leaves them out entirely. Never start inside a pair and end outside it (`_noth|ing_ nothings|`).

#decide[text handling: footnotes, translator's notes, headings, and original-language words in brackets. Label them, skip them, or label only on the reference layer?]

== 6. Hard cases to settle as you go

- *Mention vs. discussion.* Tag the concept either way; `use` says which it is.
- *Author-relative senses.* If the right sense doesn't exist yet, add it under the broad concept. If you can't tell whose sense a span uses, tag the broad concept, mark it `unsure`, and say why in `note`.
- *Torn between two fine labels?* Use the coarse one (e.g. `other` with `unsure`) and write both candidates in `note`.
- *New concepts:* just add them. The lead prunes the ones that never come back.

== 7. Working in INCEpTION

Open the address the lead gives you, log in, open the project, then *Annotation*. The guide is under the book icon at the top.

*Before a pass.* _Settings_ → _Layer preferences_: hide every layer except the one you're doing (hiding Argument also hides its relations). Raise _Page size_ (sentences per page) so long relations stay on screen.

*Spans.* Pick the layer in the _Layer_ box on the right, then select text with the mouse (double-click selects one word). The span snaps to the layer's unit. Set the label and features in the panel on the right. Everything saves automatically; there's no save button.

*Concepts.* In the `concept` field, start typing a label, or press Space to search for the selected text. Each candidate shows its description: read it before choosing. You can also browse the tree instead of searching. If the concept or sense is missing, add it on the project's _Knowledge Base_ page, under its broad concept and with a one-line description, then come back and link it.

*Relations* (argument layer). Drag from the source span to the target. For distant spans, select the source, scroll to the target, right-click it, and choose _Link to…_. Shift+Space reverses the selected relation; holding Ctrl when you release cancels.

*Interrupted passages.* On the first part, add a `continues` slot, click it to arm it, then double-click the other part's span.

*Reconstructed premises.* Shift+click where the premise belongs to make a zero-width argument span. Set `reconstructed` and write the premise in `note`.

*Mentions in bulk.* Select one `mentioned` concept annotation as a template, search for the word in the search sidebar, untick any result you don't want (all are ticked by default), then create annotations for the rest. Use this only for `mentioned`.

*Pass record.* When you finish a pass, open the _Document Metadata_ sidebar (tags icon), choose _Pass_, click +, and fill in layer, guideline version, date and minutes spent.

*Reviewing a pass.* The annotation sidebar grouped _by position_ lists everything in reading order. Shift+← and Shift+→ step through the current layer's annotations.

*Finishing.* The lock icon (or Ctrl+End) marks a document finished, which sends it to the lead. Do this only after all four passes.

Keys worth knowing: Ctrl+Z undo (the history is lost when you switch documents) · Shift+Delete delete the selected annotation · Shift+Esc deselect · Shift+PageDown/PageUp next/previous document.

Don't: _Reset_ a document (it deletes your work permanently), export documents, or click grey suggestions if any ever appear (one click accepts them).

If the page stops responding or your session times out, reload and log in again; nothing is lost.

== 8. Running a session

- Read the whole text once without labelling. You can't place an argument's boundaries until you know where it goes.
- One layer per pass: concepts, then arguments, then moves, then references.
- Warm up: re-read that layer's section of this guide and the changelog, and re-label one passage you've done before. If you'd now label it differently, settle that first.
- Sessions of 45–60 minutes.
- Flag, don't skip: mark a low-confidence span `unsure` rather than leaving it out, and say why in `note` (where, the two candidate labels, what you chose). Your notes become the guide's hard cases.
- If `other` passes roughly 10–15% of a layer, the label set is missing something. Say so to the lead.

== 9. Two worked examples

Both passages are made up, written to imitate each style.

*Analytic style.*

#quote(block: true)[
  (1) A sentence means something only if we can say what observation would confirm it. (2) No observation could confirm "the absolute is restless". (3) So that sentence, whatever its grammar suggests, says nothing.
]

- argument: (1) `claim`, (2) `claim`, (3) `thesis`. (1) and (2) are each an `inference` to (3), `strength: deductive`, `group: g1`: neither works without the other. "So" stays outside (3).
- concept: `meaning` in (1), `use: defined`; `verification` in (1), `discussed`.
- move: whole passage `analysis`.
- reference: "the absolute is restless" is an invented sample sentence. Whether that's a reference is the open decision in §3; until it's made, tag it `other` + `unsure` with `stance: disagrees`.

*Continental style.*

#quote(block: true)[
  (1) We ask about the clearing. (2) But are we not already standing in it whenever we ask at all? (3) The question turns back on the one who asks it. (4) To ask _about_ the clearing is already to be _in_ it.
]

- move: (1) `question`: it sets the topic. (2) is rhetorical, so by the definition it's not a `question`. It asserts that we already stand in the clearing, and persuades by appeal to what asking is like: `appeal`, `unsure`. (3) `wordplay`? It could be `analysis`. Tag `other` + `unsure` and put both candidates in `note`.
- argument: (4) `claim`, `reconstructed: no`, because it's stated. Because (2) is read as rhetorical, it asserts something, so (2) is an `inference` to (4), `strength: defeasible`; (3) is a `rephrase` of (4). A hidden premise ("asking requires already standing in what is asked about") is a zero-width span with `reconstructed: yes`, if you write it in.
- concept: `clearing` in (1)–(4), `discussed`; arguably `defined` by (4).
- The emphasis in (4) is the only thing marking the contrast. If the text in the tool has lost it, tell the lead.

== Before each session

- [ ] Changelog read; guideline version noted
- [ ] Other layers hidden
- [ ] Warm-up passage re-labelled
- [ ] `Pass` filled in when the pass ends

== Further reading

Optional. Background for the scheme and heuristics.

- Stab, Gurevych. "Parsing Argumentation Structures in Persuasive Essays." _Computational Linguistics_ 43(3), 2017. Claim/premise scheme and its guidelines. #link("https://aclanthology.org/J17-3005/")
- ARG-tech. Inference Anchoring Theory guidelines, 2023. The source of the relation names. #link("https://github.com/arg-tech/aif-arg-datasets/blob/main/docs_add_info/IAT_guidelines_and_tutorials-2023-10.pdf")
- Peldszus, Stede. "From Argument Diagrams to Argumentation Mining in Texts: A Survey." _Int. J. of Cognitive Informatics and Natural Intelligence_ 7(1), 2013. Linked vs. convergent premises; rebut vs. undercut.
- Pareti. "PARC 3.0: A Corpus of Attribution Relations." LREC 2016. Annotating whose view a passage voices. #link("https://aclanthology.org/L16-1619/")
- Teufel, Moens. "Summarizing Scientific Articles: Experiments with Relevance and Rhetorical Status." _Computational Linguistics_ 28(4), 2002. Argumentative zoning, a cousin of the move layer. #link("https://aclanthology.org/J02-4002/")
- Lawrence, Reed. "Argument Mining: A Survey." _Computational Linguistics_ 45(4), 2019. #link("https://aclanthology.org/J19-4006/")
- Not online: Pollock, "Defeasible Reasoning", _Cognitive Science_ 11(4), 1987 (rebut vs. undercut); Toulmin, _The Uses of Argument_ (1958); Walton, Reed, Macagno, _Argumentation Schemes_ (2008); Swales, _Genre Analysis_ (1990), the origin of "moves"; Mann, Thompson, "Rhetorical Structure Theory", _Text_ 8(3), 1988.
- INCEpTION User Guide, release 42.1. #link("https://inception-project.github.io/releases/42.1/docs/user-guide.html")
