import type { TimeEventInDayBlock } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  PLACE_TIME_EVENTS,
  placeTimeEventsArgsFromCalendar,
} from "#/core/apps/time_plans/store/mutations/place-time-events";
import {
  createTimePlanStore,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

const MODIFIED = "2026-09-14T10:00:00Z";

const DROP = {
  timePlanActivityRefId: "20",
  // Bucharest is three hours ahead of UTC in September.
  startDate: "2026-09-15",
  startTimeInDay: "10:30",
  durationMins: "30",
  extraPlacements: "",
  userTimezone: "Europe/Bucharest",
};

describe("placeTimeEventsArgsFromCalendar", () => {
  it("places the dropped activity", () => {
    expect(
      placeTimeEventsArgsFromCalendar(DROP, "p1", MODIFIED).placements,
    ).toEqual([{ activityRefId: "20", durationMins: 30 }]);
  });

  it("places a stack's members instead, when the drop brings them", () => {
    const members = [
      { activityRefId: "21", durationMins: 15 },
      { activityRefId: "22", durationMins: 45 },
    ];

    expect(
      placeTimeEventsArgsFromCalendar(
        { ...DROP, extraPlacements: JSON.stringify(members) },
        "p1",
        MODIFIED,
      ).placements,
    ).toEqual(members);
  });
});

describe("PLACE_TIME_EVENTS", () => {
  const members = placeTimeEventsArgsFromCalendar(
    {
      ...DROP,
      extraPlacements: JSON.stringify([
        { activityRefId: "21", durationMins: 15 },
        { activityRefId: "22", durationMins: 45 },
      ]),
    },
    "p1",
    MODIFIED,
  );

  it("shows placeholder events for each placement, kept in UTC", () => {
    const blocks = PLACE_TIME_EVENTS.applyOptimistic(
      selectTimePlanEntities(createTimePlanStore()),
      members,
    ).timeEventBlocks;

    expect(Object.values(blocks)).toEqual([
      expect.objectContaining({
        ref_id: "p1:0",
        owner: "TimePlanActivity:std:21",
        start_date: "2026-09-15",
        start_time_in_day: "07:30",
        duration_mins: 15,
      }),
      expect.objectContaining({
        ref_id: "p1:1",
        owner: "TimePlanActivity:std:22",
        duration_mins: 45,
      }),
    ]);
  });

  it("posts several placements the way the route reads them", () => {
    expect(PLACE_TIME_EVENTS.toFormFields(members)).toMatchObject({
      timePlanActivityRefId: "21",
      extraPlacements: JSON.stringify(members.placements),
    });
    expect(
      PLACE_TIME_EVENTS.toFormFields(
        placeTimeEventsArgsFromCalendar(DROP, "p1", MODIFIED),
      ),
    ).toMatchObject({
      timePlanActivityRefId: "20",
      durationMins: "30",
      extraPlacements: "",
    });
  });

  it("merges back the events the server made", () => {
    const made = [{ ref_id: "40" } as TimeEventInDayBlock];

    expect(PLACE_TIME_EVENTS.toDelta({ new_time_events: made })).toEqual({
      timeEventBlocks: made,
    });
  });
});
