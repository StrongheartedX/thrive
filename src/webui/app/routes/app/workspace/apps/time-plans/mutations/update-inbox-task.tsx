import { Difficulty, Eisen, InboxTaskStatus } from "@jupiter/webapi-client";
import type { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { z } from "zod";
import { CheckboxAsString, parseForm } from "zodix";
import { isInboxTaskCoreFieldEditable } from "@jupiter/core/common/sub/inbox_tasks/root";
import { noErrorSomeData } from "@jupiter/core/infra/action-result";
import { saveScoreAction } from "@jupiter/core/gamification/scores.server";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";

import { getLoggedInApiClient } from "~/api-clients.server";

// Saves an inbox task as edited from the time plan view. The view works out
// the status and dates an intent leads to, so this just stores them, and
// returns what changed for the view to merge in.
const UpdateInboxTaskFormSchema = z.object({
  refId: z.string(),
  namespace: z.string(),
  name: z.string(),
  status: z.nativeEnum(InboxTaskStatus),
  isKey: CheckboxAsString,
  eisen: z.nativeEnum(Eisen),
  difficulty: z.nativeEnum(Difficulty),
  actionableDate: z.string().optional(),
  dueDate: z.string().optional(),
});

export async function action({ request }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const form = await parseForm(request, UpdateInboxTaskFormSchema);
  // Generated tasks take these from whatever generates them.
  const corePropertyEditable = isInboxTaskCoreFieldEditable(form.namespace);

  try {
    const result = await apiClient.inboxTasks.inboxTaskUpdate({
      ref_id: form.refId,
      name: corePropertyEditable
        ? { should_change: true, value: form.name }
        : { should_change: false },
      status: { should_change: true, value: form.status },
      is_key: corePropertyEditable
        ? { should_change: true, value: form.isKey }
        : { should_change: false },
      eisen: corePropertyEditable
        ? { should_change: true, value: form.eisen }
        : { should_change: false },
      difficulty: corePropertyEditable
        ? { should_change: true, value: form.difficulty }
        : { should_change: false },
      actionable_date: {
        should_change: true,
        value: form.actionableDate ? form.actionableDate : undefined,
      },
      due_date: {
        should_change: true,
        value: form.dueDate ? form.dueDate : undefined,
      },
    });

    const data = noErrorSomeData({
      updated_inbox_task: result.updated_inbox_task,
      updated_big_plan_stats: result.updated_big_plan_stats ?? null,
    });

    if (result.record_score_result) {
      return json(data, {
        headers: {
          "Set-Cookie": await saveScoreAction(result.record_score_result),
        },
      });
    }

    return json(data);
  } catch (error) {
    return handleActionApiError(error);
  }
}
