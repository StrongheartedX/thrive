import type { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { z } from "zod";
import { parseForm } from "zodix";
import { noErrorSomeData } from "@jupiter/core/infra/action-result";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";

import { getLoggedInApiClient } from "~/api-clients.server";

// Removes a time plan activity, and returns the ref ids of it and the
// activities removed with it, for the time plan view to drop.
const RemoveActivityFormSchema = z.object({
  refId: z.string(),
});

export async function action({ request }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const form = await parseForm(request, RemoveActivityFormSchema);

  try {
    const result = await apiClient.timePlans.timePlanActivityRemove({
      ref_id: form.refId,
    });

    return json(
      noErrorSomeData({
        removed_time_plan_activity_ref_ids:
          result.removed_time_plan_activity_ref_ids,
      }),
    );
  } catch (error) {
    return handleActionApiError(error);
  }
}
