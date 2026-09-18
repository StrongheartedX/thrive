/**
 * Compute time-plan activity doneness from returned entities.
 *
 * Keep in sync with ``compute_doneness.py``. Doneness is a pure function of the
 * plan window and the state of activities, inbox tasks, big plans, habits,
 * chores, and stacks.
 */
import type {
  BigPlan,
  Chore,
  ChoreStack,
  Habit,
  HabitStack,
  InboxTask,
  TimePlan,
  TimePlanActivity,
} from "@jupiter/webapi-client";
import {
  TimePlanActivityDoneness,
  TimePlanActivityKind,
} from "@jupiter/webapi-client";
import { DateTime } from "luxon";

import {
  isCompleted as bigPlanIsCompleted,
  isWorkingOrMore as bigPlanIsWorkingOrMore,
} from "#/core/apps/big_plans/status";
import {
  isTimePlanActivityBigPlanTarget,
  isTimePlanActivityChoreStackTarget,
  isTimePlanActivityChoreTarget,
  isTimePlanActivityHabitStackTarget,
  isTimePlanActivityHabitTarget,
  isTimePlanActivityInboxTaskTarget,
  isTimePlanActivityTodoTaskTarget,
} from "#/core/apps/time_plans/sub/activity/target-wire";
import {
  BIG_PLAN,
  CHORE,
  HABIT,
  TODO_TASK,
  entityLinkRefIdFromWire,
  parentLinkNamespaceFromEntityLinkWire,
} from "#/core/common/sub/inbox_tasks/parent-link-namespace";
import {
  isCompleted as inboxTaskIsCompleted,
  isWorking as inboxTaskIsWorking,
  isWorkingOrMore as inboxTaskIsWorkingOrMore,
} from "#/core/common/sub/inbox_tasks/status";

const INBOX_MAKE_PROGRESS_EXTRA_DAYS = 30;
const BIG_PLAN_MAKE_PROGRESS_EXTRA_DAYS = 60;

export interface ComputeActivityDonenessArgs {
  timePlan: Pick<TimePlan, "start_date" | "end_date">;
  activities: ReadonlyArray<
    Pick<TimePlanActivity, "ref_id" | "kind" | "target">
  >;
  inboxTasks: ReadonlyArray<
    Pick<InboxTask, "ref_id" | "status" | "last_modified_time" | "owner">
  >;
  bigPlans?: ReadonlyArray<
    Pick<BigPlan, "ref_id" | "status" | "last_modified_time">
  > | null;
  habits?: ReadonlyArray<Pick<Habit, "ref_id" | "stack_ref_id">> | null;
  habitStacks?: ReadonlyArray<Pick<HabitStack, "ref_id">> | null;
  chores?: ReadonlyArray<Pick<Chore, "ref_id" | "stack_ref_id">> | null;
  choreStacks?: ReadonlyArray<Pick<ChoreStack, "ref_id">> | null;
}

