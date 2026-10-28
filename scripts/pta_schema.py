"""Generate the PTA labelling schema for INCEpTION.

Writes two files next to the other INCEpTION config:

- inception/pta-layers.json: layers to import under Settings -> Layers.
  `Statement` spans are the nodes; a `Connector` span is one PTA argument,
  linking one conclusion, one premise and one lever statement, and carrying
  the argument's form, substance and lever keyword, its canonical subjects and
  predicates with the transformations that produced them, plus the concepts it
  is about (`concept` or `concept/sense`, several allowed). A `Cue` span records
  the disposition of a cue that isn't a connector (document analysis, D2).
- inception/pta-constraints.txt: constraint rules to import under Settings ->
  Constraints. They put the substances valid for the chosen form, and the
  levers valid for the chosen substance, first and in bold. They don't forbid
  other values; the converter rejects invalid combinations.

The type table is PTA 3.1 (Wagemans, ATIP v6, Table 7).

Usage: python scripts/pta_schema.py
"""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "inception"
CONNECTOR = "webanno.custom.Connector"
STATEMENT = "webanno.custom.Statement"
CUE = "webanno.custom.Cue"

# form -> substance -> [(keyword, lever statement, name, symbol)]
BETA_SAME = [
    ("ANALOGOUS", "a is ANALOGOUS to b", "argument from analogy", "A"),
    ("SIMILAR", "a is SIMILAR to b", "argument from similarity", "Sim"),
    ("COMPARABLE", "a is COMPARABLE to b", "argument from comparison", "Cpa"),
    ("EQUAL", "a is EQUAL to b", "argument from equality", "Eq"),
    ("METAPHORICALLY", "a is described METAPHORICALLY as b", "metaphoric argument", "Me"),
    ("COMPOSED", "a is COMPOSED of b", "argument from composition", "Cpo"),
    ("PART", "a is a PART of b", "argument from division", "Div"),
    ("RANKS BELOW", "a RANKS BELOW b", "argumentum a maiore", "Ma"),
    ("RANKS ABOVE", "a RANKS ABOVE b", "argumentum a minore", "Mi"),
    ("OWES RECIPROCITY", "a OWES RECIPROCITY to b", "argument from reciprocity", "R"),
]
BETA_DOWN = [
    ("EXAMPLE", "b is an EXAMPLE of a", "argument from example", "Exa"),
    ("SPECIES", "b is a SPECIES of a", "argument from species", "Sp"),
]
BETA_UP = [
    ("TOTALITY", "a belongs to the TOTALITY of b", "argument from totality", "To"),
    ("GENUS", "a belongs to the GENUS of b", "argument from genus", "G"),
]
TYPES = {
    "alpha": {
        "FF": [
            ("SIGN", "Y is a SIGN of X", "argument from sign", "Sig"),
            ("CAUSE", "Y is a CAUSE of X", "argument from cause", "Cau"),
            ("EFFECT", "Y is an EFFECT of X", "argument from effect", "Ef"),
            ("CORRELATED", "Y is CORRELATED with X", "argument from correlation", "Cor"),
            ("MOTIVE", "Y is a MOTIVE for X", "argument from motive", "Mot"),
            ("EXCLUDES", "Y EXCLUDES X", "argument from incompatibility", "Inc"),
        ],
        "VF": [
            ("CRITERION", "Y is a CRITERION for X", "argument from criterion", "Cr"),
            ("DEFINITION", "Y is the DEFINITION of X", "argument from definition", "Def"),
            ("SUBSUMED", "Y can be SUBSUMED under X", "argument from subsumption", "Su"),
        ],
        "VV": [
            ("NORM", "Y is a NORM for X", "argument from norm", "Nor"),
            ("INSTANTIATION", "Y is an INSTANTIATION of X", "argument from instantiation", "Ins"),
            ("DISQUALIFIER", "Y is a DISQUALIFIER of X", "argument from disqualifier", "Dis"),
        ],
        "PF": [
            ("PRAGMATIC MOTIVATION", "Y is a PRAGMATIC MOTIVATION for X", "pragmatic argument", "Pra"),
            ("PRIOR INVESTMENT", "Y is a PRIOR INVESTMENT in X", "argument from waste", "W"),
            ("FEASIBILITY", "Y is the FEASIBILITY of X", "argument from possibility", "Pos"),
        ],
        "PV": [
            ("PRINCIPLED MOTIVATION", "Y is a PRINCIPLED MOTIVATION for X", "argument from principle", "Pri"),
            ("EVALUATIVE MOTIVATION", "Y is an EVALUATIVE MOTIVATION for X", "argument from evaluation", "Ev"),
        ],
        "PP": [
            ("DEONTIC MOTIVATION", "Y is a DEONTIC MOTIVATION for X", "deontic argument", "Deo"),
            ("TELEOLOGIC MOTIVATION", "Y is a TELEOLOGIC MOTIVATION for X", "teleologic argument", "Tel"),
        ],
        "FV": [], "FP": [], "VP": [],
    },
    "beta": {
        **{t: BETA_SAME for t in ("ss", "pp", "uu")},
        **{t: BETA_DOWN for t in ("ps", "us", "up")},
        **{t: BETA_UP for t in ("sp", "su", "pu")},
    },
    "gamma": {
        "i": [
            ("SYNONYMOUS", "b is SYNONYMOUS to a and Y is SYNONYMOUS to X", "argument from synonyms", "Sy"),
            ("OPPOSITE", "b is the OPPOSITE of a and Y is the OPPOSITE of X", "argument from opposites", "Op"),
            ("DERIVATIVE", "b is DERIVATIVE of a and Y is DERIVATIVE of X", "argument from derivatives", "Der"),
            ("INTEGRATIVE", "b is INTEGRATIVE of a and Y is INTEGRATIVE of X", "argument from integratives", "Int"),
            ("CONVERSE", "b is the CONVERSE of a and Y is the CONVERSE of X", "argument from converses", "Cve"),
        ],
        "d": [("none", "no lever: the premise is irrelevant", "non sequitur", "Non")],
    },
    "delta": {
        "I": [
            ("ETHOTICALLY AUTHORITATIVE", "Z is ETHOTICALLY AUTHORITATIVE for A", "ethotic argument", "Eth"),
        ],
        "II": [
            ("CHARACTERALLY AUTHORITATIVE", "Z is CHARACTERALLY AUTHORITATIVE for U", "argumentum ad hominem", "H"),
            ("NEGATIVE MOTIVATION", "Z is a NEGATIVE MOTIVATION for A", "argumentum ad baculum", "B"),
            ("OFFERED REWARD", "Z is an OFFERED REWARD for A", "argumentum ad carotam", "Car"),
            ("COMMITS", "Z COMMITS the addressee to A", "argument from concession", "Cce"),
            ("UNDESIRABLE IMPLICATION", "Z is an UNDESIRABLE IMPLICATION supporting U", "argumentum ad consequentiam", "Cse"),
        ],
        "III": [
            ("EPISTEMICALLY AUTHORITATIVE", "Z is EPISTEMICALLY AUTHORITATIVE for A", "argument from expert opinion", "Exp"),
            ("MORALLY AUTHORITATIVE", "Z is MORALLY AUTHORITATIVE for A", "argument from moral authority", "Mor"),
            ("TESTIMONIALLY AUTHORITATIVE", "Z is TESTIMONIALLY AUTHORITATIVE for A", "argument from testimony", "Tes"),
            ("POPULARLY AUTHORITATIVE", "Z is POPULARLY AUTHORITATIVE for A", "argumentum ad populum", "Pop"),
            ("PRESUMPTION", "Z is a PRESUMPTION in favor of A", "argumentum ad ignorantiam", "Ig"),
        ],
    },
}

