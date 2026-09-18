/**
 * Changing a time plan activity's kind and feasability.
 */
import type {
  TimePlanActivity,
  TimePlanActivityUpdateResult,
} from "@jupiter/webapi-client";
import {
  TimePlanActivityFeasability,
  TimePlanActivityKind,
} from "@jupiter/webapi-client";
import { z } from "zod";

import type { TimePlanMutation } from "#/core/apps/time_plans/store/mutation";

export interface UpdateTimePlanActivityArgs {
  refId: string;
  kind: TimePlanActivityKind;
  feasability: TimePlanActivityFeasability;
}

const UpdateTimePlanActivityFormSchema = z.object({
  kind: z.nativeEnum(TimePlanActivityKind),
  feasability: z.nativeEnum(TimePlanActivityFeasability),
});

/** The args from the activity panel's properties form. */
export function updateTimePlanActivityArgsFromForm(
  refId: string,
  formData: FormData,
): UpdateTimePlanActivityArgs {
  const { kind, feasability } = UpdateTimePlanActivityFormSchema.parse({
    kind: formData.get("kind"),
    feasability: formData.get("feasability"),
  });
  return { refId, kind, feasability };
}

export const UPDATE_TIME_PLAN_ACTIVITY: TimePlanMutation<
  UpdateTimePlanActivityArgs,
  Pick<TimePlanActivityUpdateResult, "updated_time_plan_activity">
> = {
  action: "/app/workspace/apps/time-plans/mutations/update-activity",
  toFormFields: (args) => ({
    refId: args.refId,
    kind: args.kind,
    feasability: args.feasability,
  }),
  applyOptimistic: (entities, args) => {
    const activity = entities.activities[args.refId];
    if (activity === undefined) {
      return entities;
    }
    const updated: TimePlanActivity = {
      ...activity,
      kind: args.kind,
      feasability: args.feasability,
    };
    return {
      ...entities,
      activities: { ...entities.activities, [args.refId]: updated },
    };
  },
  toDelta: (result) => ({
    activities: [result.updated_time_plan_activity],
  }),
};
