/**
 * Saving a habit stack edited from the time plan view.
 *
 * The editor also picks the stack's habits, so habits can move in or out of
 * it; the update returns the ones that did.
 */
import type {
  HabitStack,
  HabitStackUpdateResult,
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

export interface UpdateHabitStackArgs {
  refId: string;
  name: string;
  habitRefIds: string[];
  // Left alone when null.
  lifePlan: LifePlanAssociation | null;
  // When the edit was made, standing in for the server's modification time
  // until the result arrives.
  modifiedTime: string;
}

const HabitStackPropertiesFormSchema = z.object({
  refId: z.string(),
  name: z.string(),
});

/** The args from a habit stack properties editor's form. */
export function updateHabitStackArgsFromForm(
  formData: FormData,
  modifiedTime: string,
  namePrefix: string,
): UpdateHabitStackArgs {
  const field = editorFormFields(formData, namePrefix);
  const form = HabitStackPropertiesFormSchema.parse({
    refId: field("refId"),
    name: field("name"),
  });

  return {
    refId: form.refId,
    name: form.name,
    habitRefIds: refIdsFromForm(field("habitRefIds")),
    lifePlan: lifePlanAssociationFromForm(field),
    modifiedTime,
  };
}

export const UPDATE_HABIT_STACK: TimePlanMutation<
  UpdateHabitStackArgs,
  Pick<HabitStackUpdateResult, "updated_habit_stack" | "updated_habits">
> = {
  action: "/app/workspace/apps/time-plans/mutations/update-habit-stack",
  toFormFields: (args) => ({
    refId: args.refId,
    name: args.name,
    habitRefIds: args.habitRefIds.join(","),
    ...lifePlanAssociationToFormFields(args.lifePlan),
  }),
  applyOptimistic: (entities, args) => {
    const habitStack = entities.habitStacks[args.refId];
    if (habitStack === undefined) {
      return entities;
    }
    const updated: HabitStack = {
      ...habitStack,
      ...lifePlanAssociationPatch(args.lifePlan),
      name: args.name,
      last_modified_time: args.modifiedTime,
    };
    return {
      ...entities,
      habitStacks: { ...entities.habitStacks, [args.refId]: updated },
      habits: withStackMembers(
        entities.habits,
        args.refId,
        args.habitRefIds,
        args.modifiedTime,
      ),
    };
  },
  toDelta: (result) => ({
    habitStacks: [result.updated_habit_stack],
    habits: result.updated_habits,
  }),
};
