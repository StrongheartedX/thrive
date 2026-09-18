/**
 * Moving or stretching an event on the time plan view's calendar.
 */
import type {
  ADate,
  TimeEventInDayBlock,
  TimeEventInDayBlockUpdateResult,
  TimeInDay,
} from "@jupiter/webapi-client";

import type { TimePlanMutation } from "#/core/apps/time_plans/store/mutation";
import type { CalendarRescheduleFields } from "#/core/calendar/component/event-drag";
import { CALENDAR_RESCHEDULE_ACTION } from "#/core/calendar/component/event-drag";
import { timeEventInDayBlockParamsToUtc } from "#/core/common/sub/time_events/time-event";

export interface RescheduleCalendarEventArgs extends CalendarRescheduleFields {
  // When the edit was made, standing in for the server's modification time
  // until the result arrives.
  modifiedTime: string;
}

export const RESCHEDULE_CALENDAR_EVENT: TimePlanMutation<
  RescheduleCalendarEventArgs,
  Pick<TimeEventInDayBlockUpdateResult, "updated_time_event_in_day_block">
> = {
  action: CALENDAR_RESCHEDULE_ACTION,
  toFormFields: (args) => ({
    kind: args.kind,
    refId: args.refId,
    blockRefId: args.blockRefId,
    startDate: args.startDate,
    startTimeInDay: args.startTimeInDay,
    ...(args.durationMins !== undefined
      ? { durationMins: args.durationMins }
      : {}),
    userTimezone: args.userTimezone,
  }),
  applyOptimistic: (entities, args) => {
    const block = entities.timeEventBlocks[args.blockRefId];
    if (block === undefined) {
      return entities;
    }
    // The calendar works in the user's timezone; blocks are kept in UTC.
    const { startDate, startTimeInDay } = timeEventInDayBlockParamsToUtc(
      { startDate: args.startDate, startTimeInDay: args.startTimeInDay },
      args.userTimezone,
    );
    const durationMins =
      args.durationMins === undefined ? NaN : parseInt(args.durationMins, 10);
    const updated: TimeEventInDayBlock = {
      ...block,
      start_date: startDate as ADate,
      start_time_in_day: (startTimeInDay ??
        block.start_time_in_day) as TimeInDay,
      duration_mins: Number.isNaN(durationMins)
        ? block.duration_mins
        : durationMins,
      last_modified_time: args.modifiedTime,
    };
    return {
      ...entities,
      timeEventBlocks: {
        ...entities.timeEventBlocks,
        [args.blockRefId]: updated,
      },
    };
  },
  toDelta: (result) => ({
    timeEventBlocks: [result.updated_time_event_in_day_block],
  }),
};
