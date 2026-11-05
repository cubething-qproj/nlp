/**
 * The reviewed gold maps, read from the editor's examples directory so the
 * editor and the spike share one copy. `writer` groups maps by author, for
 * leaving an input's own writer out of retrieval.
 */
import { readFileSync } from 'node:fs';
import { Doc } from 'xaif/xaif';

export interface GoldEntry {
  name: string;
  writer: string;
}

export const EXAMPLES_DIR = new URL('../../xAIF/examples/', import.meta.url);

export const GOLD: GoldEntry[] = [
  { name: 'aquinas-llm', writer: 'aquinas' },
  { name: 'aristotle-function', writer: 'aristotle' },
  { name: 'engels-alt', writer: 'engels' },
  { name: 'searle-chinese-room', writer: 'searle' },
  { name: 'suits-absurd-games', writer: 'suits' },
  { name: 'truth-woman', writer: 'truth' },
];

/** Loads one gold map as the editor would. */
export function loadGold(name: string): Doc {
  return Doc.load(JSON.parse(readFileSync(new URL(`${name}.json`, EXAMPLES_DIR), 'utf8')));
}