GREEK = {"alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ"}
FORMS = {
    "alpha": "a is X because a is Y: same subject, different predicates. "
             "E.g. the minister did a great job because the minister raised the budget.",
    "beta": "a is X because b is X: same predicate, different subjects. "
            "E.g. Socrates is mortal because all men are mortal.",
    "gamma": "a is X because b is Y: nothing shared. "
             "E.g. peace can be started by truth because war can be started by lies.",
    "delta": "q is A/U because q is Z: the premise says something about the conclusion as a whole "
             "(who says it, what follows from it). E.g. the economy grew [is acceptable] "
             "because Eurostat says so.",
}
DISPOSITIONS = {
    "lever": "It introduces a stated lever of a connector. "
             "E.g. 'given that Socrates is a man', 'as robots are just like us'.",
    "rephrase": "It restates something; no argument. "
                "E.g. 'namely', 'that is', 'in other words': 'a bachelor, that is, an unmarried man'.",
    "conflict": "It attacks a statement; say which in note. "
                "E.g. 'but', 'however', 'some say … yet', 'this cannot be, for …'.",
    "background": "Explanation or context; no argument. "
                  "E.g. 'here nature means the cosmos as a whole', 'after a long winter, …'.",
    "rhetorical": "Framing only; its content is kept, the framing dropped. "
                  "E.g. 'who could deny that …?', 'is it not obvious that …?', 'clearly', "
                  "'we are sure that', 'I would argue that', 'you should accept that'.",
    "unresolved": "Undecided; say why in note. "
                  "E.g. a 'thus' that may be sequence or inference.",
}
# ATIP step 2 transformations that change a subject's or predicate's wording.
# Transposition, "because" and dropped markers are left out: the links, the
# Connector's anchor and Cue spans already record them.
TRANSFORMATIONS = {
    "anaphora": "A reference replaced by what it refers to. "
                "E.g. 'it' -> 'unauthorized downloading'.",
    "explication": "Implicit content made explicit. "
                   "E.g. 'why should you?' -> 'why should you stop carrying guns?'.",
    "illocution substitution": "A rhetorical question (or other illocution) turned into "
                               "an assertion. E.g. 'why should you?' -> 'you should not'.",
    "passivization": "Active turned passive to bring out a shared term. "
                     "E.g. 'many people have said q' -> 'q has been said by many people'.",
    "activization": "Passive turned active to bring out a shared term. "
                    "E.g. 'the budget was raised by the minister' -> 'the minister raised the budget'.",
    "nominalisation": "A clause turned into a noun phrase (ours, not ATIP's). "
                      "E.g. 'to be immature is easy' -> 'being immature is easy'.",
    "same term": "Two wordings judged to be one term (not an ATIP transformation). "
                 "E.g. 'the obedience of all to the will of one' = 'authority'.",
}
STATEMENT_TYPE = {"F": "fact", "V": "value", "P": "policy"}
QUANTITY = {"s": "singular", "p": "particular", "u": "universal"}
OTHER_SUBSTANCES = {
    "i": "identical: the subjects relate as the predicates do. "
         "E.g. peace/war as truth/lies",
    "d": "different: no shared relation (try inserting a middle step first). "
         "E.g. the tram is late because my cat is grey",
    "I": "first person: the arguer is the source. E.g. trust me, I've done this for twenty years",
    "II": "second person: the addressee (threats, rewards, commitments). "
          "E.g. agree, or you're fired; you said so yourself last week",
    "III": "third person: an expert, a witness, the public. E.g. doctors agree that …",
}


