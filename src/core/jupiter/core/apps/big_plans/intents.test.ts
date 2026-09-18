import { BigPlanStatus } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import { bigPlanStatusForIntent } from "#/core/apps/big_plans/intents";

describe("bigPlanStatusForIntent", () => {
  it.each([
    ["mark-done", BigPlanStatus.DONE],
    ["mark-not-done", BigPlanStatus.NOT_DONE],
    ["start", BigPlanStatus.IN_PROGRESS],
    ["restart", BigPlanStatus.IN_PROGRESS],
    ["block", BigPlanStatus.BLOCKED],
    ["stop", BigPlanStatus.NOT_STARTED],
    ["reactivate", BigPlanStatus.NOT_STARTED],
  ] as const)("%s → %s", (intent, expected) => {
    expect(bigPlanStatusForIntent(intent, BigPlanStatus.BLOCKED)).toBe(
      expected,
    );
  });

  it("keeps the current status on update", () => {
    expect(bigPlanStatusForIntent("update", BigPlanStatus.BLOCKED)).toBe(
      BigPlanStatus.BLOCKED,
    );
  });
});
