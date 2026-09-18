import {
  TimePlanActivityFeasability,
  TimePlanActivityKind,
} from "@jupiter/webapi-client";
import type { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { z } from "zod";
import { parseForm } from "zodix";
import { noErrorSomeData } from "@jupiter/core/infra/action-result";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";

import { getLoggedInApiClient } from "~/api-clients.server";

// Changes what a time plan activity asks for, and how much it's needed,
// returning the updated activity for the time plan view to merge in.
const UpdateActivityFormSchema = z.object({
  refId: z.string(),
  kind: z.nativeEnum(TimePlanActivityKind),
  feasability: z.nativeEnum(TimePlanActivityFeasability),
});

export async function action({ request }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const form = await parseForm(request, UpdateActivityFormSchema);

  try {
    const result = await apiClient.timePlans.timePlanActivityUpdate({
      ref_id: form.refId,
      kind: {
        should_change: true,
        value: form.kind,
      },
      feasability: {
        should_change: true,
        value: form.feasability,
      },
    });

    return json(
      noErrorSomeData({
        updated_time_plan_activity: result.updated_time_plan_activity,
      }),
    );
  } catch (error) {
    return handleActionApiError(error);
  }
}
