/**
 * Turn the time plan routes' loader data into store snapshots.
 */
import type {
  BigPlan,
  BigPlanLoadResult,
  BigPlanStats,
  Chore,
  ChoreLoadResult,
  ChoreStack,
  ChoreStackLoadResult,
  Habit,
  HabitLoadResult,
  HabitStack,
  HabitStackLoadResult,
  InboxTask,
  TimeEventInDayBlock,
  TimePlanActivity,
  TodoTask,
  TodoTaskLoadResult,
} from "@jupiter/webapi-client";

import type { TimePlanEntitySnapshot } from "#/core/apps/time_plans/store/store";

type Maybe<T> = T | null | undefined;

function present<T>(...items: ReadonlyArray<Maybe<T>>): T[] {
  return items.filter((item): item is T => item !== null && item !== undefined);
}

/** The entities the time plan loader returns. */
export interface TimePlanLoadEntities {
  activities: ReadonlyArray<TimePlanActivity>;
  targetInboxTasks?: Maybe<ReadonlyArray<InboxTask>>;
  targetBigPlans?: Maybe<ReadonlyArray<BigPlan>>;
  bigPlanStats?: Maybe<ReadonlyArray<BigPlanStats>>;
  targetTodoTasks?: Maybe<ReadonlyArray<TodoTask>>;
  targetHabits?: Maybe<ReadonlyArray<Habit>>;
  targetHabitStacks?: Maybe<ReadonlyArray<HabitStack>>;
  targetChores?: Maybe<ReadonlyArray<Chore>>;
  targetChoreStacks?: Maybe<ReadonlyArray<ChoreStack>>;
  completedNontargetInboxTasks?: Maybe<ReadonlyArray<InboxTask>>;
  completedNontargetBigPlans?: Maybe<ReadonlyArray<BigPlan>>;
  activityTimeEventBlocks?: Maybe<ReadonlyArray<TimeEventInDayBlock>>;
}

export function snapshotFromTimePlanLoad(
  data: TimePlanLoadEntities,
): TimePlanEntitySnapshot {
  return {
    activities: data.activities,
    inboxTasks: [
      ...(data.targetInboxTasks ?? []),
      ...(data.completedNontargetInboxTasks ?? []),
    ],
    bigPlans: [
      ...(data.targetBigPlans ?? []),
      ...(data.completedNontargetBigPlans ?? []),
    ],
    bigPlanStats: data.bigPlanStats ?? [],
    todoTasks: data.targetTodoTasks ?? [],
    habits: data.targetHabits ?? [],
    habitStacks: data.targetHabitStacks ?? [],
    chores: data.targetChores ?? [],
    choreStacks: data.targetChoreStacks ?? [],
    timeEventBlocks: data.activityTimeEventBlocks ?? [],
  };
}

/** The entities the time plan activity loader returns. */
export interface TimePlanActivityLoadEntities {
  timePlanActivity: TimePlanActivity;
  targetInboxTask?: Maybe<InboxTask>;
  targetBigPlan?: Maybe<BigPlan>;
  targetBigPlanInfo?: Maybe<Pick<BigPlanLoadResult, "inbox_tasks" | "stats">>;
  targetTodoTask?: Maybe<TodoTask>;
  targetTodoTaskInfo?: Maybe<Pick<TodoTaskLoadResult, "inbox_task">>;
  targetHabit?: Maybe<Habit>;
  targetHabitInfo?: Maybe<Pick<HabitLoadResult, "inbox_tasks" | "stack">>;
  targetHabitStack?: Maybe<HabitStack>;
  targetHabitStackInfo?: Maybe<Pick<HabitStackLoadResult, "habits">>;
  targetChore?: Maybe<Chore>;
  targetChoreInfo?: Maybe<Pick<ChoreLoadResult, "inbox_tasks" | "stack">>;
  targetChoreStack?: Maybe<ChoreStack>;
  targetChoreStackInfo?: Maybe<Pick<ChoreStackLoadResult, "chores">>;
  stackInboxTasks?: Maybe<ReadonlyArray<InboxTask>>;
  choreStackInboxTasks?: Maybe<ReadonlyArray<InboxTask>>;
  allHabits?: Maybe<ReadonlyArray<Habit>>;
  allStacks?: Maybe<ReadonlyArray<HabitStack>>;
  allChores?: Maybe<ReadonlyArray<Chore>>;
  allChoreStacks?: Maybe<ReadonlyArray<ChoreStack>>;
  activityTimeEventBlocks?: Maybe<ReadonlyArray<TimeEventInDayBlock>>;
}

export function snapshotFromTimePlanActivityLoad(
  data: TimePlanActivityLoadEntities,
): TimePlanEntitySnapshot {
  return {
    activities: [data.timePlanActivity],
    inboxTasks: [
      ...present(data.targetInboxTask, data.targetTodoTaskInfo?.inbox_task),
      ...(data.targetBigPlanInfo?.inbox_tasks ?? []),
      ...(data.targetHabitInfo?.inbox_tasks ?? []),
      ...(data.targetChoreInfo?.inbox_tasks ?? []),
      ...(data.stackInboxTasks ?? []),
      ...(data.choreStackInboxTasks ?? []),
    ],
    bigPlans: present(data.targetBigPlan),
    bigPlanStats: present(data.targetBigPlanInfo?.stats),
    todoTasks: present(data.targetTodoTask),
    habits: [
      ...present(data.targetHabit),
      ...(data.targetHabitStackInfo?.habits ?? []),
      ...(data.allHabits ?? []),
    ],
    habitStacks: [
      ...present(data.targetHabitStack, data.targetHabitInfo?.stack),
      ...(data.allStacks ?? []),
    ],
    chores: [
      ...present(data.targetChore),
      ...(data.targetChoreStackInfo?.chores ?? []),
      ...(data.allChores ?? []),
    ],
    choreStacks: [
      ...present(data.targetChoreStack, data.targetChoreInfo?.stack),
      ...(data.allChoreStacks ?? []),
    ],
    timeEventBlocks: data.activityTimeEventBlocks ?? [],
  };
}
