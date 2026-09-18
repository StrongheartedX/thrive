import { InboxTaskStatus } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  delayedInboxTaskDates,
  inboxTaskStatusForIntent,
} from "#/core/common/sub/inbox_tasks/intents";

describe("inboxTaskStatusForIntent", () => {
  it.each([
    ["mark-done", InboxTaskStatus.DONE],
    ["mark-not-done", InboxTaskStatus.NOT_DONE],
    ["start", InboxTaskStatus.IN_PROGRESS],
    ["restart", InboxTaskStatus.IN_PROGRESS],
    ["block", InboxTaskStatus.BLOCKED],
    ["stop", InboxTaskStatus.NOT_STARTED],
    ["reactivate", InboxTaskStatus.NOT_STARTED],
  ] as const)("%s → %s", (intent, expected) => {
    expect(inboxTaskStatusForIntent(intent, InboxTaskStatus.BLOCKED)).toBe(
      expected,
    );
  });

  it("keeps the current status on update", () => {
    expect(inboxTaskStatusForIntent("update", InboxTaskStatus.BLOCKED)).toBe(
      InboxTaskStatus.BLOCKED,
    );
  });
});

describe("delayedInboxTaskDates", () => {
  it("makes the task actionable after the delay from today", () => {
    expect(
      delayedInboxTaskDates("delay-1-week", "2026-09-14", null, null),
    ).toEqual({ actionableDate: "2026-09-21", dueDate: null });
    expect(
      delayedInboxTaskDates("delay-1-month", "2026-01-31", null, null)
        .actionableDate,
    ).toBe("2026-02-28");
  });

  it("keeps the gap between the actionable and due dates", () => {
    expect(
      delayedInboxTaskDates(
        "delay-1-day",
        "2026-09-14",
        "2026-09-01",
        "2026-09-04",
      ),
    ).toEqual({ actionableDate: "2026-09-15", dueDate: "2026-09-18" });
  });

  it("puts the due date on the new actionable date when there was none", () => {
    expect(
      delayedInboxTaskDates("delay-1-day", "2026-09-14", null, "2026-09-04"),
    ).toEqual({ actionableDate: "2026-09-15", dueDate: "2026-09-15" });
  });
});
