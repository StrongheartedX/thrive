/**
 * Saving an inbox task edited from the time plan view.
 */
import type {
  ADate,
  BigPlanStats,
  InboxTask,
  InboxTaskUpdateResult,
} from "@jupiter/webapi-client";
import { Difficulty, Eisen, InboxTaskStatus } from "@jupiter/webapi-client";
import { z } from "zod";

import type { TimePlanMutation } from "#/core/apps/time_plans/store/mutation";
import { editorFormFields } from "#/core/apps/time_plans/store/mutations/form";
import type {
  InboxTaskDelayIntent,
  InboxTaskStatusIntent,
} from "#/core/common/sub/inbox_tasks/intents";
import {
  delayedInboxTaskDates,
  inboxTaskStatusForIntent,
  isInboxTaskDelayIntent,
} from "#/core/common/sub/inbox_tasks/intents";
import { isInboxTaskCoreFieldEditable } from "#/core/common/sub/inbox_tasks/root";

export interface UpdateInboxTaskArgs {
  refId: string;
  // The task's owner namespace; generated tasks can't change their core
  // fields.
  namespace: string;
  name: string;
  status: InboxTaskStatus;
  isKey: boolean;
  eisen: Eisen;
  difficulty: Difficulty;
  actionableDate: ADate | null;
  dueDate: ADate | null;
  // When the edit was made, standing in for the server's modification time
  // until the result arrives ("make progress" doneness looks at it).
  modifiedTime: string;
}

const InboxTaskPropertiesFormSchema = z.object({
  refId: z.string(),
  namespace: z.string(),
  name: z.string(),
  status: z.nativeEnum(InboxTaskStatus),
  eisen: z.nativeEnum(Eisen),
  difficulty: z.nativeEnum(Difficulty),
});

/**
 * The args for ``intent`` from an inbox task properties editor's form.
 *
 * ``namePrefix`` is the editor's. Putting the task off only moves its dates,
 * so everything else comes from ``current``, the task as the view holds it.
 */
export function updateInboxTaskArgsFromForm(
  intent: InboxTaskStatusIntent | InboxTaskDelayIntent,
  formData: FormData,
  current: InboxTask,
  today: ADate,
  modifiedTime: string,
  namePrefix: string,
): UpdateInboxTaskArgs {
  const field = editorFormFields(formData, namePrefix);
  const form = InboxTaskPropertiesFormSchema.parse({
    refId: field("refId"),
    namespace: field("namespace"),
    name: field("name"),
    status: field("status"),
    eisen: field("eisen"),
    difficulty: field("difficulty"),
  });

  if (isInboxTaskDelayIntent(intent)) {
    return {
      refId: current.ref_id,
      namespace: form.namespace,
      name: current.name,
      status: current.status,
      isKey: current.is_key,
      eisen: current.eisen,
      difficulty: current.difficulty,
      ...delayedInboxTaskDates(
        intent,
        today,
        current.actionable_date,
        current.due_date,
      ),
      modifiedTime,
    };
  }

  return {
    refId: form.refId,
    namespace: form.namespace,
    name: form.name,
    status: inboxTaskStatusForIntent(intent, form.status),
    isKey: field("isKey") === "on",
    eisen: form.eisen,
    difficulty: form.difficulty,
    actionableDate: field("actionableDate") || null,
    dueDate: field("dueDate") || null,
    modifiedTime,
  };
}

export const UPDATE_INBOX_TASK: TimePlanMutation<
  UpdateInboxTaskArgs,
  Pick<InboxTaskUpdateResult, "updated_inbox_task"> & {
    updated_big_plan_stats: BigPlanStats | null;
  }
> = {
  action: "/app/workspace/apps/time-plans/mutations/update-inbox-task",
  toFormFields: (args) => ({
    refId: args.refId,
    namespace: args.namespace,
    name: args.name,
    status: args.status,
    ...(args.isKey ? { isKey: "on" } : {}),
    eisen: args.eisen,
    difficulty: args.difficulty,
    actionableDate: args.actionableDate ?? "",
    dueDate: args.dueDate ?? "",
  }),
  applyOptimistic: (entities, args) => {
    const inboxTask = entities.inboxTasks[args.refId];
    if (inboxTask === undefined) {
      return entities;
    }
    const coreFields = isInboxTaskCoreFieldEditable(args.namespace)
      ? {
          name: args.name,
          is_key: args.isKey,
          eisen: args.eisen,
          difficulty: args.difficulty,
        }
      : {};
    const updated: InboxTask = {
      ...inboxTask,
      ...coreFields,
      status: args.status,
      actionable_date: args.actionableDate,
      due_date: args.dueDate,
      last_modified_time: args.modifiedTime,
    };
    return {
      ...entities,
      inboxTasks: { ...entities.inboxTasks, [args.refId]: updated },
    };
  },
  toDelta: (result) => ({
    inboxTasks: [result.updated_inbox_task],
    bigPlanStats: result.updated_big_plan_stats
      ? [result.updated_big_plan_stats]
      : [],
  }),
};
