import type { EntityLink } from "@jupiter/webapi-client";

/** ``EntityLink`` wire form for a time-plan activity aimed at a todo task. */
const TODO_TASK_STD_PREFIX = "TodoTask:std:";

/** ``EntityLink`` wire form for a time-plan activity aimed at an inbox task. */
const INBOX_TASK_STD_PREFIX = "InboxTask:std:";

/** ``EntityLink`` wire form for a time-plan activity aimed at a big plan. */
const BIG_PLAN_STD_PREFIX = "BigPlan:std:";

/** ``EntityLink`` wire form for a time-plan activity aimed at a habit. */
const HABIT_STD_PREFIX = "Habit:std:";

/** ``EntityLink`` wire form for a time-plan activity aimed at a habit stack. */
const HABIT_STACK_STD_PREFIX = "HabitStack:std:";

/** ``EntityLink`` wire form for a time-plan activity aimed at a chore stack. */
const CHORE_STACK_STD_PREFIX = "ChoreStack:std:";

/** ``EntityLink`` wire form for a time-plan activity aimed at a chore. */
const CHORE_STD_PREFIX = "Chore:std:";

export function isTimePlanActivityTodoTaskTarget(target: EntityLink): boolean {
  return target.startsWith(TODO_TASK_STD_PREFIX);
}

export function isTimePlanActivityInboxTaskTarget(target: EntityLink): boolean {
  return target.startsWith(INBOX_TASK_STD_PREFIX);
}

export function isTimePlanActivityBigPlanTarget(target: EntityLink): boolean {
  return target.startsWith(BIG_PLAN_STD_PREFIX);
}

export function isTimePlanActivityHabitTarget(target: EntityLink): boolean {
  return target.startsWith(HABIT_STD_PREFIX);
}

export function isTimePlanActivityHabitStackTarget(
  target: EntityLink,
): boolean {
  return target.startsWith(HABIT_STACK_STD_PREFIX);
}

export function isTimePlanActivityChoreStackTarget(
  target: EntityLink,
): boolean {
  return target.startsWith(CHORE_STACK_STD_PREFIX);
}

export function isTimePlanActivityChoreTarget(target: EntityLink): boolean {
  return target.startsWith(CHORE_STD_PREFIX);
}

/** Sort key: todo tasks, habit stacks, habits, chore stacks, chores, big plans, then inbox tasks. */
export function timePlanActivityTargetSortOrder(target: EntityLink): number {
  if (isTimePlanActivityTodoTaskTarget(target)) {
    return 0;
  }
  if (isTimePlanActivityHabitStackTarget(target)) {
    return 1;
  }
  if (isTimePlanActivityHabitTarget(target)) {
    return 2;
  }
  if (isTimePlanActivityChoreStackTarget(target)) {
    return 3;
  }
  if (isTimePlanActivityChoreTarget(target)) {
    return 4;
  }
  if (isTimePlanActivityBigPlanTarget(target)) {
    return 5;
  }
  if (isTimePlanActivityInboxTaskTarget(target)) {
    return 6;
  }
  return 7;
}
