import { describe, expect, it } from 'vitest';
import { type ArgNode, Doc, lint } from 'xaif/xaif';
import { abstract } from './abstract';
import { expand } from './expand';
import { GOLD, loadGold } from './gold';

/**
 * A description of every node and edge that ignores IDs: nodes by kind, text,
 * span and PTA data (with `subjectNode` resolved to the node it names), edges
 * by the descriptions of their ends. Two documents with equal multisets of
 * these have the same structure, up to renumbering.
 */
function shape(doc: Doc) {
  const node = new Map(doc.nodes.map((n) => [n.id, n]));
  const describe = (n: ArgNode): string => {
    const pta = { ...(n.pta as Record<string, unknown> | undefined) };
    if (typeof pta.subjectNode === 'string') pta.subjectNode = node.get(pta.subjectNode)?.text;
    const speaker = doc.participants.find((p) => p.id === n.speaker);
    return JSON.stringify([n.kind, n.text, n.span, speaker && [speaker.firstname, speaker.surname].join(' ').trim(), pta]);
  };
  return {
    nodes: doc.nodes.map(describe).sort(),
    edges: doc.edges.map((e) => JSON.stringify([describe(node.get(e.from)!), describe(node.get(e.to)!), e.role])).sort(),
  };
}

describe.each(GOLD)('round trip $name', ({ name }) => {
  const gold = loadGold(name);
  const notation = abstract(gold);
  const doc = Doc.load(expand(notation, gold.text));

  it('lints clean', () => {
    expect(lint(doc.nodes, doc.edges, doc.text)).toEqual([]);
  });

  it('reproduces the gold structure, including RA codes', () => {
    expect(shape(doc)).toEqual(shape(gold));
  });

  it('reads back to the same notation', () => {
    expect(abstract(doc)).toEqual(notation);
  });
});
