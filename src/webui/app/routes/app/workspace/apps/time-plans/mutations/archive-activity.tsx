import type { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { z } from "zod";
import { parseForm } from "zodix";
import { noErrorSomeData } from "@jupiter/core/infra/action-result";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";

import { getLoggedInApiClient } from "~/api-clients.server";

// Archives a time plan activity, and returns it along with the activities
// archived with it, for the time plan view to merge in.
const ArchiveActivityFormSchema = z.object({
  refId: z.string(),
});

export async function action({ request }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const form = await parseForm(request, ArchiveActivityFormSchema);

  try {
    const result = await apiClient.timePlans.timePlanActivityArchive({
      ref_id: form.refId,
    });

    return json(
      noErrorSomeData({
        archived_time_plan_activities: result.archived_time_plan_activities,
      }),
    );
  } catch (error) {
    return handleActionApiError(error);
  }
}
