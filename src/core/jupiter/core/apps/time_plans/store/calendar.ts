/**
 * The time plan view's calendar, drawn from the store.
 *
 * The calendar loader's entries hold the period's events. Their in-day blocks
 * and time plan activities are seeded into the store, and the entries are drawn
 * with the store's latest blocks and entities, so moving, editing or archiving
 * an event shows up without reloading the calendar.
 */
import type {
  CalendarEventsEntries,
  TimeEventInDayBlock,
  TimePlanActivity,
} from "@jupiter/webapi-client";

import type {
  TimePlanEntities,
  TimePlanEntitySnapshot,
} from "#/core/apps/time_plans/store/store";
import {
  latestEntity,
  latestEntityOrNull,
} from "#/core/apps/time_plans/store/view";
import {
  isTimePlanActivityBigPlanTarget,
  isTimePlanActivityChoreStackTarget,
  isTimePlanActivityChoreTarget,
  isTimePlanActivityHabitStackTarget,
  isTimePlanActivityHabitTarget,
  isTimePlanActivityInboxTaskTarget,
  isTimePlanActivityTodoTaskTarget,
} from "#/core/apps/time_plans/sub/activity/target-wire";
import { parseEntityLinkStd } from "#/core/common/entity-link";

type Maybe<T> = T | null | undefined;

export function snapshotFromCalendarEntries(
  entries: Maybe<CalendarEventsEntries>,
): TimePlanEntitySnapshot {
  if (!entries) {
    return {};
  }
  return {
    activities: entries.time_plan_activity_entries.map(
      (entry) => entry.time_plan_activity,
    ),
    timeEventBlocks: [
      ...entries.schedule_event_in_day_entries.map((entry) => entry.time_event),
      ...entries.time_plan_activity_entries.flatMap(
        (entry) => entry.time_events,
      ),
      ...entries.big_plan_entries.flatMap((entry) => entry.time_events),
      ...entries.todo_task_entries.flatMap((entry) => entry.time_events),
      ...entries.habit_entries.flatMap((entry) => entry.time_events),
      ...entries.chore_entries.flatMap((entry) => entry.time_events),
    ],
  };
}

function latestBlocks(
  entities: TimePlanEntities,
  blocks: ReadonlyArray<TimeEventInDayBlock>,
): TimeEventInDayBlock[] {
  return blocks
    .map((block) => latestEntity(entities.timeEventBlocks, block))
    .filter((block) => !block.archived);
}

type TimePlanActivityEntry =
  CalendarEventsEntries["time_plan_activity_entries"][number];

const ACTIVITY_OWNER_PREFIX = "TimePlanActivity:std:";

function activityTargets(
  entities: TimePlanEntities,
  activity: TimePlanActivity,
): Omit<TimePlanActivityEntry, "time_plan_activity" | "time_events"> {
  const { refId } = parseEntityLinkStd(activity.target);
  const target = activity.target;
  return {
    target_inbox_task: isTimePlanActivityInboxTaskTarget(target)
      ? (entities.inboxTasks[refId] ?? null)
      : null,
    target_big_plan: isTimePlanActivityBigPlanTarget(target)
      ? (entities.bigPlans[refId] ?? null)
      : null,
    target_todo_task: isTimePlanActivityTodoTaskTarget(target)
      ? (entities.todoTasks[refId] ?? null)
      : null,
    target_habit: isTimePlanActivityHabitTarget(target)
      ? (entities.habits[refId] ?? null)
      : null,
    target_habit_stack: isTimePlanActivityHabitStackTarget(target)
      ? (entities.habitStacks[refId] ?? null)
      : null,
    target_chore: isTimePlanActivityChoreTarget(target)
      ? (entities.chores[refId] ?? null)
      : null,
    target_chore_stack: isTimePlanActivityChoreStackTarget(target)
      ? (entities.choreStacks[refId] ?? null)
      : null,
  };
}

