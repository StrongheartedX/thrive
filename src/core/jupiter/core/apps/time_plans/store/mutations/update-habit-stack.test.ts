import type { Habit, HabitStack } from "@jupiter/webapi-client";
import { RecurringTaskPeriod } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  UPDATE_HABIT_STACK,
  updateHabitStackArgsFromForm,
} from "#/core/apps/time_plans/store/mutations/update-habit-stack";
import {
  createTimePlanStore,
  seedTimePlanSource,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

const MODIFIED = "2026-09-14T10:00:00Z";

function habitStack(fields: Partial<HabitStack> = {}): HabitStack {
  return {
    ref_id: "40",
    version: 1,
    archived: false,
    name: "Stored stack",
    period: RecurringTaskPeriod.WEEKLY,
    aspect_ref_id: "1",
    chapter_ref_id: "2",
    goal_ref_id: null,
    last_modified_time: "2026-09-01T00:00:00Z",
    ...fields,
  } as HabitStack;
}

function habit(refId: string, stackRefId: string | null): Habit {
  return {
    ref_id: refId,
    version: 1,
    archived: false,
    name: `Habit ${refId}`,
    stack_ref_id: stackRefId,
    last_modified_time: "2026-09-01T00:00:00Z",
  } as Habit;
}

function editorForm(fields: Record<string, string>): FormData {
  const formData = new FormData();
  const values = {
    RefId: "40",
    Name: "Edited stack",
    HabitRefIds: "401,403",
    ...fields,
  };
  for (const [name, value] of Object.entries(values)) {
    formData.set(`targetHabitStack${name}`, value);
  }
  return formData;
}

describe("updateHabitStackArgsFromForm", () => {
  it("reads the name, habits and life plan", () => {
    expect(
      updateHabitStackArgsFromForm(
        editorForm({ Aspect: "3", Chapter: "", Goal: "" }),
        MODIFIED,
        "targetHabitStack",
      ),
    ).toEqual({
      refId: "40",
      name: "Edited stack",
      habitRefIds: ["401", "403"],
      lifePlan: { aspectRefId: "3", chapterRefId: null, goalRefId: null },
      modifiedTime: MODIFIED,
    });
  });
});

describe("UPDATE_HABIT_STACK", () => {
  it("renames the stack and moves habits in and out of it", () => {
    const entities = UPDATE_HABIT_STACK.applyOptimistic(
      selectTimePlanEntities(
        seedTimePlanSource(createTimePlanStore(), "plan", {
          habitStacks: [habitStack()],
          habits: [
            habit("401", "40"),
            habit("402", "40"),
            habit("403", null),
            habit("404", "41"),
          ],
        }),
      ),
      updateHabitStackArgsFromForm(
        editorForm({}),
        MODIFIED,
        "targetHabitStack",
      ),
    );

    expect(entities.habitStacks["40"]).toMatchObject({
      name: "Edited stack",
      chapter_ref_id: "2",
    });
    expect(entities.habits["401"].last_modified_time).not.toBe(MODIFIED);
    expect(entities.habits["402"].stack_ref_id).toBeNull();
    expect(entities.habits["403"].stack_ref_id).toBe("40");
    expect(entities.habits["404"].stack_ref_id).toBe("41");
  });

  it("merges back the stack and the habits that moved", () => {
    const updatedStack = habitStack({ version: 2 });
    const updatedHabits = [habit("403", "40")];

    expect(
      UPDATE_HABIT_STACK.toDelta({
        updated_habit_stack: updatedStack,
        updated_habits: updatedHabits,
      }),
    ).toEqual({ habitStacks: [updatedStack], habits: updatedHabits });
  });
});
