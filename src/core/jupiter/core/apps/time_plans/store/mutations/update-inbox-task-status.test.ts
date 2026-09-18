import type { BigPlanStats, InboxTask } from "@jupiter/webapi-client";
import { Difficulty, Eisen, InboxTaskStatus } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  UPDATE_INBOX_TASK_STATUS,
  inboxTaskKanbanMoveArgs,
} from "#/core/apps/time_plans/store/mutations/update-inbox-task-status";
import {
  createTimePlanStore,
  seedTimePlanSource,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

const MODIFIED = "2026-09-14T10:00:00Z";

function inboxTask(fields: Partial<InboxTask> = {}): InboxTask {
  return {
    ref_id: "100",
    version: 1,
    archived: false,
    name: "The task",
    owner: "TodoTask:std:700",
    status: InboxTaskStatus.NOT_STARTED,
    is_key: false,
    eisen: Eisen.REGULAR,
    difficulty: Difficulty.EASY,
    last_modified_time: "2026-09-01T00:00:00Z",
    ...fields,
  } as InboxTask;
}

describe("inboxTaskKanbanMoveArgs", () => {
  it("moves a task to the column's status and eisen", () => {
    expect(
      inboxTaskKanbanMoveArgs(
        inboxTask(),
        `inbox-tasks-column:${Eisen.IMPORTANT}:${InboxTaskStatus.IN_PROGRESS}`,
        MODIFIED,
      ),
    ).toEqual({
      refId: "100",
      status: InboxTaskStatus.IN_PROGRESS,
      eisen: Eisen.IMPORTANT,
      modifiedTime: MODIFIED,
    });
  });

  it("leaves the eisen alone on boards that don't split by it", () => {
    expect(
      inboxTaskKanbanMoveArgs(
        inboxTask(),
        `inbox-tasks-column:undefined:${InboxTaskStatus.DONE}:group-1`,
        MODIFIED,
      ),
    ).toMatchObject({ status: InboxTaskStatus.DONE, eisen: null });
  });

  it("keeps generated tasks on their own eisen's board", () => {
    const generated = inboxTask({ owner: "Habit:std:400" });

    expect(
      inboxTaskKanbanMoveArgs(
        generated,
        `inbox-tasks-column:${Eisen.IMPORTANT}:${InboxTaskStatus.DONE}`,
        MODIFIED,
      ),
    ).toBeNull();
    expect(
      inboxTaskKanbanMoveArgs(
        generated,
        `inbox-tasks-column:${Eisen.REGULAR}:${InboxTaskStatus.DONE}`,
        MODIFIED,
      ),
    ).toMatchObject({ status: InboxTaskStatus.DONE, eisen: null });
  });
});

describe("UPDATE_INBOX_TASK_STATUS", () => {
  it("patches the status, and the eisen only when one is given", () => {
    const entities = selectTimePlanEntities(
      seedTimePlanSource(createTimePlanStore(), "plan", {
        inboxTasks: [inboxTask()],
      }),
    );

    expect(
      UPDATE_INBOX_TASK_STATUS.applyOptimistic(entities, {
        refId: "100",
        status: InboxTaskStatus.BLOCKED,
        eisen: null,
        modifiedTime: MODIFIED,
      }).inboxTasks["100"],
    ).toMatchObject({
      status: InboxTaskStatus.BLOCKED,
      eisen: Eisen.REGULAR,
      last_modified_time: MODIFIED,
    });
    expect(
      UPDATE_INBOX_TASK_STATUS.applyOptimistic(entities, {
        refId: "100",
        status: InboxTaskStatus.BLOCKED,
        eisen: Eisen.URGENT,
        modifiedTime: MODIFIED,
      }).inboxTasks["100"].eisen,
    ).toBe(Eisen.URGENT);
  });

  it("posts what the update-status-and-eisen route reads", () => {
    expect(
      UPDATE_INBOX_TASK_STATUS.toFormFields({
        refId: "100",
        status: InboxTaskStatus.DONE,
        eisen: null,
        modifiedTime: MODIFIED,
      }),
    ).toEqual({ id: "100", status: InboxTaskStatus.DONE, eisen: "no-go" });
  });

  it("merges back the task and its big plan's stats", () => {
    const task = inboxTask({ version: 2 });
    const stats = { big_plan_ref_id: "500" } as BigPlanStats;

    expect(
      UPDATE_INBOX_TASK_STATUS.toDelta({
        updated_inbox_task: task,
        updated_big_plan_stats: stats,
      }),
    ).toEqual({ inboxTasks: [task], bigPlanStats: [stats] });
  });
});
