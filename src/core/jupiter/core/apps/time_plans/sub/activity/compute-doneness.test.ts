/**
 * Shared doneness cases, run against the TypeScript implementation.
 *
 * Keep the JSON in sync with ``compute_doneness.test.py``.
 */
import type {
  BigPlanStatus,
  InboxTaskStatus,
  TimePlanActivityKind,
} from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import { computeActivityDoneness } from "#/core/apps/time_plans/sub/activity/compute-doneness";
import casesJson from "#/core/apps/time_plans/sub/activity/compute_doneness.cases.json";

interface DonenessCase {
  name: string;
  time_plan: { start_date: string; end_date: string };
  activities: Array<{
    ref_id: string;
    kind: string;
    target: string;
  }>;
  inbox_tasks: Array<{
    ref_id: string;
    status: string;
    last_modified_time: string;
    owner: string;
  }>;
  big_plans?: Array<{
    ref_id: string;
    status: string;
    last_modified_time: string;
  }>;
  habits?: Array<{ ref_id: string; stack_ref_id: string | null }>;
  habit_stacks?: Array<{ ref_id: string }>;
  chores?: Array<{ ref_id: string; stack_ref_id: string | null }>;
  chore_stacks?: Array<{ ref_id: string }>;
  expected: Record<string, string>;
}

const cases = casesJson as unknown as DonenessCase[];

describe("computeActivityDoneness", () => {
  it.each(cases)("$name", (testCase) => {
    const actual = computeActivityDoneness({
      timePlan: testCase.time_plan,
      activities: testCase.activities.map((activity) => ({
        ref_id: activity.ref_id,
        kind: activity.kind as TimePlanActivityKind,
        target: activity.target,
      })),
      inboxTasks: testCase.inbox_tasks.map((inboxTask) => ({
        ref_id: inboxTask.ref_id,
        status: inboxTask.status as InboxTaskStatus,
        last_modified_time: inboxTask.last_modified_time,
        owner: inboxTask.owner,
      })),
      bigPlans: testCase.big_plans?.map((bigPlan) => ({
        ref_id: bigPlan.ref_id,
        status: bigPlan.status as BigPlanStatus,
        last_modified_time: bigPlan.last_modified_time,
      })),
      habits: testCase.habits,
      habitStacks: testCase.habit_stacks,
      chores: testCase.chores,
      choreStacks: testCase.chore_stacks,
    });

    expect(actual).toEqual(testCase.expected);
  });
});
