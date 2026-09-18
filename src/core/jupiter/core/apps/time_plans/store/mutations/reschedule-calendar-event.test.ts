import type { TimeEventInDayBlock } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import { RESCHEDULE_CALENDAR_EVENT } from "#/core/apps/time_plans/store/mutations/reschedule-calendar-event";
import {
  createTimePlanStore,
  seedTimePlanSource,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

const MODIFIED = "2026-09-14T10:00:00Z";

function entities() {
  return selectTimePlanEntities(
    seedTimePlanSource(createTimePlanStore(), "calendar", {
      timeEventBlocks: [
        {
          ref_id: "30",
          version: 1,
          archived: false,
          start_date: "2026-09-14",
          start_time_in_day: "08:00",
          duration_mins: 30,
        } as TimeEventInDayBlock,
      ],
    }),
  );
}

const MOVE = {
  kind: "time-event-in-day-block" as const,
  refId: "30",
  blockRefId: "30",
  // Bucharest is three hours ahead of UTC in September.
  startDate: "2026-09-15",
  startTimeInDay: "10:30",
  userTimezone: "Europe/Bucharest",
  modifiedTime: MODIFIED,
};

describe("RESCHEDULE_CALENDAR_EVENT", () => {
  it("moves the block, keeping it in UTC", () => {
    const moved = RESCHEDULE_CALENDAR_EVENT.applyOptimistic(entities(), MOVE)
      .timeEventBlocks["30"];

    expect(moved).toMatchObject({
      start_date: "2026-09-15",
      start_time_in_day: "07:30",
      duration_mins: 30,
      last_modified_time: MODIFIED,
    });
  });

  it("stretches the block when a duration comes along", () => {
    const stretched = RESCHEDULE_CALENDAR_EVENT.applyOptimistic(entities(), {
      ...MOVE,
      durationMins: "75",
    }).timeEventBlocks["30"];

    expect(stretched.duration_mins).toBe(75);
  });

  it("only posts a duration for a stretch", () => {
    expect(RESCHEDULE_CALENDAR_EVENT.toFormFields(MOVE)).not.toHaveProperty(
      "durationMins",
    );
    expect(
      RESCHEDULE_CALENDAR_EVENT.toFormFields({ ...MOVE, durationMins: "75" })
        .durationMins,
    ).toBe("75");
  });
});
