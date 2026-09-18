import type {
  BigPlanStats,
  InboxTask,
  TimePlanActivity,
  TodoTask,
} from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  CREATE_BIG_PLAN_INBOX_TASK,
  CREATE_TODO_TASK,
  formFieldsFromFormData,
} from "#/core/apps/time_plans/store/mutations/create-entities";
import {
  createTimePlanStore,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

describe("formFieldsFromFormData", () => {
  it("keeps the fields but not the intent", () => {
    const formData = new FormData();
    formData.set("intent", "create");
    formData.set("name", "The todo");
    formData.set("eisen", "regular");

    expect(formFieldsFromFormData(formData)).toEqual({
      name: "The todo",
      eisen: "regular",
    });
  });
});

describe("CREATE_TODO_TASK", () => {
  const args = { timePlanRefId: "9", fields: { name: "The todo" } };

  it("posts the form along with the plan", () => {
    expect(CREATE_TODO_TASK.action).toBe(
      "/app/workspace/apps/time-plans/mutations/create-todo-task",
    );
    expect(CREATE_TODO_TASK.toFormFields(args)).toEqual({
      name: "The todo",
      timePlanRefId: "9",
    });
  });

  it("shows nothing until the server has made it", () => {
    const entities = selectTimePlanEntities(createTimePlanStore());

    expect(CREATE_TODO_TASK.applyOptimistic(entities, args)).toBe(entities);
  });

  it("merges in the todo, its inbox task and its activity", () => {
    const todoTask = { ref_id: "700" } as TodoTask;
    const inboxTask = { ref_id: "100" } as InboxTask;
    const activity = { ref_id: "20" } as TimePlanActivity;

    expect(
      CREATE_TODO_TASK.toDelta({
        new_todo_task: todoTask,
        new_inbox_task: inboxTask,
        new_time_plan_activity: activity,
      }),
    ).toEqual({
      todoTasks: [todoTask],
      inboxTasks: [inboxTask],
      activities: [activity],
    });
  });
});

describe("CREATE_BIG_PLAN_INBOX_TASK", () => {
  it("merges in the task, and activities only when they were made", () => {
    const inboxTask = { ref_id: "100" } as InboxTask;

    expect(
      CREATE_BIG_PLAN_INBOX_TASK.toDelta({
        new_inbox_task: inboxTask,
        new_time_plan_activity: null,
        new_big_plan_time_plan_activity: null,
        updated_big_plan_stats: null,
      }),
    ).toEqual({ inboxTasks: [inboxTask], activities: [], bigPlanStats: [] });
  });

  it("merges in the big plan's new activity and its stats", () => {
    const inboxTask = { ref_id: "100" } as InboxTask;
    const activity = { ref_id: "20" } as TimePlanActivity;
    const bigPlanActivity = { ref_id: "21" } as TimePlanActivity;
    const stats = { big_plan_ref_id: "5" } as BigPlanStats;

    expect(
      CREATE_BIG_PLAN_INBOX_TASK.toDelta({
        new_inbox_task: inboxTask,
        new_time_plan_activity: activity,
        new_big_plan_time_plan_activity: bigPlanActivity,
        updated_big_plan_stats: stats,
      }),
    ).toEqual({
      inboxTasks: [inboxTask],
      activities: [activity, bigPlanActivity],
      bigPlanStats: [stats],
    });
  });
});
