import type { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { z } from "zod";
import { parseForm } from "zodix";
import { noErrorSomeData } from "@jupiter/core/infra/action-result";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";

import { getLoggedInApiClient } from "~/api-clients.server";

// Archives an activity's time event from the time plan view, and returns it
// for the view to merge in.
const ArchiveTimeEventFormSchema = z.object({
  timeEventRefId: z.string(),
});

export async function action({ request }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const form = await parseForm(request, ArchiveTimeEventFormSchema);

  try {
    const result = await apiClient.timeEvents.timeEventInDayBlockArchive({
      ref_id: form.timeEventRefId,
    });

    return json(
      noErrorSomeData({
        archived_time_event_in_day_block:
          result.archived_time_event_in_day_block,
      }),
    );
  } catch (error) {
    return handleActionApiError(error);
  }
}
