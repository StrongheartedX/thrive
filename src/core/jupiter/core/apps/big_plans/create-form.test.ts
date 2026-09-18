import { Difficulty, Eisen } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  BigPlanCreateFormSchema,
  BigPlanInboxTaskCreateFormSchema,
  bigPlanCreateArgs,
  bigPlanInboxTaskCreateArgs,
} from "#/core/apps/big_plans/create-form";

describe("bigPlanCreateArgs", () => {
  it("reads the dependencies the multi-select joined", () => {
    const form = BigPlanCreateFormSchema.parse({
      name: "The big plan",
      eisen: Eisen.REGULAR,
      difficulty: Difficulty.EASY,
      dependencyRefIds: "7,8",
    });

    expect(bigPlanCreateArgs(form, "9")).toMatchObject({
      time_plan_ref_id: "9",
      dependency_ref_ids: ["7", "8"],
      is_key: false,
    });
  });

  it("depends on nothing when none are picked", () => {
    const form = BigPlanCreateFormSchema.parse({
      name: "The big plan",
      eisen: Eisen.REGULAR,
      difficulty: Difficulty.EASY,
      dependencyRefIds: "",
    });

    expect(bigPlanCreateArgs(form).dependency_ref_ids).toEqual([]);
  });
});

describe("bigPlanInboxTaskCreateArgs", () => {
  it("makes the task for the big plan", () => {
    const form = BigPlanInboxTaskCreateFormSchema.parse({
      name: "The task",
      isKey: "on",
      eisen: Eisen.URGENT,
      difficulty: Difficulty.MEDIUM,
      dueDate: "",
    });

    expect(bigPlanInboxTaskCreateArgs(form, "500", "9")).toEqual({
      big_plan_ref_id: "500",
      name: "The task",
      time_plan_ref_id: "9",
      time_plan_activity_kind: undefined,
      time_plan_activity_feasability: undefined,
      is_key: true,
      eisen: Eisen.URGENT,
      difficulty: Difficulty.MEDIUM,
      actionable_date: undefined,
      due_date: undefined,
    });
  });
});
