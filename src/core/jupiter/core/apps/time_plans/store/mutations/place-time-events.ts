/**
 * Putting a time plan activity on the calendar: dropping it there, or making
 * an event for it from its panel.
 *
 * A habit stack's event lands on each of its member activities, so one edit
 * can make several events.
 */
import type {
  ADate,
  TimeEventInDayBlock,
  TimeInDay,
} from "@jupiter/webapi-client";
import { z } from "zod";

import type { TimePlanMutation } from "#/core/apps/time_plans/store/mutation";
import type { CalendarPlaceFields } from "#/core/calendar/component/event-drag";
import { CALENDAR_PLACE_ACTIVITY_ACTION } from "#/core/calendar/component/event-drag";
import { entityLinkStd } from "#/core/common/entity-link";
import {
  parseTimeEventBufferMins,
  timeEventInDayBlockParamsToUtc,
} from "#/core/common/sub/time_events/time-event";

export interface TimeEventPlacement {
  activityRefId: string;
  durationMins: number;
}

export interface PlaceTimeEventsArgs {
  placements: TimeEventPlacement[];
  // In the user's timezone.
  startDate: string;
  startTimeInDay: string;
  userTimezone: string;
  // As an editor posts them; empty means no buffer.
  bufferBeforeMins: string;
  bufferAfterMins: string;
  // Stands in for the new events' ref ids until the server's arrive.
  placeholderRefId: string;
  modifiedTime: string;
}

const PlacementsSchema = z.array(
  z.object({ activityRefId: z.string(), durationMins: z.number() }),
);

/** The args for an activity dropped on the calendar. */
export function placeTimeEventsArgsFromCalendar(
  fields: CalendarPlaceFields,
  placeholderRefId: string,
  modifiedTime: string,
): PlaceTimeEventsArgs {
  const extraPlacements = fields.extraPlacements
    ? PlacementsSchema.parse(JSON.parse(fields.extraPlacements))
    : [];
  return {
    placements:
      extraPlacements.length > 0
        ? extraPlacements
        : [
            {
              activityRefId: fields.timePlanActivityRefId,
              durationMins: parseInt(fields.durationMins, 10),
            },
          ],
    startDate: fields.startDate,
    startTimeInDay: fields.startTimeInDay,
    userTimezone: fields.userTimezone,
    bufferBeforeMins: "",
    bufferAfterMins: "",
    placeholderRefId,
    modifiedTime,
  };
}

export const PLACE_TIME_EVENTS: TimePlanMutation<
  PlaceTimeEventsArgs,
  { new_time_events: TimeEventInDayBlock[] }
> = {
  action: CALENDAR_PLACE_ACTIVITY_ACTION,
  toFormFields: (args) => ({
    timePlanActivityRefId: args.placements[0]?.activityRefId ?? "",
    startDate: args.startDate,
    startTimeInDay: args.startTimeInDay,
    durationMins: String(args.placements[0]?.durationMins ?? 0),
    // The route places these instead of the single activity when there are
    // any.
    extraPlacements:
      args.placements.length > 1 ? JSON.stringify(args.placements) : "",
    userTimezone: args.userTimezone,
    bufferBeforeMins: args.bufferBeforeMins,
    bufferAfterMins: args.bufferAfterMins,
  }),
  applyOptimistic: (entities, args) => {
    if (!args.startTimeInDay) {
      return entities;
    }
    // The calendar works in the user's timezone; blocks are kept in UTC.
    const { startDate, startTimeInDay } = timeEventInDayBlockParamsToUtc(
      { startDate: args.startDate, startTimeInDay: args.startTimeInDay },
      args.userTimezone,
    );
    const placeholders: Record<string, TimeEventInDayBlock> = {};
    args.placements.forEach((placement, index) => {
      const refId = `${args.placeholderRefId}:${index}`;
      placeholders[refId] = {
        ref_id: refId,
        version: 0,
        archived: false,
        created_time: args.modifiedTime,
        last_modified_time: args.modifiedTime,
        name: "",
        time_event_domain_ref_id: "",
        owner: entityLinkStd("TimePlanActivity", placement.activityRefId),
        start_date: startDate as ADate,
        start_time_in_day: startTimeInDay as TimeInDay,
        duration_mins: placement.durationMins,
        buffer_before_mins:
          parseTimeEventBufferMins(args.bufferBeforeMins || undefined) ?? null,
        buffer_after_mins:
          parseTimeEventBufferMins(args.bufferAfterMins || undefined) ?? null,
      } as TimeEventInDayBlock;
    });
    return {
      ...entities,
      timeEventBlocks: { ...entities.timeEventBlocks, ...placeholders },
    };
  },
  toDelta: (result) => ({ timeEventBlocks: result.new_time_events }),
};
