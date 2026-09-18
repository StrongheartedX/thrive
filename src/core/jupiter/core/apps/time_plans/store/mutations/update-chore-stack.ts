/**
 * Saving a chore stack edited from the time plan view.
 *
 * The editor also picks the stack's chores, so chores can move in or out of
 * it; the update returns the ones that did.
 */
import type {
  ChoreStack,
  ChoreStackUpdateResult,
} from "@jupiter/webapi-client";
import { z } from "zod";

import type { TimePlanMutation } from "#/core/apps/time_plans/store/mutation";
import type { LifePlanAssociation } from "#/core/apps/time_plans/store/mutations/form";
import {
  editorFormFields,
  lifePlanAssociationFromForm,
  lifePlanAssociationPatch,
  lifePlanAssociationToFormFields,
  refIdsFromForm,
} from "#/core/apps/time_plans/store/mutations/form";
import { withStackMembers } from "#/core/apps/time_plans/store/mutations/stack-members";

export interface UpdateChoreStackArgs {
  refId: string;
  name: string;
  choreRefIds: string[];
  // Left alone when null.
  lifePlan: LifePlanAssociation | null;
  // When the edit was made, standing in for the server's modification time
  // until the result arrives.
  modifiedTime: string;
}

const ChoreStackPropertiesFormSchema = z.object({
  refId: z.string(),
  name: z.string(),
});

/** The args from a chore stack properties editor's form. */
export function updateChoreStackArgsFromForm(
  formData: FormData,
  modifiedTime: string,
  namePrefix: string,
): UpdateChoreStackArgs {
  const field = editorFormFields(formData, namePrefix);
  const form = ChoreStackPropertiesFormSchema.parse({
    refId: field("refId"),
    name: field("name"),
  });

  return {
    refId: form.refId,
    name: form.name,
    choreRefIds: refIdsFromForm(field("choreRefIds")),
    lifePlan: lifePlanAssociationFromForm(field),
    modifiedTime,
  };
}

export const UPDATE_CHORE_STACK: TimePlanMutation<
  UpdateChoreStackArgs,
  Pick<ChoreStackUpdateResult, "updated_chore_stack" | "updated_chores">
> = {
  action: "/app/workspace/apps/time-plans/mutations/update-chore-stack",
  toFormFields: (args) => ({
    refId: args.refId,
    name: args.name,
    choreRefIds: args.choreRefIds.join(","),
    ...lifePlanAssociationToFormFields(args.lifePlan),
  }),
  applyOptimistic: (entities, args) => {
    const choreStack = entities.choreStacks[args.refId];
    if (choreStack === undefined) {
      return entities;
    }
    const updated: ChoreStack = {
      ...choreStack,
      ...lifePlanAssociationPatch(args.lifePlan),
      name: args.name,
      last_modified_time: args.modifiedTime,
    };
    return {
      ...entities,
      choreStacks: { ...entities.choreStacks, [args.refId]: updated },
      chores: withStackMembers(
        entities.chores,
        args.refId,
        args.choreRefIds,
        args.modifiedTime,
      ),
    };
  },
  toDelta: (result) => ({
    choreStacks: [result.updated_chore_stack],
    chores: result.updated_chores,
  }),
};
