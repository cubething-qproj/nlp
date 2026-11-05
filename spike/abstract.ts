/**
 * xAIF → notation: the inverse of `expand.ts`. Used to turn gold maps into
 * few-shot examples and to test that the notation loses nothing. Throws on
 * structure the notation can't express, so gaps surface in the round trip.
 */
import type { Analysis, Connector, Reconstruction } from 'xaif/pta';
import { type ArgNode, DEFAULT_TEXT, type Doc, nameOf } from 'xaif/xaif';
import { type Anchor, DEFAULT_FORCE, type Force, type Locution, type Notation, type Proposition, type Relation } from './notation';

/** Reads a loaded xAIF document as notation, numbering IDs in reading order. */
export function abstract(doc: Doc): Notation {
  const node = new Map(doc.nodes.map((n) => [n.id, n]));
  const kind = (id: string) => node.get(id)?.kind;
  const into = (id: string) => doc.edges.filter((e) => e.to === id);
  const outOf = (id: string) => doc.edges.filter((e) => e.from === id);
  const fail = (n: ArgNode, why: string): never => {
    throw new Error(`${n.kind} ${n.id}: ${why}`);
  };

  // Locutions in text order; implicit ones (no span) last, in file order.
  const locutions = doc.nodes
    .filter((n) => n.kind === 'L')
    .map((n, i) => ({ n, i }))
    .sort((a, b) => (a.n.span?.start ?? Infinity) - (b.n.span?.start ?? Infinity) || a.i - b.i)
    .map(({ n }) => n);
  const props = doc.nodes.filter((n) => n.kind === 'I');
  const rels = doc.nodes.filter((n) => n.kind === 'RA' || n.kind === 'CA' || n.kind === 'MA');
  const short = new Map<string, string>([
    ...locutions.map((n, i) => [n.id, `l${i + 1}`] as const),
    ...props.map((n, i) => [n.id, `p${i + 1}`] as const),
    ...rels.map((n, i) => [n.id, `r${i + 1}`] as const),
  ]);
  const ref = (id: string) => short.get(id) ?? fail(node.get(id)!, 'is not a locution, proposition or relation');
  const speaker = (n: ArgNode) => {
    const p = doc.participants.find((p) => p.id === n.speaker);
    return p ? nameOf(p) : fail(n, 'has no speaker');
  };

  /** The YA's source as an anchor, with its force unless it is the default. */
  const anchorOf = (ya: ArgNode, defaultForce: Force): Anchor => {
    const sources = into(ya.id);
    if (sources.length !== 1) fail(ya, `has ${sources.length} sources`);
    const src = node.get(sources[0].from)!;
    let at: Anchor;
    if (src.kind === 'L') at = { locution: ref(src.id) };
    else if (src.kind === 'TA') {
      const target = outOf(src.id).find((e) => kind(e.to) === 'L') ?? fail(src, 'leads to no locution');
      at = { transitionInto: ref(target.to) };
    } else return fail(ya, `is anchored in a ${src.kind}`);
    if (ya.text !== defaultForce) at.force = ya.text as Force;
    const tx = (ya.pta as Reconstruction | undefined)?.transformations;
    if (tx?.length) at.transformations = tx as Anchor['transformations'];
    return at;
  };
  const yasInto = (id: string) => into(id).filter((e) => kind(e.from) === 'YA').map((e) => node.get(e.from)!);

  const notationLocutions = locutions.map((n): Locution => {
    const l: Locution = { id: ref(n.id), speaker: speaker(n), quote: n.text, replyTo: [] };
    if (!n.span) l.implicit = true;
    const reporters = yasInto(n.id);
    if (reporters.length > 1) fail(n, 'is reported more than once');
    for (const ya of reporters) {
      if (ya.text !== 'Asserting') fail(ya, `reports by ${ya.text}`);
      const src = into(ya.id).map((e) => node.get(e.from)!);
      if (src.length !== 1 || src[0].kind !== 'L') fail(ya, 'is not anchored in one locution');
      l.reportedBy = ref(src[0].id);
    }
    const ta = into(n.id).filter((e) => kind(e.from) === 'TA');
    if (ta.length === 1) l.replyTo = into(ta[0].from).map((e) => ref(e.from));
    return l;
  });

  const propositions = props.map((n): Proposition => {
    const a = (n.pta ?? {}) as Analysis;
    if (!a.kind || !a.scope) fail(n, 'has no statement type or scope');
    const p: Proposition = {
      id: ref(n.id),
      text: n.text,
      anchors: yasInto(n.id).map((ya) => anchorOf(ya, 'Asserting')),
      kind: a.kind!,
      scope: a.scope!,
    };
    if (a.subject) p.subject = a.subject;
    if (a.subjectNode) p.about = ref(a.subjectNode);
    if (a.predicate) p.predicate = a.predicate;
    if (a.perspective) p.perspective = a.perspective;
    if (a.acceptability) p.acceptability = a.acceptability;
    if (a.note) p.note = a.note;
    return p;
  });

  const relations = rels.map((n): Relation => {
    const k = n.kind as Relation['kind'];
    if (k !== 'RA' && n.text !== DEFAULT_TEXT[k]) fail(n, `uses scheme ${n.text}`);
    // Inputs are propositions; a CA arriving here is an undercut, recorded on the CA.
    const ins = into(n.id).filter((e) => kind(e.from) === 'I');
    const premises = ins.filter((e) => e.role !== 'lever');
    const levers = ins.filter((e) => e.role === 'lever');
    const outs = outOf(n.id);
    const anchors = yasInto(n.id);
    if (premises.length !== 1 || outs.length !== 1 || anchors.length !== 1 || levers.length > 1)
      fail(n, `has ${premises.length} inputs, ${outs.length} outputs, ${anchors.length} anchors`);
    const r: Relation = { id: ref(n.id), kind: k, from: ref(premises[0].from), to: ref(outs[0].to), anchor: anchorOf(anchors[0], DEFAULT_FORCE[k]) };
    const c = (n.pta ?? {}) as Connector;
    if (c.lever) r.lever = c.lever;
    if (levers.length) r.leverStatement = ref(levers[0].from);
    if (c.concepts?.length) r.concepts = c.concepts;
    if (c.note) r.note = c.note;
    return r;
  });

  return { speakers: doc.participants.map(nameOf), locutions: notationLocutions, propositions, relations };
}
