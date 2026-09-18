import type { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { z } from "zod";
import { parseForm } from "zodix";
import { noErrorNoData } from "@jupiter/core/infra/action-result";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";

import { getLoggedInApiClient } from "~/api-clients.server";

// Regenerates a habit's inbox tasks. It returns nothing to merge: the time plan
// view reloads afterwards, since regen can touch any of the habit's tasks.
const RegenHabitFormSchema = z.object({
  refId: z.string(),
});

export async function action({ request }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const form = await parseForm(request, RegenHabitFormSchema);

  try {
    await apiClient.habits.habitRegen({
      ref_id: form.refId,
    });

    return json(noErrorNoData());
  } catch (error) {
    return handleActionApiError(error);
  }
}
