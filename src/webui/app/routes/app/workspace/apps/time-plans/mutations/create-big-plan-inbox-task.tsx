import type { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { z } from "zod";
import { parseForm } from "zodix";
import {
  BigPlanInboxTaskCreateFormSchema,
  bigPlanInboxTaskCreateArgs,
} from "@jupiter/core/apps/big_plans/create-form";
import { noErrorSomeData } from "@jupiter/core/infra/action-result";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";

import { getLoggedInApiClient } from "~/api-clients.server";

// Creates an inbox task for a big plan along with its activity in a time plan,
// from the plan's own creation form, and returns both for the view to merge in.
const CreateFormSchema = BigPlanInboxTaskCreateFormSchema.extend({
  timePlanRefId: z.string(),
  bigPlanRefId: z.string(),
});

export async function action({ request }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const form = await parseForm(request, CreateFormSchema);

  try {
    const result = await apiClient.bigPlans.bigPlanCreateInboxTask(
      bigPlanInboxTaskCreateArgs(form, form.bigPlanRefId, form.timePlanRefId),
    );

    return json(
      noErrorSomeData({
        new_inbox_task: result.new_inbox_task,
        new_time_plan_activity: result.new_time_plan_activity ?? null,
        new_big_plan_time_plan_activity:
          result.new_big_plan_time_plan_activity ?? null,
        updated_big_plan_stats: result.updated_big_plan_stats ?? null,
      }),
    );
  } catch (error) {
    return handleActionApiError(error);
  }
}
