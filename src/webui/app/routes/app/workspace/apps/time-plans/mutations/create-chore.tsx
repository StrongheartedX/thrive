import type { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { z } from "zod";
import { parseForm } from "zodix";
import {
  ChoreCreateFormSchema,
  choreCreateArgs,
} from "@jupiter/core/apps/chores/create-form";
import { noErrorSomeData } from "@jupiter/core/infra/action-result";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";

import { getLoggedInApiClient } from "~/api-clients.server";

// Creates a chore along with its activity in a time plan, from the plan's own
// creation form, and returns both for the view to merge in.
const CreateFormSchema = ChoreCreateFormSchema.extend({
  timePlanRefId: z.string(),
});

export async function action({ request }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const form = await parseForm(request, CreateFormSchema);

  try {
    const result = await apiClient.chores.choreCreate(
      choreCreateArgs(form, form.timePlanRefId),
    );

    return json(
      noErrorSomeData({
        new_chore: result.new_chore,
        new_time_plan_activity: result.new_time_plan_activity ?? null,
      }),
    );
  } catch (error) {
    return handleActionApiError(error);
  }
}