export function computeActivityDoneness(
  args: ComputeActivityDonenessArgs,
): Record<string, TimePlanActivityDoneness> {
  const activityDoneness: Record<string, TimePlanActivityDoneness> = {};
  const activities = args.activities;

  const inboxTasksByRefId = new Map(
    args.inboxTasks.map((inboxTask) => [inboxTask.ref_id, inboxTask]),
  );
  const todoOwnedInboxTasksByTodoRefId = new Map<
    string,
    (typeof args.inboxTasks)[number]
  >();
  for (const inboxTask of args.inboxTasks) {
    if (parentLinkNamespaceFromEntityLinkWire(inboxTask.owner) === TODO_TASK) {
      todoOwnedInboxTasksByTodoRefId.set(
        entityLinkRefIdFromWire(inboxTask.owner),
        inboxTask,
      );
    }
  }

  const bigPlansByRefId = new Map(
    (args.bigPlans ?? []).map((bigPlan) => [bigPlan.ref_id, bigPlan]),
  );
  const habitsByRefId = new Map(
    (args.habits ?? []).map((habit) => [habit.ref_id, habit]),
  );
  const habitStacksByRefId = new Map(
    (args.habitStacks ?? []).map((stack) => [stack.ref_id, stack]),
  );
  const choresByRefId = new Map(
    (args.chores ?? []).map((chore) => [chore.ref_id, chore]),
  );
  const choreStacksByRefId = new Map(
    (args.choreStacks ?? []).map((stack) => [stack.ref_id, stack]),
  );

  const activitiesByBigPlanRefId = new Map<string, string[]>();
  const activitiesByHabitRefId = new Map<string, string[]>();
  const activitiesByChoreRefId = new Map<string, string[]>();

  for (const activity of activities) {
    let resolvedInboxTask: (typeof args.inboxTasks)[number] | undefined =
      undefined;
    if (isTimePlanActivityInboxTaskTarget(activity.target)) {
      resolvedInboxTask = inboxTasksByRefId.get(
        entityLinkRefIdFromWire(activity.target),
      );
    } else if (isTimePlanActivityTodoTaskTarget(activity.target)) {
      resolvedInboxTask = todoOwnedInboxTasksByTodoRefId.get(
        entityLinkRefIdFromWire(activity.target),
      );
    }

    if (resolvedInboxTask === undefined) {
      continue;
    }

    const inboxDoneness = inboxTaskDoneness(
      args.timePlan,
      activity.kind,
      resolvedInboxTask,
    );
    activityDoneness[activity.ref_id] = inboxDoneness;

    const ownerNamespace = parentLinkNamespaceFromEntityLinkWire(
      resolvedInboxTask.owner,
    );
    const ownerRefId = entityLinkRefIdFromWire(resolvedInboxTask.owner);
    if (ownerNamespace === BIG_PLAN) {
      appendIndexed(activitiesByBigPlanRefId, ownerRefId, activity.ref_id);
    } else if (ownerNamespace === HABIT) {
      appendIndexed(activitiesByHabitRefId, ownerRefId, activity.ref_id);
    } else if (ownerNamespace === CHORE) {
      appendIndexed(activitiesByChoreRefId, ownerRefId, activity.ref_id);
    }
  }

  for (const activity of activities) {
    if (!isTimePlanActivityBigPlanTarget(activity.target)) {
      continue;
    }

    const targetRefId = entityLinkRefIdFromWire(activity.target);
    const bigPlan = bigPlansByRefId.get(targetRefId);
    if (bigPlan === undefined) {
      activityDoneness[activity.ref_id] = TimePlanActivityDoneness.DONE;
      continue;
    }

    const { someWorkingOrDone, allDone } = subactivityFlags(
      activityDoneness,
      activitiesByBigPlanRefId.get(bigPlan.ref_id) ?? [],
    );
    const bigPlanDonenessValue = bigPlanDoneness(
      args.timePlan,
      activity.kind,
      bigPlan,
      someWorkingOrDone,
      allDone,
    );
    activityDoneness[activity.ref_id] = bigPlanDonenessValue;
  }

  for (const activity of activities) {
    if (!isTimePlanActivityHabitTarget(activity.target)) {
      continue;
    }

    const targetRefId = entityLinkRefIdFromWire(activity.target);
    if (!habitsByRefId.has(targetRefId)) {
      activityDoneness[activity.ref_id] = TimePlanActivityDoneness.DONE;
      continue;
    }

    const { someWorkingOrDone, allDone, majorityDone } = subactivityFlags(
      activityDoneness,
      activitiesByHabitRefId.get(targetRefId) ?? [],
    );
    activityDoneness[activity.ref_id] = donenessFromSubRollUp(
      activity.kind,
      someWorkingOrDone,
      allDone,
      majorityDone,
    );
  }

  for (const activity of activities) {
    if (!isTimePlanActivityHabitStackTarget(activity.target)) {
      continue;
    }

    const stackRefId = entityLinkRefIdFromWire(activity.target);
    if (!habitStacksByRefId.has(stackRefId)) {
      activityDoneness[activity.ref_id] = TimePlanActivityDoneness.DONE;
      continue;
    }

    const memberHabitActivityRefIds = memberStackActivityRefIds(
      activities,
      habitsByRefId,
      stackRefId,
      isTimePlanActivityHabitTarget,
    );
    const { someWorkingOrDone, allDone, majorityDone } = subactivityFlags(
      activityDoneness,
      memberHabitActivityRefIds,
    );
    activityDoneness[activity.ref_id] = donenessFromSubRollUp(
      activity.kind,
      someWorkingOrDone,
      allDone,
      majorityDone,
    );
  }

  for (const activity of activities) {
    if (!isTimePlanActivityChoreTarget(activity.target)) {
      continue;
    }

    const targetRefId = entityLinkRefIdFromWire(activity.target);
    if (!choresByRefId.has(targetRefId)) {
      activityDoneness[activity.ref_id] = TimePlanActivityDoneness.DONE;
      continue;
    }

    const { someWorkingOrDone, allDone, majorityDone } = subactivityFlags(
      activityDoneness,
      activitiesByChoreRefId.get(targetRefId) ?? [],
    );
    activityDoneness[activity.ref_id] = donenessFromSubRollUp(
      activity.kind,
      someWorkingOrDone,
      allDone,
      majorityDone,
    );
  }

  for (const activity of activities) {
    if (!isTimePlanActivityChoreStackTarget(activity.target)) {
      continue;
    }

    const stackRefId = entityLinkRefIdFromWire(activity.target);
    if (!choreStacksByRefId.has(stackRefId)) {
      activityDoneness[activity.ref_id] = TimePlanActivityDoneness.DONE;
      continue;
    }

    const memberChoreActivityRefIds = memberStackActivityRefIds(
      activities,
      choresByRefId,
      stackRefId,
      isTimePlanActivityChoreTarget,
    );
    const { someWorkingOrDone, allDone, majorityDone } = subactivityFlags(
      activityDoneness,
      memberChoreActivityRefIds,
    );
    activityDoneness[activity.ref_id] = donenessFromSubRollUp(
      activity.kind,
      someWorkingOrDone,
      allDone,
      majorityDone,
    );
  }

  return activityDoneness;
}

