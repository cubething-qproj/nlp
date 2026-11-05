import { Ajv } from 'ajv';
import { describe, expect, it } from 'vitest';
import { abstract } from './abstract';
import { GOLD, loadGold } from './gold';
import { NOTATION_SCHEMA, withoutNotes } from './schema';

const validate = new Ajv({ allErrors: true }).compile(NOTATION_SCHEMA);

describe('notation schema', () => {
  // If gold doesn't fit the grammar, the model can't write what gold says.
  it.each(GOLD)('accepts gold $name', ({ name }) => {
    expect(validate(withoutNotes(abstract(loadGold(name)))), JSON.stringify(validate.errors)).toBe(true);
  });

  it('rejects a hand-written RA code', () => {
    const n = withoutNotes(abstract(loadGold('suits-absurd-games')));
    const ra = { ...n.relations[0], code: 'α VF Cr' };
    expect(validate({ ...n, relations: [ra] })).toBe(false);
  });
});