function selectActivityEntries(
  entries: CalendarEventsEntries,
  entities: TimePlanEntities,
  timePlanRefId: string,
): TimePlanActivityEntry[] {
  // What the store has for each activity, events placed since the calendar
  // loaded included.
  const storeBlocksByActivity = new Map<string, TimeEventInDayBlock[]>();
  for (const block of Object.values(entities.timeEventBlocks)) {
    if (block.archived || !block.owner.startsWith(ACTIVITY_OWNER_PREFIX)) {
      continue;
    }
    const activityRefId = block.owner.slice(ACTIVITY_OWNER_PREFIX.length);
    storeBlocksByActivity.set(activityRefId, [
      ...(storeBlocksByActivity.get(activityRefId) ?? []),
      block,
    ]);
  }

  const activitiesWithEntries = new Set<string>();
  const selected = entries.time_plan_activity_entries.flatMap((entry) => {
    activitiesWithEntries.add(entry.time_plan_activity.ref_id);
    // The activities are seeded from these very entries, so one that's
    // missing from the store was removed.
    const activity = entities.activities[entry.time_plan_activity.ref_id];
    if (activity === undefined || activity.archived) {
      return [];
    }
    const loaded = new Set(entry.time_events.map((block) => block.ref_id));
    return [
      {
        ...entry,
        time_plan_activity: activity,
        target_inbox_task: latestEntityOrNull(
          entities.inboxTasks,
          entry.target_inbox_task,
        ),
        target_big_plan: latestEntityOrNull(
          entities.bigPlans,
          entry.target_big_plan,
        ),
        target_todo_task: latestEntityOrNull(
          entities.todoTasks,
          entry.target_todo_task,
        ),
        target_habit: latestEntityOrNull(entities.habits, entry.target_habit),
        target_habit_stack: latestEntityOrNull(
          entities.habitStacks,
          entry.target_habit_stack,
        ),
        target_chore: latestEntityOrNull(entities.chores, entry.target_chore),
        target_chore_stack: latestEntityOrNull(
          entities.choreStacks,
          entry.target_chore_stack,
        ),
        time_events: [
          ...latestBlocks(entities, entry.time_events),
          ...(storeBlocksByActivity.get(activity.ref_id) ?? []).filter(
            (block) => !loaded.has(block.ref_id),
          ),
        ],
      },
    ];
  });

  // Activities of this plan that had no events when the calendar loaded, but
  // have some now.
  const placed = Object.values(entities.activities)
    .filter(
      (activity) =>
        !activity.archived &&
        activity.time_plan_ref_id === timePlanRefId &&
        !activitiesWithEntries.has(activity.ref_id) &&
        storeBlocksByActivity.has(activity.ref_id),
    )
    .map((activity) => ({
      time_plan_activity: activity,
      ...activityTargets(entities, activity),
      time_events: storeBlocksByActivity.get(activity.ref_id) ?? [],
    }));

  return [...selected, ...placed];
}

/** ``entries`` with the store's latest blocks and entities. */
export function selectCalendarEntries(
  entries: Maybe<CalendarEventsEntries>,
  entities: TimePlanEntities,
  timePlanRefId: string,
): CalendarEventsEntries | null {
  if (!entries) {
    return null;
  }
  return {
    ...entries,
    schedule_event_in_day_entries: entries.schedule_event_in_day_entries
      .map((entry) => ({
        ...entry,
        time_event: latestEntity(entities.timeEventBlocks, entry.time_event),
      }))
      .filter((entry) => !entry.time_event.archived),
    time_plan_activity_entries: selectActivityEntries(
      entries,
      entities,
      timePlanRefId,
    ),
    big_plan_entries: entries.big_plan_entries.map((entry) => ({
      ...entry,
      big_plan: latestEntity(entities.bigPlans, entry.big_plan),
      time_events: latestBlocks(entities, entry.time_events),
    })),
    todo_task_entries: entries.todo_task_entries.map((entry) => ({
      ...entry,
      todo_task: latestEntity(entities.todoTasks, entry.todo_task),
      inbox_task: latestEntity(entities.inboxTasks, entry.inbox_task),
      time_events: latestBlocks(entities, entry.time_events),
    })),
    habit_entries: entries.habit_entries.map((entry) => ({
      ...entry,
      habit: latestEntity(entities.habits, entry.habit),
      time_events: latestBlocks(entities, entry.time_events),
    })),
    chore_entries: entries.chore_entries.map((entry) => ({
      ...entry,
      chore: latestEntity(entities.chores, entry.chore),
      time_events: latestBlocks(entities, entry.time_events),
    })),
  };
}
