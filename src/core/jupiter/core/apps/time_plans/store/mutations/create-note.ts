/**
 * Creating a note for one of a time plan activity's targets.
 *
 * Notes aren't part of the store; the panel keeps the note the route returns
 * and shows its editor right away.
 */
import type { NamedEntityTag, NoteCreateResult } from "@jupiter/webapi-client";

import type { TimePlanMutation } from "#/core/apps/time_plans/store/mutation";

export interface CreateNoteArgs {
  ownerTag: NamedEntityTag;
  ownerRefId: string;
}

export const CREATE_NOTE: TimePlanMutation<
  CreateNoteArgs,
  Pick<NoteCreateResult, "new_note">
> = {
  action: "/app/workspace/apps/time-plans/mutations/create-note",
  toFormFields: (args) => ({
    ownerTag: args.ownerTag,
    ownerRefId: args.ownerRefId,
  }),
  applyOptimistic: (entities) => entities,
  toDelta: () => ({}),
};

/** How the panel keys the notes it created, by owner. */
export function createdNoteKey(
  ownerTag: NamedEntityTag,
  ownerRefId: string,
): string {
  return `${ownerTag}:${ownerRefId}`;
}