def substance_description(t: str) -> str:
    """Spell out a substance code, conclusion first."""
    if t in OTHER_SUBSTANCES:
        return OTHER_SUBSTANCES[t]
    names = STATEMENT_TYPE if t[0] in STATEMENT_TYPE else QUANTITY
    return f"conclusion {names[t[0]]}, premise {names[t[1]]}"


def substance_tag(form: str, t: str) -> str:
    """Substance tag, prefixed with the form: tag names may compare
    case-insensitively, which would merge `pp` with `PP` and `i` with `I`."""
    return f"{GREEK[form]} {t}"


def tagset(name: str, tags: list[tuple[str, str]]) -> dict:
    return {
        "name": name,
        "description": name,
        "language": None,
        "create_tag": False,
        "tags": [{"tag_name": n, "tag_description": d} for n, d in tags],
    }


def feature(name: str, rank: int, description: str, **kw) -> dict:
    base = {
        "name": name,
        "uiName": name,
        "type": "uima.cas.String",
        "description": description,
        "enabled": True,
        "visible": False,
        "include_in_hover": True,
        "required": False,
        "remember": False,
        "hideUnconstraintFeature": False,
        "multi_value_mode": "NONE",
        "link_mode": "NONE",
        "curatable": True,
        "rank": rank,
        "tag_set": None,
        "traits": None,
    }
    return base | kw