function appendIndexed(
  index: Map<string, string[]>,
  key: string,
  activityRefId: string,
): void {
  const existing = index.get(key);
  if (existing === undefined) {
    index.set(key, [activityRefId]);
    return;
  }
  existing.push(activityRefId);
}

function parseTimestampUtc(raw: string): DateTime {
  const iso = DateTime.fromISO(raw, { zone: "utc" });
  if (iso.isValid) {
    return iso;
  }
  const sql = DateTime.fromSQL(raw, { zone: "utc" });
  if (sql.isValid) {
    return sql;
  }
  throw new Error(`Invalid timestamp: ${raw}`);
}

function modifiedInTimePlanWindow(
  lastModifiedTime: string,
  startDate: string,
  endDate: string,
  extraDays: number,
): boolean {
  const ts = parseTimestampUtc(lastModifiedTime);
  const windowStart = DateTime.fromISO(startDate, { zone: "utc" }).startOf(
    "day",
  );
  // Exclusive upper bound equivalent to Python end-of-day of (endDate + extraDays).
  const windowEndExclusive = DateTime.fromISO(endDate, { zone: "utc" })
    .plus({ days: extraDays + 1 })
    .startOf("day");
  return ts >= windowStart && ts < windowEndExclusive;
}

function inboxTaskDoneness(
  timePlan: Pick<TimePlan, "start_date" | "end_date">,
  kind: TimePlanActivityKind,
  inboxTask: Pick<InboxTask, "status" | "last_modified_time">,
): TimePlanActivityDoneness {
  if (kind === TimePlanActivityKind.FINISH) {
    if (inboxTaskIsCompleted(inboxTask.status)) {
      return TimePlanActivityDoneness.DONE;
    }
    if (inboxTaskIsWorking(inboxTask.status)) {
      return TimePlanActivityDoneness.WORKING;
    }
    return TimePlanActivityDoneness.NOT_DONE;
  }

  const modifiedInTimePlan =
    inboxTaskIsWorkingOrMore(inboxTask.status) &&
    modifiedInTimePlanWindow(
      inboxTask.last_modified_time,
      timePlan.start_date,
      timePlan.end_date,
      INBOX_MAKE_PROGRESS_EXTRA_DAYS,
    );
  if (inboxTaskIsCompleted(inboxTask.status) || modifiedInTimePlan) {
    return TimePlanActivityDoneness.DONE;
  }
  if (inboxTaskIsWorking(inboxTask.status)) {
    return TimePlanActivityDoneness.WORKING;
  }
  return TimePlanActivityDoneness.NOT_DONE;
}

