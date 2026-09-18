/**
 * What the time plan view renders, selected from the store's entities.
 *
 * The lists mirror what ``TimePlanLoadService`` returns for a plan, so the
 * routes can use them in place of the loader's.
 */
import type {
  BigPlan,
  BigPlanStats,
  Chore,
  ChoreStack,
  EntityLink,
  Habit,
  HabitStack,
  InboxTask,
  TimeEventInDayBlock,
  TimePlan,
  TimePlanActivity,
  TimePlanActivityDoneness,
  TodoTask,
} from "@jupiter/webapi-client";
import { NamedEntityTag } from "@jupiter/webapi-client";

import { entityLinkStd, parseEntityLink } from "#/core/common/entity-link";
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
import { selectActivityDoneness } from "#/core/apps/time_plans/store/store";

export interface TimePlanView {
  activities: TimePlanActivity[];
  targetInboxTasks: InboxTask[];
  targetBigPlans: BigPlan[];
  bigPlanStats: BigPlanStats[];
  targetTodoTasks: TodoTask[];
  targetHabits: Habit[];
  targetHabitStacks: HabitStack[];
  targetChores: Chore[];
  targetChoreStacks: ChoreStack[];
  activityTimeEventBlocks: TimeEventInDayBlock[];
  activityDoneness: Record<string, TimePlanActivityDoneness>;
}

function pick<T>(table: EntityTable<T>, refIds: Iterable<string>): T[] {
  const result: T[] = [];
  for (const refId of refIds) {
    const entity = table[refId];
    if (entity !== undefined) {
      result.push(entity);
    }
  }
  return result;
}

export function selectTimePlanView(
  entities: TimePlanEntities,
  timePlan: Pick<TimePlan, "ref_id" | "start_date" | "end_date">,
): TimePlanView {
  const activities = Object.values(entities.activities).filter(
    (activity) =>
      activity.time_plan_ref_id === timePlan.ref_id && !activity.archived,
  );

  function targetRefIds(isTarget: (target: EntityLink) => boolean) {
    return new Set(
      activities
        .filter((activity) => isTarget(activity.target))
        .map((activity) => entityLinkRefIdFromWire(activity.target)),
    );
  }

  const directInboxTasks = pick(
    entities.inboxTasks,
    targetRefIds(isTimePlanActivityInboxTaskTarget),
  );
  const targetTodoTasks = pick(
    entities.todoTasks,
    targetRefIds(isTimePlanActivityTodoTaskTarget),
  );

  // Like the server, a target todo task brings its inbox task along.
  const todoOwners = new Set(
    targetTodoTasks.map((todoTask) =>
      entityLinkStd(NamedEntityTag.TODO_TASK, todoTask.ref_id),
    ),
  );
  const directInboxTaskRefIds = new Set(
    directInboxTasks.map((inboxTask) => inboxTask.ref_id),
  );
  const todoOwnedInboxTasks =
    todoOwners.size === 0
      ? []
      : Object.values(entities.inboxTasks).filter(
          (inboxTask) =>
            todoOwners.has(inboxTask.owner) &&
            !directInboxTaskRefIds.has(inboxTask.ref_id),
        );

  // And the big plans owning target inbox tasks come along too.
  const bigPlanRefIds = targetRefIds(isTimePlanActivityBigPlanTarget);
  for (const inboxTask of directInboxTasks) {
    const owner = parseEntityLink(inboxTask.owner);
    if (owner.theType === NamedEntityTag.BIG_PLAN) {
      bigPlanRefIds.add(owner.refId);
    }
  }

  const activityOwners = new Set(
    activities.map((activity) =>
      entityLinkStd(NamedEntityTag.TIME_PLAN_ACTIVITY, activity.ref_id),
    ),
  );

  return {
    activities,
    targetInboxTasks: [...directInboxTasks, ...todoOwnedInboxTasks],
    targetBigPlans: pick(entities.bigPlans, bigPlanRefIds),
    bigPlanStats: Object.values(entities.bigPlanStats),
    targetTodoTasks,
    targetHabits: pick(
      entities.habits,
      targetRefIds(isTimePlanActivityHabitTarget),
    ),
    targetHabitStacks: pick(
      entities.habitStacks,
      targetRefIds(isTimePlanActivityHabitStackTarget),
    ),
    targetChores: pick(
      entities.chores,
      targetRefIds(isTimePlanActivityChoreTarget),
    ),
    targetChoreStacks: pick(
      entities.choreStacks,
      targetRefIds(isTimePlanActivityChoreStackTarget),
    ),
    activityTimeEventBlocks: Object.values(entities.timeEventBlocks).filter(
      (block) => !block.archived && activityOwners.has(block.owner),
    ),
    activityDoneness: selectActivityDoneness(entities, timePlan),
  };
}

/** The store's copy of ``entity`` if it has one, else ``entity`` itself. */
export function latestEntity<T extends { ref_id: string }>(
  table: EntityTable<T>,
  entity: T,
): T {
  return table[entity.ref_id] ?? entity;
}

export function latestEntityOrNull<T extends { ref_id: string }>(
  table: EntityTable<T>,
  entity: T | null | undefined,
): T | null | undefined {
  return entity === null || entity === undefined
    ? entity
    : latestEntity(table, entity);
}

export function latestEntities<T extends { ref_id: string }>(
  table: EntityTable<T>,
  entities: ReadonlyArray<T>,
): T[] {
  return entities.map((entity) => latestEntity(table, entity));
}
