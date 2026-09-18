/**
 * Moving habits or chores in and out of a stack locally.
 */

interface Stackable {
  ref_id: string;
  stack_ref_id?: string | null;
  last_modified_time: string;
}

/**
 * ``table`` with exactly ``memberRefIds`` in the stack ``stackRefId``.
 *
 * Members that were elsewhere move into the stack, and ones that are no longer
 * listed leave it. Entities whose membership doesn't change are kept as they
 * are.
 */
export function withStackMembers<T extends Stackable>(
  table: Readonly<Record<string, T>>,
  stackRefId: string,
  memberRefIds: ReadonlyArray<string>,
  modifiedTime: string,
): Record<string, T> {
  const members = new Set(memberRefIds);
  const updated: Record<string, T> = { ...table };
  for (const entity of Object.values(table)) {
    const inStack = entity.stack_ref_id === stackRefId;
    if (members.has(entity.ref_id) && !inStack) {
      updated[entity.ref_id] = {
        ...entity,
        stack_ref_id: stackRefId,
        last_modified_time: modifiedTime,
      };
    } else if (!members.has(entity.ref_id) && inStack) {
      updated[entity.ref_id] = {
        ...entity,
        stack_ref_id: null,
        last_modified_time: modifiedTime,
      };
    }
  }
  return updated;
}
