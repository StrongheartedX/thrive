import type {
  BigPlan,
  Habit,
  HabitStack,
  InboxTask,
  TimeEventInDayBlock,
  TimePlanActivity,
  TodoTask,
} from "@jupiter/webapi-client";
import { TimePlanActivityKind } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import { snapshotFromTimePlanActivityLoad } from "#/core/apps/time_plans/store/snapshots";
import {
  createTimePlanStore,
  seedTimePlanSource,
  selectTimePlanEntities,
  syncTimePlanSources,
} from "#/core/apps/time_plans/store/store";
import {
  latestEntities,
  selectTimePlanView,
} from "#/core/apps/time_plans/store/view";

const TIME_PLAN = {
  ref_id: "tp1",
  start_date: "2026-07-06",
  end_date: "2026-07-12",
};

function activity(
  refId: string,
  target: string,
  fields: Partial<TimePlanActivity> = {},
): TimePlanActivity {
  return {
    ref_id: refId,
    version: 1,
    archived: false,
    time_plan_ref_id: "tp1",
    target,
    kind: TimePlanActivityKind.FINISH,
    ...fields,
  } as TimePlanActivity;
}

function inboxTask(
  refId: string,
  owner: string,
  fields: Partial<InboxTask> = {},
): InboxTask {
  return {
    ref_id: refId,
    version: 1,
    archived: false,
    owner,
    last_modified_time: "2026-07-08T12:00:00Z",
    ...fields,
  } as InboxTask;
}

function withRefId<T>(refId: string, fields: Partial<T> = {}): T {
  return { ref_id: refId, version: 1, archived: false, ...fields } as T;
}

describe("selectTimePlanView", () => {
  it("only has the time plan's live activities", () => {
    const store = seedTimePlanSource(createTimePlanStore(), "plan", {
      activities: [
        activity("1", "InboxTask:std:100"),
        activity("2", "InboxTask:std:101", { archived: true }),
        activity("3", "InboxTask:std:102", { time_plan_ref_id: "tp2" }),
      ],
    });

    const view = selectTimePlanView(selectTimePlanEntities(store), TIME_PLAN);

    expect(view.activities.map((a) => a.ref_id)).toEqual(["1"]);
  });

  it("brings in target todo tasks' inbox tasks and target inbox tasks' big plans", () => {
    const store = seedTimePlanSource(createTimePlanStore(), "plan", {
      activities: [
        activity("1", "InboxTask:std:100"),
        activity("2", "TodoTask:std:700"),
      ],
      inboxTasks: [
        inboxTask("100", "BigPlan:std:500"),
        inboxTask("101", "TodoTask:std:700"),
        inboxTask("102", "TodoTask:std:701"),
      ],
      todoTasks: [withRefId<TodoTask>("700")],
      bigPlans: [withRefId<BigPlan>("500"), withRefId<BigPlan>("501")],
    });

    const view = selectTimePlanView(selectTimePlanEntities(store), TIME_PLAN);

    expect(view.targetInboxTasks.map((it) => it.ref_id)).toEqual([
      "100",
      "101",
    ]);
    expect(view.targetTodoTasks.map((tt) => tt.ref_id)).toEqual(["700"]);
    expect(view.targetBigPlans.map((bp) => bp.ref_id)).toEqual(["500"]);
  });

  it("only has live time event blocks of the plan's activities", () => {
    const block = (refId: string, owner: string, archived = false) =>
      withRefId<TimeEventInDayBlock>(refId, { owner, archived });
    const store = seedTimePlanSource(createTimePlanStore(), "plan", {
      activities: [activity("1", "InboxTask:std:100")],
      timeEventBlocks: [
        block("900", "TimePlanActivity:std:1"),
        block("901", "TimePlanActivity:std:1", true),
        block("902", "TimePlanActivity:std:2"),
        block("903", "BigPlan:std:500"),
      ],
    });

    const view = selectTimePlanView(selectTimePlanEntities(store), TIME_PLAN);

    expect(view.activityTimeEventBlocks.map((b) => b.ref_id)).toEqual(["900"]);
  });
});

describe("syncTimePlanSources", () => {
  it("reseeds changed sources, drops removed ones, and skips unchanged ones", () => {
    const plan = { inboxTasks: [inboxTask("100", "TodoTask:std:700")] };
    const leaf = { inboxTasks: [inboxTask("200", "TodoTask:std:701")] };
    const store = syncTimePlanSources(
      createTimePlanStore(),
      {},
      { plan, leaf },
    );

    expect(syncTimePlanSources(store, { plan, leaf }, { plan, leaf })).toBe(
      store,
    );

    const withoutLeaf = syncTimePlanSources(
      store,
      { plan, leaf },
      { plan, leaf: undefined },
    );
    expect(Object.keys(selectTimePlanEntities(withoutLeaf).inboxTasks)).toEqual(
      ["100"],
    );
  });
});

describe("snapshotFromTimePlanActivityLoad", () => {
  it("collects the entities the activity panel shows", () => {
    const snapshot = snapshotFromTimePlanActivityLoad({
      timePlanActivity: activity("1", "HabitStack:std:300"),
      targetHabitStack: withRefId<HabitStack>("300"),
      targetHabitStackInfo: { habits: [withRefId<Habit>("400")] },
      stackInboxTasks: [inboxTask("100", "Habit:std:400")],
      targetInboxTask: null,
    });

    const entities = selectTimePlanEntities(
      seedTimePlanSource(createTimePlanStore(), "activity", snapshot),
    );

    expect(Object.keys(entities.activities)).toEqual(["1"]);
    expect(Object.keys(entities.habitStacks)).toEqual(["300"]);
    expect(Object.keys(entities.habits)).toEqual(["400"]);
    expect(Object.keys(entities.inboxTasks)).toEqual(["100"]);
  });
});

describe("latestEntities", () => {
  it("prefers the store's copy and falls back to the given entity", () => {
    const entities = selectTimePlanEntities(
      seedTimePlanSource(createTimePlanStore(), "plan", {
        inboxTasks: [
          inboxTask("100", "TodoTask:std:700", { version: 2, name: "Store" }),
        ],
      }),
    );

    const result = latestEntities(entities.inboxTasks, [
      inboxTask("100", "TodoTask:std:700", { name: "Loader" }),
      inboxTask("101", "TodoTask:std:701", { name: "Only loader" }),
    ]);

    expect(result.map((it) => it.name)).toEqual(["Store", "Only loader"]);
  });
});
