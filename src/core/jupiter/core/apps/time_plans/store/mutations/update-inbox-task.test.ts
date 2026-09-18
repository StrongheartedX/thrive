import type { BigPlanStats, InboxTask } from "@jupiter/webapi-client";
import { Difficulty, Eisen, InboxTaskStatus } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  UPDATE_INBOX_TASK,
  updateInboxTaskArgsFromForm,
} from "#/core/apps/time_plans/store/mutations/update-inbox-task";
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
    name: "Stored name",
    owner: "TodoTask:std:700",
    status: InboxTaskStatus.NOT_STARTED,
    is_key: false,
    eisen: Eisen.REGULAR,
    difficulty: Difficulty.EASY,
    actionable_date: "2026-09-01",
    due_date: "2026-09-04",
    last_modified_time: "2026-09-01T00:00:00Z",
    ...fields,
  } as InboxTask;
}

function editorForm(fields: Record<string, string>): FormData {
  const formData = new FormData();
  const values = {
    RefId: "100",
    Namespace: "TodoTask:std",
    Name: "Edited name",
    Status: InboxTaskStatus.NOT_STARTED,
    Eisen: Eisen.IMPORTANT,
    Difficulty: Difficulty.HARD,
    ActionableDate: "2026-09-10",
    DueDate: "",
    ...fields,
  };
  for (const [name, value] of Object.entries(values)) {
    formData.set(`targetInboxTask${name}`, value);
  }
  return formData;
}

describe("updateInboxTaskArgsFromForm", () => {
  it("takes the edited fields and the status the intent leads to", () => {
    const formData = editorForm({ IsKey: "on" });

    const args = updateInboxTaskArgsFromForm(
      "mark-done",
      formData,
      inboxTask(),
      "2026-09-14",
      MODIFIED,
      "targetInboxTask",
    );

    expect(args).toEqual({
      refId: "100",
      namespace: "TodoTask:std",
      name: "Edited name",
      status: InboxTaskStatus.DONE,
      isKey: true,
      eisen: Eisen.IMPORTANT,
      difficulty: Difficulty.HARD,
      actionableDate: "2026-09-10",
      dueDate: null,
      modifiedTime: MODIFIED,
    });
  });

  it("only moves the dates when putting the task off", () => {
    const args = updateInboxTaskArgsFromForm(
      "delay-1-day",
      editorForm({}),
      inboxTask(),
      "2026-09-14",
      MODIFIED,
      "targetInboxTask",
    );

    expect(args).toMatchObject({
      name: "Stored name",
      status: InboxTaskStatus.NOT_STARTED,
      eisen: Eisen.REGULAR,
      actionableDate: "2026-09-15",
      dueDate: "2026-09-18",
    });
  });
});

describe("UPDATE_INBOX_TASK", () => {
  const args = {
    refId: "100",
    namespace: "Habit:std",
    name: "Edited name",
    status: InboxTaskStatus.DONE,
    isKey: true,
    eisen: Eisen.IMPORTANT,
    difficulty: Difficulty.HARD,
    actionableDate: null,
    dueDate: "2026-09-20",
    modifiedTime: MODIFIED,
  };

  it("leaves a generated task's core fields alone", () => {
    const entities = selectTimePlanEntities(
      seedTimePlanSource(createTimePlanStore(), "plan", {
        inboxTasks: [inboxTask({ owner: "Habit:std:400" })],
      }),
    );

    const updated = UPDATE_INBOX_TASK.applyOptimistic(entities, args)
      .inboxTasks["100"];

    expect(updated).toMatchObject({
      name: "Stored name",
      eisen: Eisen.REGULAR,
      status: InboxTaskStatus.DONE,
      actionable_date: null,
      due_date: "2026-09-20",
      last_modified_time: MODIFIED,
    });
  });

  it("sends the key flag the way a checkbox does", () => {
    expect(UPDATE_INBOX_TASK.toFormFields(args).isKey).toBe("on");
    expect(
      UPDATE_INBOX_TASK.toFormFields({ ...args, isKey: false }),
    ).not.toHaveProperty("isKey");
  });

  it("merges back the task and its big plan's stats", () => {
    const stats = { big_plan_ref_id: "500" } as BigPlanStats;
    const task = inboxTask({ version: 2 });

    expect(
      UPDATE_INBOX_TASK.toDelta({
        updated_inbox_task: task,
        updated_big_plan_stats: stats,
      }),
    ).toEqual({ inboxTasks: [task], bigPlanStats: [stats] });
  });
});
