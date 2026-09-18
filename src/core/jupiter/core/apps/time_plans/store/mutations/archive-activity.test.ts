import type { TimePlanActivity } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  ARCHIVE_TIME_PLAN_ACTIVITY,
  REMOVE_TIME_PLAN_ACTIVITY,
} from "#/core/apps/time_plans/store/mutations/archive-activity";
import {
  createTimePlanStore,
  enqueueTimePlanMutation,
  resolveTimePlanMutation,
  seedTimePlanSource,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

const MODIFIED = "2026-09-14T10:00:00Z";

function activity(refId: string, fields: Partial<TimePlanActivity> = {}) {
  return {
    ref_id: refId,
    version: 1,
    archived: false,
    time_plan_ref_id: "9",
    target: `BigPlan:std:${refId}`,
    last_modified_time: "2026-09-01T00:00:00Z",
    ...fields,
  } as TimePlanActivity;
}

function seeded() {
  return seedTimePlanSource(createTimePlanStore(), "plan", {
    activities: [activity("20"), activity("21"), activity("22")],
  });
}

describe("ARCHIVE_TIME_PLAN_ACTIVITY", () => {
  it("archives the activity right away", () => {
    const entities = ARCHIVE_TIME_PLAN_ACTIVITY.applyOptimistic(
      selectTimePlanEntities(seeded()),
      { refId: "20", modifiedTime: MODIFIED },
    );

    expect(entities.activities["20"]).toMatchObject({
      archived: true,
      archived_time: MODIFIED,
    });
    expect(entities.activities["21"].archived).toBe(false);
  });

  it("merges back every activity the server archived along with it", () => {
    const archived = [
      activity("20", { version: 2, archived: true }),
      activity("21", { version: 2, archived: true }),
    ];
    let store = enqueueTimePlanMutation(seeded(), {
      id: "m1",
      applyOptimistic: (entities) =>
        ARCHIVE_TIME_PLAN_ACTIVITY.applyOptimistic(entities, {
          refId: "20",
          modifiedTime: MODIFIED,
        }),
    });
    store = resolveTimePlanMutation(
      store,
      "m1",
      ARCHIVE_TIME_PLAN_ACTIVITY.toDelta({
        archived_time_plan_activities: archived,
      }),
      "plan",
    );

    const entities = selectTimePlanEntities(store);
    expect(entities.activities["20"].archived).toBe(true);
    expect(entities.activities["21"].archived).toBe(true);
    expect(entities.activities["22"].archived).toBe(false);
  });
});

describe("REMOVE_TIME_PLAN_ACTIVITY", () => {
  it("drops the activity right away", () => {
    const entities = REMOVE_TIME_PLAN_ACTIVITY.applyOptimistic(
      selectTimePlanEntities(seeded()),
      { refId: "20" },
    );

    expect(entities.activities["20"]).toBeUndefined();
    expect(entities.activities["21"]).toBeDefined();
  });

  it("drops every activity the server removed along with it", () => {
    let store = enqueueTimePlanMutation(seeded(), {
      id: "m1",
      applyOptimistic: (entities) =>
        REMOVE_TIME_PLAN_ACTIVITY.applyOptimistic(entities, { refId: "20" }),
    });
    store = resolveTimePlanMutation(
      store,
      "m1",
      REMOVE_TIME_PLAN_ACTIVITY.toDelta({
        removed_time_plan_activity_ref_ids: ["20", "21"],
      }),
      "plan",
    );

    const entities = selectTimePlanEntities(store);
    expect(entities.activities["20"]).toBeUndefined();
    expect(entities.activities["21"]).toBeUndefined();
    expect(entities.activities["22"]).toBeDefined();
  });
});
