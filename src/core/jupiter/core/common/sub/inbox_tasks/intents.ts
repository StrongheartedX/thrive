/**
 * What the inbox task properties editor's intents do to a task.
 *
 * Kept pure so a view can apply an intent locally exactly the way it's then
 * saved.
 */
import type { ADate } from "@jupiter/webapi-client";
import { InboxTaskStatus } from "@jupiter/webapi-client";
import { DateTime } from "luxon";

export const INBOX_TASK_STATUS_INTENTS = [
  "update",
  "mark-done",
  "mark-not-done",
  "start",
  "restart",
  "block",
  "stop",
  "reactivate",
] as const;

export type InboxTaskStatusIntent = (typeof INBOX_TASK_STATUS_INTENTS)[number];

export const INBOX_TASK_DELAY_INTENTS = [
  "delay-1-day",
  "delay-1-week",
  "delay-1-month",
] as const;

export type InboxTaskDelayIntent = (typeof INBOX_TASK_DELAY_INTENTS)[number];

export function isInboxTaskDelayIntent(
  intent: InboxTaskStatusIntent | InboxTaskDelayIntent,
): intent is InboxTaskDelayIntent {
  return (INBOX_TASK_DELAY_INTENTS as ReadonlyArray<string>).includes(intent);
}

/** The status a task ends up in after ``intent``; "update" keeps ``current``. */
export function inboxTaskStatusForIntent(
  intent: InboxTaskStatusIntent,
  current: InboxTaskStatus,
): InboxTaskStatus {
  switch (intent) {
    case "update":
      return current;
    case "mark-done":
      return InboxTaskStatus.DONE;
    case "mark-not-done":
      return InboxTaskStatus.NOT_DONE;
    case "start":
    case "restart":
      return InboxTaskStatus.IN_PROGRESS;
    case "block":
      return InboxTaskStatus.BLOCKED;
    case "stop":
    case "reactivate":
      return InboxTaskStatus.NOT_STARTED;
  }
}

const DELAYS = {
  "delay-1-day": { days: 1 },
  "delay-1-week": { weeks: 1 },
  "delay-1-month": { months: 1 },
} as const;

/**
 * The dates a task gets when it's put off.
 *
 * It becomes actionable ``intent``'s delay after ``today``. A due date keeps
 * its distance from the old actionable date, or lands on the new actionable
 * date if there wasn't one. No due date stays no due date.
 */
export function delayedInboxTaskDates(
  intent: InboxTaskDelayIntent,
  today: ADate,
  actionableDate: ADate | null | undefined,
  dueDate: ADate | null | undefined,
): { actionableDate: ADate; dueDate: ADate | null } {
  const newActionableDate = DateTime.fromISO(today).plus(DELAYS[intent]);

  let newDueDate: DateTime | null = null;
  if (dueDate) {
    if (actionableDate) {
      const gapDays = DateTime.fromISO(dueDate).diff(
        DateTime.fromISO(actionableDate),
        "days",
      ).days;
      newDueDate = newActionableDate.plus({ days: gapDays });
    } else {
      newDueDate = newActionableDate;
    }
  }

  return {
    actionableDate: newActionableDate.toISODate() as ADate,
    dueDate: newDueDate === null ? null : (newDueDate.toISODate() as ADate),
  };
}
