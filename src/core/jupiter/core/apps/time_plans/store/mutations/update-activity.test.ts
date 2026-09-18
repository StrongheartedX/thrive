import type { TimePlanActivity } from "@jupiter/webapi-client";
import {
  TimePlanActivityFeasability,
  TimePlanActivityKind,
} from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  UPDATE_TIME_PLAN_ACTIVITY,
  updateTimePlanActivityArgsFromForm,
} from "#/core/apps/time_plans/store/mutations/update-activity";
import {
  createTimePlanStore,
  seedTimePlanSource,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

function activity(fields: Partial<TimePlanActivity> = {}): TimePlanActivity {
  return {
    ref_id: "1",
    version: 1,
    archived: false,
    time_plan_ref_id: "tp1",
    target: "InboxTask:std:100",
    kind: TimePlanActivityKind.FINISH,
    feasability: TimePlanActivityFeasability.MUST_DO,
    ...fields,
  } as TimePlanActivity;
}

const ARGS = {
  refId: "1",
  kind: TimePlanActivityKind.MAKE_PROGRESS,
  feasability: TimePlanActivityFeasability.STRETCH,
};

describe("UPDATE_TIME_PLAN_ACTIVITY", () => {
  it("reads its args from the properties form", () => {
    const formData = new FormData();
    formData.set("kind", TimePlanActivityKind.MAKE_PROGRESS);
    formData.set("feasability", TimePlanActivityFeasability.STRETCH);

    expect(updateTimePlanActivityArgsFromForm("1", formData)).toEqual(ARGS);
  });

  it("changes the activity right away", () => {
    const entities = selectTimePlanEntities(
      seedTimePlanSource(createTimePlanStore(), "plan", {
        activities: [activity()],
      }),
    );

    const updated = UPDATE_TIME_PLAN_ACTIVITY.applyOptimistic(entities, ARGS);

    expect(updated.activities["1"].kind).toBe(
      TimePlanActivityKind.MAKE_PROGRESS,
    );
    expect(updated.activities["1"].feasability).toBe(
      TimePlanActivityFeasability.STRETCH,
    );
    expect(entities.activities["1"].kind).toBe(TimePlanActivityKind.FINISH);
  });

  it("leaves the entities alone for an activity it doesn't hold", () => {
    const entities = selectTimePlanEntities(createTimePlanStore());

    expect(UPDATE_TIME_PLAN_ACTIVITY.applyOptimistic(entities, ARGS)).toBe(
      entities,
    );
  });

  it("merges back the updated activity", () => {
    const result = activity({
      version: 2,
      kind: TimePlanActivityKind.MAKE_PROGRESS,
    });

    expect(
      UPDATE_TIME_PLAN_ACTIVITY.toDelta({ updated_time_plan_activity: result }),
    ).toEqual({ activities: [result] });
  });
});
