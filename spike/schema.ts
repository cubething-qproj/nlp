/**
 * The JSON schema the model's output is constrained to (llama-server's
 * `json_schema`, which it compiles to a grammar). It mirrors `notation.ts`
 * minus `note` fields: notes are for people, and every output token costs
 * time. Closed sets come from the editor's own lists. Property order is the
 * order the model writes in, so each decision comes after what it depends on
 * (a proposition's text before its terms, a relation's ends before its lever).
 *
 * Arrays are bounded a little above the gold maxima (3 `replyTo` sources, 4
 * anchors, 3 transformations, 4 concepts): unbounded, a small model can loop
 * until it runs out of tokens.
 */
import { ACCEPTABILITIES, KINDS, LEVERS, NOVEL, PERSPECTIVES, SCOPES, TRANSFORMATIONS } from 'xaif/pta';
import { FORCES, type Notation } from './notation';

const id = (prefix: string) => ({ type: 'string', pattern: `^${prefix}[0-9]+$` });
const locution = id('l');
const proposition = id('p');
const strings = { type: 'array', items: { type: 'string' } };
const upTo = (maxItems: number, items: object) => ({ type: 'array', items, maxItems });
const enumOf = (values: readonly string[]) => ({ type: 'string', enum: [...values] });

const anchorExtras = {
  force: enumOf(FORCES),
  transformations: upTo(4, enumOf(TRANSFORMATIONS)),
};
const anchor = {
  oneOf: [
    { type: 'object', properties: { locution, ...anchorExtras }, required: ['locution'], additionalProperties: false },
    { type: 'object', properties: { transitionInto: locution, ...anchorExtras }, required: ['transitionInto'], additionalProperties: false },
  ],
};

export const NOTATION_SCHEMA = {
  type: 'object',
  properties: {
    speakers: { ...strings, minItems: 1 },
    locutions: {
      type: 'array',
      minItems: 1,
      items: {
        type: 'object',
        properties: {
          id: locution,
          speaker: { type: 'string' },
          quote: { type: 'string', minLength: 1 },
          implicit: { const: true },
          reportedBy: locution,
          replyTo: upTo(4, locution),
        },
        required: ['id', 'speaker', 'quote', 'replyTo'],
        additionalProperties: false,
      },
    },
    propositions: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: proposition,
          anchors: upTo(6, anchor),
          text: { type: 'string', minLength: 1 },
          subject: { type: 'string' },
          about: proposition,
          predicate: { type: 'string' },
          kind: enumOf(KINDS),
          scope: enumOf(SCOPES),
          perspective: enumOf(PERSPECTIVES),
          acceptability: enumOf(ACCEPTABILITIES),
        },
        required: ['id', 'anchors', 'text', 'kind', 'scope'],
        additionalProperties: false,
      },
    },
    relations: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: id('r'),
          kind: enumOf(['RA', 'CA', 'MA']),
          from: proposition,
          to: { type: 'string', pattern: '^[pr][0-9]+$' },
          anchor,
          lever: enumOf([...new Set(LEVERS.map((l) => l.keyword)), NOVEL]),
          leverStatement: proposition,
          concepts: upTo(6, { type: 'string' }),
        },
        required: ['id', 'kind', 'from', 'to', 'anchor'],
        additionalProperties: false,
      },
    },
  },
  required: ['speakers', 'locutions', 'propositions', 'relations'],
  additionalProperties: false,
} as const;

/** A notation as the model would write it: without notes. */
export function withoutNotes(n: Notation): Notation {
  return {
    ...n,
    propositions: n.propositions.map(({ note, ...p }) => p),
    relations: n.relations.map(({ note, ...r }) => r),
  };
}
