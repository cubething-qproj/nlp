/**
 * The compact notation the model writes instead of raw xAIF.
 *
 * It holds only the decisions: what was said and by whom, what each locution
 * asserts, and how propositions relate. The expander (`expand.ts`) builds the
 * xAIF from it: numeric IDs, YA/TA nodes and edges, character offsets found by
 * searching the input for each quote, and every RA's code, which is derived
 * by the editor's rules and never written by the model.
 *
 * IDs are short strings local to one notation: `l1…` for locutions, `p1…` for
 * propositions, `r1…` for relations. A relation can target another relation
 * (an undercut), so relation IDs share a namespace with propositions.
 */
import type { Acceptability, Perspective, Scope, StatementKind, TRANSFORMATIONS } from 'xaif/pta';

export type Transformation = (typeof TRANSFORMATIONS)[number];

/** Illocutionary forces the gold set uses, plus the editor's other questioning forces. */
export const FORCES = [
  'Asserting',
  'Agreeing',
  'Disagreeing',
  'Restating',
  'Arguing',
  'Rhetorical Questioning',
  'Pure Questioning',
  'Assertive Questioning',
  'Challenging',
] as const;
export type Force = (typeof FORCES)[number];

export interface Notation {
  /** Speakers as IAT prefixes locutions: `Forename Surname`. */
  speakers: string[];
  locutions: Locution[];
  propositions: Proposition[];
  relations: Relation[];
}

export interface Locution {
  id: string;
  /** One of `speakers`. */
  speaker: string;
  /**
   * The exact words, copied from the input. The expander finds them by
   * search; a repeated quote takes the next occurrence not already used.
   */
  quote: string;
  /** Words attributed to the speaker but not in the input (no span). */
  implicit?: true;
  /** The locution that reports these words, which anchors them by Asserting. */
  reportedBy?: string;
  /**
   * Locutions this one responds to: the inputs of its incoming TA. Required,
   * so the model decides it for every locution; empty for none.
   */
  replyTo: string[];
}

/** Where a YA hangs: a locution, or the TA into a locution. */
export type Anchor = ({ locution: string } | { transitionInto: string }) & {
  /** Default: Asserting for propositions; Arguing, Disagreeing or Restating for relations. */
  force?: Force;
  /** ATIP step-2 changes from the locution's wording to the proposition. */
  transformations?: Transformation[];
};

export interface Proposition {
  id: string;
  /** The canonical proposition as a sentence. */
  text: string;
  /** Empty for an implicit proposition. */
  anchors: Anchor[];
  subject?: string;
  /** For a second-order statement: the proposition it is about (`p…`), instead of `subject`. */
  about?: string;
  /** Omitted when `acceptability` replaces it. */
  predicate?: string;
  kind: StatementKind;
  scope: Scope;
  /** Second-order statements: the source's perspective (δ substance). */
  perspective?: Perspective;
  /** Second-order statements: the predicate is [is acceptable] / [is unacceptable]. */
  acceptability?: Acceptability;
  note?: string;
}

export interface Relation {
  id: string;
  /** RA support, CA conflict, MA rephrase. */
  kind: 'RA' | 'CA' | 'MA';
  /** The premise, conflicting or rephrased proposition. */
  from: string;
  /** A proposition, or a relation for an undercut. */
  to: string;
  /** RA only: the lever keyword, e.g. `CRITERION`. */
  lever?: string;
  /** RA only: a proposition stating the lever. */
  leverStatement?: string;
  /** RA only: lowercase concept tags. */
  concepts?: string[];
  anchor: Anchor;
  note?: string;
}

/** The force a relation's anchor has unless the notation says otherwise. */
export const DEFAULT_FORCE: Record<Relation['kind'], Force> = { RA: 'Arguing', CA: 'Disagreeing', MA: 'Restating' };
