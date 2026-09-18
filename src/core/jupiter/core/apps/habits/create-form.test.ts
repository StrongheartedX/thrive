import {
  Difficulty,
  Eisen,
  HabitRepeatsStrategy,
  RecurringTaskPeriod,
} from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  HabitCreateFormSchema,
  habitCreateArgs,
} from "#/core/apps/habits/create-form";

describe("habitCreateArgs", () => {
  const base = {
    name: "The habit",
    period: RecurringTaskPeriod.WEEKLY,
    eisen: Eisen.REGULAR,
    difficulty: Difficulty.EASY,
  };

  it("reads the gen params and stack", () => {
    const form = HabitCreateFormSchema.parse({
      ...base,
      stack: "40",
      dueAtDay: "3",
      actionableFromDay: "",
      repeatsStrategy: HabitRepeatsStrategy.ALL_SAME,
      repeatsInPeriodCount: "2",
    });

    expect(habitCreateArgs(form, "9")).toMatchObject({
      time_plan_ref_id: "9",
      stack_ref_id: "40",
      due_at_day: 3,
      actionable_from_day: undefined,
      repeats_strategy: HabitRepeatsStrategy.ALL_SAME,
      repeats_in_period_count: 2,
    });
  });

  it("makes no repeats strategy out of none", () => {
    const form = HabitCreateFormSchema.parse({
      ...base,
      stack: "",
      repeatsStrategy: "none",
    });

    expect(habitCreateArgs(form)).toMatchObject({
      stack_ref_id: undefined,
      repeats_strategy: undefined,
    });
  });
});
