/**
 * Few-shot example selection: rank gold maps by BM25 similarity of their
 * passage to the input, never using the input's own writer, and take the best
 * that fit a token budget. A chunk is a whole gold map: gold passages are the
 * size of passage-mode inputs, and cutting a map would break RAs that cross
 * the cut. Player-line inputs will need smaller chunks.
 */
import { abstract } from './abstract';
import { GOLD, type GoldEntry, loadGold } from './gold';
import type { Notation } from './notation';
import { withoutNotes } from './schema';

export interface Example {
  gold: GoldEntry;
  speakers: string[];
  text: string;
  notation: Notation;
  /** Rough prompt cost of passage plus notation, at four characters a token. */
  tokens: number;
}

const STOPWORDS = new Set(
  'a an and are as at be but by for from has have he i in is it its not of on or that the their there this to was we which with you'.split(' '),
);

function terms(text: string): string[] {
  return (text.toLowerCase().match(/\p{L}+/gu) ?? []).filter((t) => !STOPWORDS.has(t));
}

/** Okapi BM25 scores of each document against the query (k1 = 1.2, b = 0.75). */
export function bm25(query: string, docs: string[], k1 = 1.2, b = 0.75): number[] {
  const tokenized = docs.map(terms);
  const avg = tokenized.reduce((n, d) => n + d.length, 0) / Math.max(tokenized.length, 1);
  const df = new Map<string, number>();
  for (const d of tokenized) for (const t of new Set(d)) df.set(t, (df.get(t) ?? 0) + 1);
  const q = new Set(terms(query));
  return tokenized.map((d) => {
    const tf = new Map<string, number>();
    for (const t of d) tf.set(t, (tf.get(t) ?? 0) + 1);
    let score = 0;
    for (const t of q) {
      const f = tf.get(t);
      if (!f) continue;
      const n = df.get(t) ?? 0;
      const idf = Math.log(1 + (docs.length - n + 0.5) / (n + 0.5));
      score += (idf * f * (k1 + 1)) / (f + k1 * (1 - b + (b * d.length) / avg));
    }
    return score;
  });
}

/** Loads every gold map as an example, notes removed. */
export function goldExamples(): Example[] {
  return GOLD.map((gold) => {
    const doc = loadGold(gold.name);
    const notation = withoutNotes(abstract(doc));
    const tokens = Math.ceil((doc.text.length + JSON.stringify(notation).length) / 4);
    return { gold, speakers: notation.speakers, text: doc.text, notation, tokens };
  });
}

/**
 * The examples for an input: other writers' maps, most similar first, at most
 * `k` of them, skipping any that would take the total over `budget` tokens.
 */
export function selectExamples(input: { text: string; writer: string }, pool: Example[], k: number, budget: number): Example[] {
  const candidates = pool.filter((e) => e.gold.writer !== input.writer);
  const scores = bm25(input.text, candidates.map((e) => e.text));
  const ranked = candidates.map((e, i) => ({ e, s: scores[i] })).sort((a, b) => b.s - a.s);
  const chosen: Example[] = [];
  let used = 0;
  for (const { e } of ranked) {
    if (chosen.length === k) break;
    if (used + e.tokens > budget) continue;
    chosen.push(e);
    used += e.tokens;
  }
  return chosen;
}