def link(name: str, ui_name: str, rank: int, description: str) -> dict:
    """A link feature from a Connector to Statement spans, role labels off."""
    return feature(
        name, rank, description,
        uiName=ui_name,
        type=STATEMENT,
        include_in_hover=False,
        multi_value_mode="ARRAY",
        link_mode="WITH_ROLE",
        traits=json.dumps({"enableRoleLabels": False}),
        link_type_name=f"{CONNECTOR}{name[0].upper()}{name[1:]}Link",
        link_type_role_feature_name="role",
        link_type_target_feature_name="target",
    )


def layer(name: str, ui_name: str, description: str, features: list[dict]) -> dict:
    return {
        "name": name,
        "uiName": ui_name,
        "type": "span",
        "description": description,
        "enabled": True,
        "built_in": False,
        "readonly": False,
        "cross_sentence": True,
        "show_hover": True,
        "anchoring_mode": "TOKENS",
        "overlap_mode": "ANY_OVERLAP",
        "validation_mode": "ALWAYS",
        "allow_stacking": True,
        "lock_to_token_offset": False,
        "multiple_tokens": True,
        "linked_list_behavior": False,
        "features": features,
    }


def text(name: str, ui_name: str, rank: int, description: str) -> dict:
    """A free-text feature that grows with its content."""
    return feature(
        name, rank, description,
        uiName=ui_name,
        traits=json.dumps({"multipleRows": True, "dynamicSize": True}),
    )


def note(rank: int, description: str = "Doubts, the label you nearly chose, "
                                       "or the wording of an implicit statement.") -> dict:
    return text("note", "note", rank, description)


def levers() -> dict[str, tuple[str, str]]:
    """Every lever keyword, once, with its description."""
    out = {}
    for subs in TYPES.values():
        for entries in subs.values():
            for kw, statement, name, symbol in entries:
                out[kw] = (statement, f"{name} ({symbol})")
    return out


