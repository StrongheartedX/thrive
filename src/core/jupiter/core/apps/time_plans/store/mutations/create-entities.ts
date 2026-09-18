/**
 * Creating todos, habits, chores, big plans and big plan inbox tasks from the
 * time plan view.
 *
 * The creation forms post what they post anywhere else; the resource routes
 * make the entity along with its activity in the plan and send both back to be
 * merged in. Nothing shows until then, since there's no ref id to show it under.
 */
import type {
  BigPlan,
  BigPlanStats,
  Chore,
  Habit,
  InboxTask,
  TimePlanActivity,
  TodoTask,
} from "@jupiter/webapi-client";

import type { TimePlanMutation } from "#/core/apps/time_plans/store/mutation";
import type { TimePlanEntityDelta } from "#/core/apps/time_plans/store/store";

export interface CreateInTimePlanArgs {
  timePlanRefId: string;
  // The creation form's fields, as it posts them.
  fields: Record<string, string>;
}

export interface CreatedInTimePlan {
  new_time_plan_activity?: TimePlanActivity | null;
}

/** A creation form's fields, without the intent that submitted it. */
export function formFieldsFromFormData(
  formData: FormData,
): Record<string, string> {
  const fields: Record<string, string> = {};
  formData.forEach((value, name) => {
    if (typeof value === "string" && name !== "intent") {
      fields[name] = value;
    }
  });
  return fields;
}

function newActivities(result: CreatedInTimePlan): Array<TimePlanActivity> {
  return result.new_time_plan_activity ? [result.new_time_plan_activity] : [];
}

function createInTimePlan<Result extends CreatedInTimePlan>(
  slug: string,
  toDelta: (result: Result) => TimePlanEntityDelta,
): TimePlanMutation<CreateInTimePlanArgs, Result> {
  return {
    action: `/app/workspace/apps/time-plans/mutations/create-${slug}`,
    toFormFields: (args) => ({
      ...args.fields,
      timePlanRefId: args.timePlanRefId,
    }),
    applyOptimistic: (entities) => entities,
    toDelta: (result) => {
      const delta = toDelta(result);
      return {
        ...delta,
        activities: [...newActivities(result), ...(delta.activities ?? [])],
      };
    },
  };
}

export const CREATE_TODO_TASK = createInTimePlan<
  CreatedInTimePlan & { new_todo_task: TodoTask; new_inbox_task: InboxTask }
>("todo-task", (result) => ({
  todoTasks: [result.new_todo_task],
  inboxTasks: [result.new_inbox_task],
}));

export const CREATE_HABIT = createInTimePlan<
  CreatedInTimePlan & { new_habit: Habit }
>("habit", (result) => ({ habits: [result.new_habit] }));

export const CREATE_CHORE = createInTimePlan<
  CreatedInTimePlan & { new_chore: Chore }
>("chore", (result) => ({ chores: [result.new_chore] }));

export const CREATE_BIG_PLAN = createInTimePlan<
  CreatedInTimePlan & { new_big_plan: BigPlan }
>("big-plan", (result) => ({ bigPlans: [result.new_big_plan] }));

// Making a big plan's inbox task in the plan also brings the big plan into it,
// if it wasn't already, and changes the big plan's stats.
export const CREATE_BIG_PLAN_INBOX_TASK = createInTimePlan<
  CreatedInTimePlan & {
    new_inbox_task: InboxTask;
    new_big_plan_time_plan_activity?: TimePlanActivity | null;
    updated_big_plan_stats?: BigPlanStats | null;
  }
>("big-plan-inbox-task", (result) => ({
  inboxTasks: [result.new_inbox_task],
  activities: result.new_big_plan_time_plan_activity
    ? [result.new_big_plan_time_plan_activity]
    : [],
  bigPlanStats: result.updated_big_plan_stats
    ? [result.updated_big_plan_stats]
    : [],
}));
