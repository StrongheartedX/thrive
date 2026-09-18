/**
 * Archiving or removing a time plan activity from the time plan view.
 *
 * Both take other activities with them - a big plan's inbox task activities,
 * a stack's member activities - which the server works out and returns.
 */
import type {
  TimePlanActivity,
  TimePlanActivityArchiveResult,
  TimePlanActivityRemoveResult,
} from "@jupiter/webapi-client";

import type { TimePlanMutation } from "#/core/apps/time_plans/store/mutation";

export interface ArchiveTimePlanActivityArgs {
  refId: string;
  // When the edit was made, standing in for the server's archival time until
  // the result arrives.
  modifiedTime: string;
}

export const ARCHIVE_TIME_PLAN_ACTIVITY: TimePlanMutation<
  ArchiveTimePlanActivityArgs,
  Pick<TimePlanActivityArchiveResult, "archived_time_plan_activities">
> = {
  action: "/app/workspace/apps/time-plans/mutations/archive-activity",
  toFormFields: (args) => ({ refId: args.refId }),
  applyOptimistic: (entities, args) => {
    const activity = entities.activities[args.refId];
    if (activity === undefined) {
      return entities;
    }
    const updated: TimePlanActivity = {
      ...activity,
      archived: true,
      archived_time: args.modifiedTime,
      last_modified_time: args.modifiedTime,
    };
    return {
      ...entities,
      activities: { ...entities.activities, [args.refId]: updated },
    };
  },
  toDelta: (result) => ({
    activities: result.archived_time_plan_activities,
  }),
};

export interface RemoveTimePlanActivityArgs {
  refId: string;
}

export const REMOVE_TIME_PLAN_ACTIVITY: TimePlanMutation<
  RemoveTimePlanActivityArgs,
  Pick<TimePlanActivityRemoveResult, "removed_time_plan_activity_ref_ids">
> = {
  action: "/app/workspace/apps/time-plans/mutations/remove-activity",
  toFormFields: (args) => ({ refId: args.refId }),
  applyOptimistic: (entities, args) => {
    if (entities.activities[args.refId] === undefined) {
      return entities;
    }
    const activities = { ...entities.activities };
    delete activities[args.refId];
    return { ...entities, activities };
  },
  toDelta: (result) => ({
    removed: { activities: result.removed_time_plan_activity_ref_ids },
  }),
};
