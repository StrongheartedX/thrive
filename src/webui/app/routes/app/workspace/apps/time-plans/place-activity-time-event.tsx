import type { TimeEventInDayBlock } from "@jupiter/webapi-client";
import type { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { z } from "zod";
import { parseForm } from "zodix";
import { noErrorSomeData } from "@jupiter/core/infra/action-result";
import {
  parseTimeEventBufferMins,
  timeEventInDayBlockParamsToUtc,
} from "@jupiter/core/common/sub/time_events/time-event";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";

import { getLoggedInApiClient } from "~/api-clients.server";

const ExtraPlacementSchema = z.array(
  z.object({
    activityRefId: z.string(),
    durationMins: z.number(),
  }),
);

const PlaceFormSchema = z.object({
  timePlanActivityRefId: z.string(),
  startDate: z.string(),
  startTimeInDay: z.string(),
  durationMins: z.string().transform((v) => parseInt(v, 10)),
  extraPlacements: z.string().optional(),
  userTimezone: z.string(),
  // Events made from a form have buffers; ones dropped on the calendar don't.
  bufferBeforeMins: z.string().optional(),
  bufferAfterMins: z.string().optional(),
});

export async function action({ request }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const form = await parseForm(request, PlaceFormSchema);

  const extraPlacements =
    form.extraPlacements !== undefined && form.extraPlacements !== ""
      ? ExtraPlacementSchema.parse(JSON.parse(form.extraPlacements))
      : [];

  const { startDate, startTimeInDay } = timeEventInDayBlockParamsToUtc(
    { startDate: form.startDate, startTimeInDay: form.startTimeInDay },
    form.userTimezone,
  );
  const placements =
    extraPlacements.length > 0
      ? extraPlacements
      : [
          {
            activityRefId: form.timePlanActivityRefId,
            durationMins: form.durationMins,
          },
        ];

  try {
    // Views that keep their own copy of the entities add these to it.
    const newTimeEvents: TimeEventInDayBlock[] = [];
    for (const placement of placements) {
      const result =
        await apiClient.timeEvents.timeEventInDayBlockCreateForTimePlanActivity(
          {
            time_plan_activity_ref_id: placement.activityRefId,
            start_date: startDate,
            start_time_in_day: startTimeInDay ?? "",
            duration_mins: placement.durationMins,
            buffer_before_mins: parseTimeEventBufferMins(form.bufferBeforeMins),
            buffer_after_mins: parseTimeEventBufferMins(form.bufferAfterMins),
          },
        );
      newTimeEvents.push(result.new_time_event);
    }

    return json(noErrorSomeData({ new_time_events: newTimeEvents }));
  } catch (error) {
    return handleActionApiError(error);
  }
}
