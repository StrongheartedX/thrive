/**
 * Editing or removing an activity's time event from the time plan view.
 */
import type {
  ADate,
  TimeEventInDayBlock,
  TimeEventInDayBlockArchiveResult,
  TimeEventInDayBlockUpdateResult,
  TimeInDay,
} from "@jupiter/webapi-client";
import { z } from "zod";

import type { TimePlanMutation } from "#/core/apps/time_plans/store/mutation";
import { editorFormFields } from "#/core/apps/time_plans/store/mutations/form";
import {
  parseTimeEventBufferMins,
  timeEventInDayBlockParamsToUtc,
} from "#/core/common/sub/time_events/time-event";

export interface UpdateTimeEventArgs {
  refId: string;
  userTimezone: string;
  // In the user's timezone, as the editor shows them.
  startDate: string;
  startTimeInDay: string;
  durationMins: number;
  // As the editor posts them; empty means no buffer.
  bufferBeforeMins: string;
  bufferAfterMins: string;
  // When the edit was made, standing in for the server's modification time
  // until the result arrives.
  modifiedTime: string;
}

const TimeEventPropertiesFormSchema = z.object({
  timeEventRefId: z.string(),
  userTimezone: z.string(),
  startDate: z.string(),
  durationMins: z.string().transform((v) => parseInt(v, 10)),
});

/** The args from a time event in day block properties editor's form. */
export function updateTimeEventArgsFromForm(
  formData: FormData,
  modifiedTime: string,
): UpdateTimeEventArgs {
  const field = editorFormFields(formData, "");
  const form = TimeEventPropertiesFormSchema.parse({
    timeEventRefId: field("timeEventRefId"),
    userTimezone: field("userTimezone"),
    startDate: field("startDate"),
    durationMins: field("durationMins"),
  });

  return {
    refId: form.timeEventRefId,
    userTimezone: form.userTimezone,
    startDate: form.startDate,
    startTimeInDay: field("startTimeInDay") ?? "",
    durationMins: form.durationMins,
    bufferBeforeMins: field("bufferBeforeMins") ?? "",
    bufferAfterMins: field("bufferAfterMins") ?? "",
    modifiedTime,
  };
}

export const UPDATE_TIME_EVENT: TimePlanMutation<
  UpdateTimeEventArgs,
  Pick<TimeEventInDayBlockUpdateResult, "updated_time_event_in_day_block">
> = {
  action: "/app/workspace/apps/time-plans/mutations/update-time-event",
  toFormFields: (args) => ({
    timeEventRefId: args.refId,
    userTimezone: args.userTimezone,
    startDate: args.startDate,
    startTimeInDay: args.startTimeInDay,
    durationMins: String(args.durationMins),
    bufferBeforeMins: args.bufferBeforeMins,
    bufferAfterMins: args.bufferAfterMins,
  }),
  applyOptimistic: (entities, args) => {
    const block = entities.timeEventBlocks[args.refId];
    if (block === undefined || !args.startTimeInDay) {
      // Without a time the server turns the edit down, so there's nothing
      // to show in the meantime.
      return entities;
    }
    const { startDate, startTimeInDay } = timeEventInDayBlockParamsToUtc(
      { startDate: args.startDate, startTimeInDay: args.startTimeInDay },
      args.userTimezone,
    );
    const updated: TimeEventInDayBlock = {
      ...block,
      start_date: startDate as ADate,
      start_time_in_day: startTimeInDay as TimeInDay,
      duration_mins: Number.isNaN(args.durationMins)
        ? block.duration_mins
        : args.durationMins,
      buffer_before_mins:
        parseTimeEventBufferMins(args.bufferBeforeMins || undefined) ?? null,
      buffer_after_mins:
        parseTimeEventBufferMins(args.bufferAfterMins || undefined) ?? null,
      last_modified_time: args.modifiedTime,
    };
    return {
      ...entities,
      timeEventBlocks: { ...entities.timeEventBlocks, [args.refId]: updated },
    };
  },
  toDelta: (result) => ({
    timeEventBlocks: [result.updated_time_event_in_day_block],
  }),
};

export interface ArchiveTimeEventArgs {
  refId: string;
  // When the edit was made, standing in for the server's archival time until
  // the result arrives.
  modifiedTime: string;
}

/** The args for removing the event a time event editor shows. */
export function archiveTimeEventArgsFromForm(
  formData: FormData,
  modifiedTime: string,
): ArchiveTimeEventArgs {
  return {
    refId: z.string().parse(formData.get("timeEventRefId")),
    modifiedTime,
  };
}

export const ARCHIVE_TIME_EVENT: TimePlanMutation<
  ArchiveTimeEventArgs,
  Pick<TimeEventInDayBlockArchiveResult, "archived_time_event_in_day_block">
> = {
  action: "/app/workspace/apps/time-plans/mutations/archive-time-event",
  toFormFields: (args) => ({ timeEventRefId: args.refId }),
  applyOptimistic: (entities, args) => {
    const block = entities.timeEventBlocks[args.refId];
    if (block === undefined) {
      return entities;
    }
    const updated: TimeEventInDayBlock = {
      ...block,
      archived: true,
      archived_time: args.modifiedTime,
      last_modified_time: args.modifiedTime,
    };
    return {
      ...entities,
      timeEventBlocks: { ...entities.timeEventBlocks, [args.refId]: updated },
    };
  },
  toDelta: (result) => ({
    timeEventBlocks: [result.archived_time_event_in_day_block],
  }),
};
