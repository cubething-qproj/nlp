import { describe, expect, it } from 'vitest';
import { argumentType, lint } from 'xaif/xaif';
import { GOLD, loadGold } from './gold';

// Gold is the reference the spike is scored against: it must stay valid in the editor.
describe.each(GOLD)('gold $name', ({ name }) => {
  const doc = loadGold(name);

  it('lints clean', () => {
    expect(lint(doc.nodes, doc.edges, doc.text)).toEqual([]);
  });

  it('labels every RA with the code the editor derives', () => {
    for (const n of doc.nodes.filter((n) => n.kind === 'RA')) {
      const t = argumentType(n.id, doc.nodes, doc.edges);
      expect(t && `${t.form} ${t.substance} ${t.symbol}`, `RA ${n.id}`).toBe(n.text);
    }
  });
});
