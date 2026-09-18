import type { TimeEventInDayBlock } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  ARCHIVE_TIME_EVENT,
  UPDATE_TIME_EVENT,
  archiveTimeEventArgsFromForm,
  updateTimeEventArgsFromForm,
} from "#/core/apps/time_plans/store/mutations/time-event";
import {
  createTimePlanStore,
  seedTimePlanSource,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

const MODIFIED = "2026-09-14T10:00:00Z";

function entities() {
  return selectTimePlanEntities(
    seedTimePlanSource(createTimePlanStore(), "activity", {
      timeEventBlocks: [
        {
          ref_id: "30",
          version: 1,
          archived: false,
          start_date: "2026-09-14",
          start_time_in_day: "08:00",
          duration_mins: 30,
          buffer_before_mins: 5,
          buffer_after_mins: null,
        } as TimeEventInDayBlock,
      ],
    }),
  );
}

function editorForm(fields: Record<string, string> = {}): FormData {
  const formData = new FormData();
  const values = {
    timeEventRefId: "30",
    userTimezone: "Europe/Bucharest",
    startDate: "2026-09-15",
    startTimeInDay: "09:15",
    durationMins: "45",
    bufferBeforeMins: "",
    bufferAfterMins: "10",
    ...fields,
  };
  for (const [name, value] of Object.entries(values)) {
    formData.set(name, value);
  }
  return formData;
}

describe("UPDATE_TIME_EVENT", () => {
  it("saves the editor's times, kept in UTC", () => {
    const args = updateTimeEventArgsFromForm(editorForm(), MODIFIED);
    const updated = UPDATE_TIME_EVENT.applyOptimistic(entities(), args)
      .timeEventBlocks["30"];

    expect(updated).toMatchObject({
      start_date: "2026-09-15",
      start_time_in_day: "06:15",
      duration_mins: 45,
      buffer_before_mins: null,
      buffer_after_mins: 10,
      last_modified_time: MODIFIED,
    });
  });

  it("posts back what the editor had", () => {
    const args = updateTimeEventArgsFromForm(editorForm(), MODIFIED);

    expect(UPDATE_TIME_EVENT.toFormFields(args)).toEqual({
      timeEventRefId: "30",
      userTimezone: "Europe/Bucharest",
      startDate: "2026-09-15",
      startTimeInDay: "09:15",
      durationMins: "45",
      bufferBeforeMins: "",
      bufferAfterMins: "10",
    });
  });

  it("shows nothing until the server has turned down an event without a time", () => {
    const args = updateTimeEventArgsFromForm(
      editorForm({ startTimeInDay: "" }),
      MODIFIED,
    );

    expect(
      UPDATE_TIME_EVENT.applyOptimistic(entities(), args).timeEventBlocks["30"]
        .start_time_in_day,
    ).toBe("08:00");
  });
});

describe("ARCHIVE_TIME_EVENT", () => {
  it("archives the editor's event right away", () => {
    const args = archiveTimeEventArgsFromForm(editorForm(), MODIFIED);

    expect(
      ARCHIVE_TIME_EVENT.applyOptimistic(entities(), args).timeEventBlocks[
        "30"
      ],
    ).toMatchObject({ archived: true, archived_time: MODIFIED });
  });
});