function bigPlanDoneness(
  timePlan: Pick<TimePlan, "start_date" | "end_date">,
  kind: TimePlanActivityKind,
  bigPlan: Pick<BigPlan, "status" | "last_modified_time">,
  someWorkingOrDone: boolean,
  allDone: boolean,
): TimePlanActivityDoneness {
  if (kind === TimePlanActivityKind.FINISH) {
    if (bigPlanIsCompleted(bigPlan.status)) {
      return TimePlanActivityDoneness.DONE;
    }
    if (someWorkingOrDone) {
      return TimePlanActivityDoneness.WORKING;
    }
    return TimePlanActivityDoneness.NOT_DONE;
  }

  const modifiedInTimePlan =
    bigPlanIsWorkingOrMore(bigPlan.status) &&
    modifiedInTimePlanWindow(
      bigPlan.last_modified_time,
      timePlan.start_date,
      timePlan.end_date,
      BIG_PLAN_MAKE_PROGRESS_EXTRA_DAYS,
    );
  if (bigPlanIsCompleted(bigPlan.status) || allDone) {
    return TimePlanActivityDoneness.DONE;
  }
  if (modifiedInTimePlan || someWorkingOrDone) {
    return TimePlanActivityDoneness.WORKING;
  }
  return TimePlanActivityDoneness.NOT_DONE;
}

function donenessOf(
  activityDoneness: Record<string, TimePlanActivityDoneness>,
  refId: string,
): TimePlanActivityDoneness {
  const value = activityDoneness[refId];
  if (value === undefined) {
    throw new Error(`Missing doneness for activity ${refId}`);
  }
  return value;
}

function subactivityFlags(
  activityDoneness: Record<string, TimePlanActivityDoneness>,
  subRefIds: readonly string[],
): {
  someWorkingOrDone: boolean;
  allDone: boolean;
  majorityDone: boolean;
} {
  if (subRefIds.length === 0) {
    return {
      someWorkingOrDone: false,
      allDone: false,
      majorityDone: false,
    };
  }
  const someWorkingOrDone = subRefIds.some((refId) => {
    const doneness = donenessOf(activityDoneness, refId);
    return (
      doneness === TimePlanActivityDoneness.WORKING ||
      doneness === TimePlanActivityDoneness.DONE
    );
  });
  const allDone = subRefIds.every(
    (refId) =>
      donenessOf(activityDoneness, refId) === TimePlanActivityDoneness.DONE,
  );
  const doneCount = subRefIds.filter(
    (refId) =>
      donenessOf(activityDoneness, refId) === TimePlanActivityDoneness.DONE,
  ).length;
  return {
    someWorkingOrDone,
    allDone,
    majorityDone: doneCount / subRefIds.length > 0.5,
  };
}

function donenessFromSubRollUp(
  kind: TimePlanActivityKind,
  someWorkingOrDone: boolean,
  allDone: boolean,
  majorityDone: boolean,
): TimePlanActivityDoneness {
  if (kind === TimePlanActivityKind.FINISH) {
    if (allDone) {
      return TimePlanActivityDoneness.DONE;
    }
    if (someWorkingOrDone) {
      return TimePlanActivityDoneness.WORKING;
    }
    return TimePlanActivityDoneness.NOT_DONE;
  }

  if (majorityDone) {
    return TimePlanActivityDoneness.DONE;
  }
  if (someWorkingOrDone) {
    return TimePlanActivityDoneness.WORKING;
  }
  return TimePlanActivityDoneness.NOT_DONE;
}

function memberStackActivityRefIds(
  activities: ReadonlyArray<
    Pick<TimePlanActivity, "ref_id" | "kind" | "target">
  >,
  membersByRefId: Map<string, { stack_ref_id?: string | null }>,
  stackRefId: string,
  isMemberTarget: (target: TimePlanActivity["target"]) => boolean,
): string[] {
  const memberActivityRefIds: string[] = [];
  for (const memberActivity of activities) {
    if (!isMemberTarget(memberActivity.target)) {
      continue;
    }
    const member = membersByRefId.get(
      entityLinkRefIdFromWire(memberActivity.target),
    );
    if (member === undefined || member.stack_ref_id !== stackRefId) {
      continue;
    }
    memberActivityRefIds.push(memberActivity.ref_id);
  }
  return memberActivityRefIds;
}
