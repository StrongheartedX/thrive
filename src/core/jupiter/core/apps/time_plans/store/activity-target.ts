/**
 * An activity of the time plan view and what it targets, from the store.
 */
import type {
  BigPlan,
  Chore,
  ChoreStack,
  EntityLink,
  Habit,
  HabitStack,
  InboxTask,
  TimePlanActivity,
  TodoTask,
} from "@jupiter/webapi-client";

import { entityLinkRefIdFromWire } from "#/core/common/sub/inbox_tasks/parent-link-namespace";
import {
  isTimePlanActivityBigPlanTarget,
  isTimePlanActivityChoreStackTarget,
  isTimePlanActivityChoreTarget,
  isTimePlanActivityHabitStackTarget,
  isTimePlanActivityHabitTarget,
  isTimePlanActivityInboxTaskTarget,
  isTimePlanActivityTodoTaskTarget,
} from "#/core/apps/time_plans/sub/activity/target-wire";
import type {
  EntityTable,
  TimePlanEntities,
} from "#/core/apps/time_plans/store/store";

export interface ActivityWithTarget {
  timePlanActivity: TimePlanActivity;
  targetInboxTask: InboxTask | null;
  targetBigPlan: BigPlan | null;
  targetTodoTask: TodoTask | null;
  targetHabit: Habit | null;
  targetHabitStack: HabitStack | null;
  targetChore: Chore | null;
  targetChoreStack: ChoreStack | null;
  // For a habit stack, its members the store knows of - which covers every
  // member with an activity in the plan.
  habitStackMembers: Habit[];
}

export function selectActivityWithTarget(
  entities: TimePlanEntities,
  activityRefId: string,
): ActivityWithTarget | null {
  const timePlanActivity = entities.activities[activityRefId];
  if (timePlanActivity === undefined) {
    return null;
  }

  const targetRefId = entityLinkRefIdFromWire(timePlanActivity.target);
  function target<T>(
    isTarget: (target: EntityLink) => boolean,
    table: EntityTable<T>,
  ): T | null {
    return isTarget(timePlanActivity.target)
      ? (table[targetRefId] ?? null)
      : null;
  }

  const targetHabitStack = target(
    isTimePlanActivityHabitStackTarget,
    entities.habitStacks,
  );

  return {
    timePlanActivity,
    targetInboxTask: target(
      isTimePlanActivityInboxTaskTarget,
      entities.inboxTasks,
    ),
    targetBigPlan: target(isTimePlanActivityBigPlanTarget, entities.bigPlans),
    targetTodoTask: target(
      isTimePlanActivityTodoTaskTarget,
      entities.todoTasks,
    ),
    targetHabit: target(isTimePlanActivityHabitTarget, entities.habits),
    targetHabitStack,
    targetChore: target(isTimePlanActivityChoreTarget, entities.chores),
    targetChoreStack: target(
      isTimePlanActivityChoreStackTarget,
      entities.choreStacks,
    ),
    habitStackMembers:
      targetHabitStack === null
        ? []
        : Object.values(entities.habits).filter(
            (habit) => habit.stack_ref_id === targetHabitStack.ref_id,
          ),
  };
}
