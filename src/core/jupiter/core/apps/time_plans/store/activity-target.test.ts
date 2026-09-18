import type {
  Habit,
  HabitStack,
  InboxTask,
  TimePlanActivity,
} from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import { selectActivityWithTarget } from "#/core/apps/time_plans/store/activity-target";
import {
  createTimePlanStore,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

const empty = selectTimePlanEntities(createTimePlanStore());

describe("selectActivityWithTarget", () => {
  it("is null for an activity the store doesn't have", () => {
    expect(selectActivityWithTarget(empty, "20")).toBeNull();
  });

  it("finds an inbox task activity's task", () => {
    const activity = {
      ref_id: "20",
      target: "InboxTask:std:100",
    } as unknown as TimePlanActivity;
    const inboxTask = { ref_id: "100" } as InboxTask;

    const selected = selectActivityWithTarget(
      {
        ...empty,
        activities: { "20": activity },
        inboxTasks: { "100": inboxTask },
      },
      "20",
    );

    expect(selected?.timePlanActivity).toBe(activity);
    expect(selected?.targetInboxTask).toBe(inboxTask);
    expect(selected?.targetHabit).toBeNull();
    expect(selected?.habitStackMembers).toEqual([]);
  });

  it("finds a habit stack activity's stack and its members", () => {
    const activity = {
      ref_id: "21",
      target: "HabitStack:std:7",
    } as unknown as TimePlanActivity;
    const stack = { ref_id: "7" } as HabitStack;
    const member = { ref_id: "30", stack_ref_id: "7" } as Habit;
    const other = { ref_id: "31", stack_ref_id: "8" } as Habit;

    const selected = selectActivityWithTarget(
      {
        ...empty,
        activities: { "21": activity },
        habitStacks: { "7": stack },
        habits: { "30": member, "31": other },
      },
      "21",
    );

    expect(selected?.targetHabitStack).toBe(stack);
    expect(selected?.habitStackMembers).toEqual([member]);
  });
});
