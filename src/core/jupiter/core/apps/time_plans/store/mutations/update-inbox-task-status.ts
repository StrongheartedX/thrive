/**
 * Moving an inbox task to another status (and maybe eisen) from the time plan
 * view: dragging it on the kanban, or marking a card done or not done.
 */
import type {
  BigPlanStats,
  InboxTask,
  InboxTaskUpdateResult,
} from "@jupiter/webapi-client";
import { Eisen, InboxTaskStatus } from "@jupiter/webapi-client";
import { z } from "zod";

import type { TimePlanMutation } from "#/core/apps/time_plans/store/mutation";
import { parentLinkNamespaceFromEntityLinkWire } from "#/core/common/sub/inbox_tasks/parent-link-namespace";
import { isInboxTaskCoreFieldEditable } from "#/core/common/sub/inbox_tasks/root";

export interface UpdateInboxTaskStatusArgs {
  refId: string;
  status: InboxTaskStatus;
  // Left alone when null.
  eisen: Eisen | null;
  // When the edit was made, standing in for the server's modification time
  // until the result arrives ("make progress" doneness looks at it).
  modifiedTime: string;
}

// Kanban columns are `inbox-tasks-column:<eisen>:<status>[:<group>]`, with an
// eisen of "undefined" on boards that don't split by it.
const KanbanColumnSchema = z
  .tuple([
    z.string(),
    z.nativeEnum(Eisen).or(z.literal("undefined").transform(() => undefined)),
    z.nativeEnum(InboxTaskStatus),
  ])
  .rest(z.string());

/**
 * The args for dropping ``inboxTask`` on the kanban column ``droppableId``.
 *
 * Generated tasks take their eisen from whatever generates them, so they can't
 * move to another eisen's board: that gives null. Their status still changes.
 */
export function inboxTaskKanbanMoveArgs(
  inboxTask: InboxTask,
  droppableId: string,
  modifiedTime: string,
): UpdateInboxTaskStatusArgs | null {
  const [, eisen, status] = KanbanColumnSchema.parse(droppableId.split(":"));
  const coreFieldEditable = isInboxTaskCoreFieldEditable(
    parentLinkNamespaceFromEntityLinkWire(inboxTask.owner),
  );

  if (!coreFieldEditable && eisen !== undefined && eisen !== inboxTask.eisen) {
    return null;
  }

  return {
    refId: inboxTask.ref_id,
    status,
    eisen: coreFieldEditable ? (eisen ?? null) : null,
    modifiedTime,
  };
}

export const UPDATE_INBOX_TASK_STATUS: TimePlanMutation<
  UpdateInboxTaskStatusArgs,
  Pick<InboxTaskUpdateResult, "updated_inbox_task"> & {
    updated_big_plan_stats: BigPlanStats | null;
  }
> = {
  action: "/app/workspace/core/inbox-tasks/update-status-and-eisen",
  toFormFields: (args) => ({
    id: args.refId,
    status: args.status,
    eisen: args.eisen ?? "no-go",
  }),
  applyOptimistic: (entities, args) => {
    const inboxTask = entities.inboxTasks[args.refId];
    if (inboxTask === undefined) {
      return entities;
    }
    const updated: InboxTask = {
      ...inboxTask,
      status: args.status,
      eisen: args.eisen ?? inboxTask.eisen,
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
