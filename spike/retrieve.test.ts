import { describe, expect, it } from 'vitest';
import { bm25, goldExamples, selectExamples } from './retrieve';

const pool = goldExamples();

describe('selectExamples', () => {
  it.each(pool)("never uses $gold.name's own writer", ({ gold, text }) => {
    const chosen = selectExamples({ text, writer: gold.writer }, pool, pool.length, Infinity);
    expect(chosen.map((e) => e.gold.writer)).not.toContain(gold.writer);
    expect(chosen).toHaveLength(pool.length - 1);
  });

  it('ranks a passage the input repeats first', () => {
    const target = pool.find((e) => e.gold.name === 'searle-chinese-room')!;
    const [first] = selectExamples({ text: target.text, writer: 'someone else' }, pool, 1, Infinity);
    expect(first.gold.name).toBe('searle-chinese-room');
  });

  it('stays within k and the token budget', () => {
    const budget = 2000;
    const chosen = selectExamples({ text: 'games and their rules', writer: 'nobody' }, pool, 2, budget);
    expect(chosen.length).toBeLessThanOrEqual(2);
    expect(chosen.reduce((n, e) => n + e.tokens, 0)).toBeLessThanOrEqual(budget);
  });
});

describe('bm25', () => {
  it('scores documents without query terms as zero', () => {
    expect(bm25('ship authority', ['the cat sat', 'authority on a ship'])).toEqual([0, expect.any(Number)]);
  });
});
