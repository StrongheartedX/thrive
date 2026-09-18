import type {
  BigPlanStats,
  InboxTask,
  TimePlanActivity,
} from "@jupiter/webapi-client";
import {
  InboxTaskStatus,
  TimePlanActivityDoneness,
  TimePlanActivityKind,
} from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import type {
  PendingTimePlanMutation,
  TimePlanEntities,
} from "#/core/apps/time_plans/store/store";
import {
  createTimePlanStore,
  dropTimePlanSource,
  enqueueTimePlanMutation,
  rejectTimePlanMutation,
  resolveTimePlanMutation,
  seedTimePlanSource,
  selectActivityDoneness,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

function inboxTask(refId: string, fields: Partial<InboxTask> = {}): InboxTask {
  return {
    ref_id: refId,
    version: 1,
    archived: false,
    name: `Task ${refId}`,
    status: InboxTaskStatus.NOT_STARTED,
    last_modified_time: "2026-07-08T12:00:00Z",
    owner: "TodoTask:std:700",
    ...fields,
  } as InboxTask;
}

function activity(
  refId: string,
  fields: Partial<TimePlanActivity> = {},
): TimePlanActivity {
  return {
    ref_id: refId,
    version: 1,
    archived: false,
    time_plan_ref_id: "tp1",
    target: "InboxTask:std:100",
    kind: TimePlanActivityKind.FINISH,
    ...fields,
  } as TimePlanActivity;
}

function renameInboxTask(
  id: string,
  refId: string,
  name: string,
): PendingTimePlanMutation {
  return {
    id,
    applyOptimistic: (entities: TimePlanEntities): TimePlanEntities => ({
      ...entities,
      inboxTasks: {
        ...entities.inboxTasks,
        [refId]: { ...entities.inboxTasks[refId], name },
      },
    }),
  };
}

describe("seedTimePlanSource", () => {
  it("adds the entities of a source", () => {
    const store = seedTimePlanSource(createTimePlanStore(), "plan", {
      inboxTasks: [inboxTask("100"), inboxTask("101")],
      activities: [activity("1")],
    });

    const entities = selectTimePlanEntities(store);
    expect(Object.keys(entities.inboxTasks).sort()).toEqual(["100", "101"]);
    expect(Object.keys(entities.activities)).toEqual(["1"]);
  });

  it("keeps an entity already held at a newer version", () => {
    let store = seedTimePlanSource(createTimePlanStore(), "plan", {
      inboxTasks: [inboxTask("100", { version: 3, name: "Newer" })],
    });
    store = seedTimePlanSource(store, "leaf", {
      inboxTasks: [inboxTask("100", { version: 2, name: "Older" })],
    });

    expect(selectTimePlanEntities(store).inboxTasks["100"].name).toBe("Newer");
  });

  it("removes what a source no longer contributes on reseed", () => {
    let store = seedTimePlanSource(createTimePlanStore(), "plan", {
      inboxTasks: [inboxTask("100"), inboxTask("101")],
    });
    store = seedTimePlanSource(store, "plan", {
      inboxTasks: [inboxTask("100")],
    });

    expect(Object.keys(selectTimePlanEntities(store).inboxTasks)).toEqual([
      "100",
    ]);
  });

  it("keeps an entity until every source holding it is dropped", () => {
    let store = seedTimePlanSource(createTimePlanStore(), "plan", {
      inboxTasks: [inboxTask("100")],
    });
    store = seedTimePlanSource(store, "leaf", {
      inboxTasks: [inboxTask("100"), inboxTask("200")],
    });

    store = dropTimePlanSource(store, "leaf");
    expect(Object.keys(selectTimePlanEntities(store).inboxTasks)).toEqual([
      "100",
    ]);

    store = dropTimePlanSource(store, "plan");
    expect(selectTimePlanEntities(store).inboxTasks).toEqual({});
  });

  it("replaces big plan stats, which have no version", () => {
    const stats = (completed: number): BigPlanStats => ({
      created_time: "2026-07-01T00:00:00Z",
      last_modified_time: "2026-07-01T00:00:00Z",
      big_plan_ref_id: "bp1",
      all_inbox_tasks_cnt: 3,
      completed_inbox_tasks_cnt: completed,
    });
    let store = seedTimePlanSource(createTimePlanStore(), "plan", {
      bigPlanStats: [stats(1)],
    });
    store = seedTimePlanSource(store, "plan", { bigPlanStats: [stats(2)] });

    expect(
      selectTimePlanEntities(store).bigPlanStats["bp1"]
        .completed_inbox_tasks_cnt,
    ).toBe(2);
  });
});

describe("pending mutations", () => {
  it("are applied in order without changing the confirmed state", () => {
    let store = seedTimePlanSource(createTimePlanStore(), "plan", {
      inboxTasks: [inboxTask("100")],
    });
    store = enqueueTimePlanMutation(store, renameInboxTask("m1", "100", "A"));
    store = enqueueTimePlanMutation(store, renameInboxTask("m2", "100", "B"));

    expect(selectTimePlanEntities(store).inboxTasks["100"].name).toBe("B");
    expect(store.confirmed.inboxTasks["100"].name).toBe("Task 100");
  });

  it("merge the result and stop applying on resolve", () => {
    let store = seedTimePlanSource(createTimePlanStore(), "plan", {
      inboxTasks: [inboxTask("100")],
    });
    store = enqueueTimePlanMutation(store, renameInboxTask("m1", "100", "A"));
    store = resolveTimePlanMutation(
      store,
      "m1",
      { inboxTasks: [inboxTask("100", { version: 2, name: "From server" })] },
      "plan",
    );

    expect(store.pending).toEqual([]);
    expect(selectTimePlanEntities(store).inboxTasks["100"].name).toBe(
      "From server",
    );
  });

  it("attribute new entities from a result to the given source", () => {
    let store = seedTimePlanSource(createTimePlanStore(), "leaf", {});
    store = resolveTimePlanMutation(
      store,
      "m1",
      { activities: [activity("9")] },
      "leaf",
    );
    expect(Object.keys(selectTimePlanEntities(store).activities)).toEqual([
      "9",
    ]);

    store = dropTimePlanSource(store, "leaf");
    expect(selectTimePlanEntities(store).activities).toEqual({});
  });

  it("delete entities a result removes", () => {
    let store = seedTimePlanSource(createTimePlanStore(), "plan", {
      activities: [activity("1"), activity("2")],
    });
    store = resolveTimePlanMutation(
      store,
      "m1",
      { removed: { activities: ["2"] } },
      "plan",
    );

    expect(Object.keys(selectTimePlanEntities(store).activities)).toEqual([
      "1",
    ]);
  });

  it("roll back on reject", () => {
    let store = seedTimePlanSource(createTimePlanStore(), "plan", {
      inboxTasks: [inboxTask("100")],
    });
    store = enqueueTimePlanMutation(store, renameInboxTask("m1", "100", "A"));
    store = rejectTimePlanMutation(store, "m1");

    expect(selectTimePlanEntities(store).inboxTasks["100"].name).toBe(
      "Task 100",
    );
  });

  it("stay applied when a source is reseeded", () => {
    let store = seedTimePlanSource(createTimePlanStore(), "plan", {
      inboxTasks: [inboxTask("100")],
    });
    store = enqueueTimePlanMutation(store, renameInboxTask("m1", "100", "A"));
    store = seedTimePlanSource(store, "plan", {
      inboxTasks: [inboxTask("100", { version: 2 })],
    });

    expect(selectTimePlanEntities(store).inboxTasks["100"].name).toBe("A");
  });
});

describe("selectActivityDoneness", () => {
  it("derives doneness for the live activities of the time plan", () => {
    const store = seedTimePlanSource(createTimePlanStore(), "plan", {
      activities: [
        activity("1"),
        activity("2", { archived: true }),
        activity("3", { time_plan_ref_id: "tp2" }),
      ],
      inboxTasks: [inboxTask("100", { status: InboxTaskStatus.DONE })],
    });

    const doneness = selectActivityDoneness(selectTimePlanEntities(store), {
      ref_id: "tp1",
      start_date: "2026-07-06",
      end_date: "2026-07-12",
    });

    expect(doneness).toEqual({ "1": TimePlanActivityDoneness.DONE });
  });
});