def layers() -> list[dict]:
    substances = [(substance_tag(f, t), substance_description(t))
                  for f, subs in TYPES.items() for t in subs]
    lever_tags = [(kw, f"{s}. {n}") for kw, (s, n) in levers().items()]
    lever_tags.append(("novel", "None of the listed levers fits: write it out in note."))
    transformation_tags = [(f"{kind} ({side})", f"{d} Applied to the {side}.")
                           for kind, d in TRANSFORMATIONS.items()
                           for side in ("conclusion", "premise")]
    statement = layer(
        STATEMENT, "Statement",
        "A conclusion, premise or lever. Its role comes from the connectors linking it. "
        "Implicit statements are zero-width (Shift+click) with their wording in note. "
        "E.g. in 'Socrates is a man; therefore he is mortal': 'Socrates is a man', "
        "'he is mortal' (note: Socrates is mortal), and a zero-width 'All men are mortal'.",
        [note(1)],
    )
    connector = layer(
        CONNECTOR, "Connector",
        "One PTA argument: one conclusion, one premise, one lever. "
        "Anchor on the coherence marker (because, so, …), or zero-width if there is none. "
        "E.g. on 'therefore' in 'Socrates is a man; therefore he is mortal': conclusion "
        "'he is mortal', premise the implicit 'All men are mortal', lever statement "
        "'Socrates is a man'; beta, β su, GENUS.",
        [
            feature("form", 1, "Which elements conclusion and premise share.",
                    visible=True, tag_set=tagset("PTA forms", list(FORMS.items())),
                    traits=json.dumps({"editorType": "RADIOGROUP"})),
            feature("substance", 2, "Prefixed with the form; conclusion first, then premise.",
                    visible=True,
                    tag_set=tagset("PTA substances", substances)),
            feature("lever", 3, "The lever keyword.",
                    visible=True, tag_set=tagset("PTA levers", lever_tags)),
            link("conclusion", "conclusion", 4,
                 "The statement argued for. Exactly one. E.g. 'Socrates is mortal'."),
            link("premise", "premise", 5,
                 "The reason given; when two statements support jointly, the one the text marks "
                 "as the reason, else the generalization. Exactly one. E.g. 'all men are mortal'."),
            link("leverStatement", "lever statement", 6,
                 "The lever as a statement, only if the text states it or argues about it; "
                 "otherwise leave empty (the lever keyword is enough). At most one. "
                 "E.g. 'Socrates is a man' (membership), 'robots are just like us' (likeness)."),
            text("conclusionSubject", "conclusion subject", 7,
                 "The conclusion's subject in canonical form: a in the lever templates; "
                 "for delta, the whole proposition q. E.g. 'Socrates'."),
            text("conclusionPredicate", "conclusion predicate", 8,
                 "The conclusion's predicate in canonical form: X in the lever templates; "
                 "for delta, '[is acceptable]' or '[is unacceptable]' (A/U). E.g. 'is mortal'."),
            text("premiseSubject", "premise subject", 9,
                 "The premise's subject in canonical form: b in the lever templates "
                 "(a again for alpha); for delta, q. E.g. 'all men'."),
            text("premisePredicate", "premise predicate", 10,
                 "The premise's predicate in canonical form: Y in the lever templates "
                 "(X again for beta); for delta, Z. E.g. 'are mortal'."),
            feature("transformations", 11,
                    "The transformations that changed a subject's or predicate's wording, "
                    "each with the statement it applied to; once each, in any order. "
                    "Empty if the text needed none.",
                    visible=True, type="uima.cas.StringArray", multi_value_mode="ARRAY",
                    tag_set=tagset("PTA transformations", transformation_tags)),
            feature("concepts", 12,
                    "What the argument is about: one or more tags, each `concept` or "
                    "`concept/sense` for a writer's own sense (e.g. being, being/scotus). "
                    "Lowercase only. At least one.",
                    visible=True, type="uima.cas.StringArray", multi_value_mode="ARRAY",
                    tag_set=tagset("PTA concepts", []) | {"create_tag": True}),
            note(13, "Doubts, the label you nearly chose, or a novel lever written out. "
                     "The canonical form goes in the subject and predicate fields, not here."),
        ],
    )
    cue = layer(
        CUE, "Cue",
        "A place that might signal an argument but isn't a connector. "
        "Cues that are connectors are Connector spans. "
        "E.g. 'who could deny that' (rhetorical), 'namely' (rephrase), 'however' (conflict), "
        "'given that' introducing a stated lever (lever).",
        [
            feature("disposition", 1, "What the cue turned out to be.",
                    visible=True, tag_set=tagset("Cue dispositions", list(DISPOSITIONS.items())),
                    traits=json.dumps({"editorType": "RADIOGROUP"})),
            note(2),
        ],
    )
    return [statement, connector, cue]


def constraints() -> str:
    lines = [f"import {CONNECTOR} as Connector;", "", "Connector {"]
    for form, subs in TYPES.items():
        options = " | ".join(f'substance = "{substance_tag(form, t)}"' for t in subs)
        lines.append(f'  form = "{form}" -> {options};')
    lines.append("")
    for form, subs in TYPES.items():
        for t, entries in subs.items():
            options = [f'lever = "{kw}"' for kw, *_ in entries] + ['lever = "novel"']
            lines.append(f'  substance = "{substance_tag(form, t)}" -> {" | ".join(options)};')
    lines.append("}")
    return "\n".join(lines) + "\n"


def main() -> None:
    (OUT / "pta-layers.json").write_text(json.dumps(layers(), indent=1, ensure_ascii=False) + "\n")
    (OUT / "pta-constraints.txt").write_text(constraints())


if __name__ == "__main__":
    main()
