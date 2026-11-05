/**
 * Notation → xAIF. Builds the nodes, edges and locution spans the notation
 * leaves out, then labels every RA with the code the editor derives from its
 * premise and conclusion. Throws an {@link ExpandError} on anything it can't
 * resolve (an unknown ID, a quote that isn't in the text), which the spike
 * counts as invalid output.
 */
import { formatCode } from 'xaif/pta';
import { argumentType, DEFAULT_TEXT, Doc } from 'xaif/xaif';
import { type Anchor, DEFAULT_FORCE, type Force, type Notation } from './notation';

export class ExpandError extends Error {}

type Json = Record<string, unknown>;

/** Expands a notation over its source text into an xAIF document. */
export function expand(notation: Notation, text: string): Json {
  const nodes: Json[] = [];
  const edges: Json[] = [];
  const locutions: Json[] = [];
  const id = new Map<string, number>();
  const taInto = new Map<string, number>();
  const node = (type: string, nodeText: string, pta?: Json) => {
    const nodeID = nodes.length + 1;
    nodes.push({ nodeID, type, text: nodeText, ...(pta && { pta }) });
    return nodeID;
  };
  const edge = (fromID: number, toID: number, role?: 'lever') =>
    edges.push({ edgeID: edges.length + 1, fromID, toID, ...(role && { role }) });
  const look = (ref: string) => id.get(ref) ?? fail(`unknown ID ${ref}`);
  const fail = (why: string): never => {
    throw new ExpandError(why);
  };

  const participants = notation.speakers.map((name, i) => {
    const [firstname, ...rest] = name.split(' ');
    return { participantID: i + 1, firstname, surname: rest.join(' ') };
  });
  const person = (name: string) =>
    participants[notation.speakers.indexOf(name)]?.participantID ?? fail(`unknown speaker ${name}`);

  // Locutions, each quote at its next unused occurrence.
  const used = new Map<string, Set<number>>();
  for (const l of notation.locutions) {
    if (id.has(l.id)) fail(`duplicate ID ${l.id}`);
    const nodeID = node('L', `${l.speaker}: ${l.quote}`);
    id.set(l.id, nodeID);
    const loc: Json = { nodeID, personID: person(l.speaker) };
    if (!l.implicit) {
      const seen = used.get(l.quote) ?? new Set<number>();
      let start = text.indexOf(l.quote);
      while (start >= 0 && seen.has(start)) start = text.indexOf(l.quote, start + 1);
      if (start < 0) fail(`${l.id}: quote not found in the text`);
      seen.add(start);
      used.set(l.quote, seen);
      Object.assign(loc, { start, end: start + l.quote.length });
    }
    locutions.push(loc);
  }
  for (const l of notation.locutions) {
    if (l.replyTo?.length) {
      const ta = node('TA', DEFAULT_TEXT.TA);
      for (const src of l.replyTo) edge(look(src), ta);
      edge(ta, look(l.id));
      taInto.set(l.id, ta);
    }
    if (l.reportedBy) ya({ locution: l.reportedBy }, 'Asserting', look(l.id));
  }

  /** Adds a YA from the anchor to `target`. */
  function ya(at: Anchor, defaultForce: Force, target: number) {
    const src = 'locution' in at ? look(at.locution) : (taInto.get(at.transitionInto) ?? fail(`no TA into ${at.transitionInto}`));
    const y = node('YA', at.force ?? defaultForce, at.transformations?.length ? { transformations: at.transformations } : undefined);
    edge(src, y);
    edge(y, target);
  }

  // Propositions and relations get IDs first, so `about`, undercuts and lever statements can point forward.
  for (const p of notation.propositions) {
    if (id.has(p.id)) fail(`duplicate ID ${p.id}`);
    id.set(p.id, node('I', p.text));
  }
  for (const r of notation.relations) {
    if (id.has(r.id)) fail(`duplicate ID ${r.id}`);
    id.set(r.id, node(r.kind, DEFAULT_TEXT[r.kind]));
  }
  for (const p of notation.propositions) {
    const n = nodes[look(p.id) - 1];
    n.pta = Object.fromEntries(
      Object.entries({
        subject: p.subject,
        subjectNode: p.about && String(look(p.about)),
        predicate: p.predicate,
        kind: p.kind,
        scope: p.scope,
        perspective: p.perspective,
        acceptability: p.acceptability,
        note: p.note,
      }).filter(([, v]) => v !== undefined),
    );
    for (const at of p.anchors) ya(at, 'Asserting', look(p.id));
  }
  for (const r of notation.relations) {
    const rid = look(r.id);
    edge(look(r.from), rid);
    edge(rid, look(r.to));
    if (r.leverStatement) edge(look(r.leverStatement), rid, 'lever');
    const pta = Object.fromEntries(Object.entries({ lever: r.lever, concepts: r.concepts, note: r.note }).filter(([, v]) => v !== undefined));
    if (Object.keys(pta).length) nodes[rid - 1].pta = pta;
    ya(r.anchor, DEFAULT_FORCE[r.kind], rid);
  }

  const json: Json = {
    AIF: { nodes, edges, locutions, participants, schemefulfillments: [], descriptorfulfillments: [] },
    text,
    dialog: true,
  };

  // RA codes are derived, never written: label each RA as the editor would.
  const doc = Doc.load(json);
  for (const r of notation.relations.filter((r) => r.kind === 'RA')) {
    const t = argumentType(String(look(r.id)), doc.nodes, doc.edges);
    nodes[look(r.id) - 1].text = t ? formatCode(t) : DEFAULT_TEXT.RA;
  }
  return json;
}
