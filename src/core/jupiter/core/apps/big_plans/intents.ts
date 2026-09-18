/**
 * What the big plan properties editor's intents do to a big plan.
 *
 * Kept pure so a view can apply an intent locally exactly the way it's then
 * saved.
 */
import { BigPlanStatus } from "@jupiter/webapi-client";

export const BIG_PLAN_STATUS_INTENTS = [
  "update",
  "mark-done",
  "mark-not-done",
  "start",
  "restart",
  "block",
  "stop",
  "reactivate",
] as const;

export type BigPlanStatusIntent = (typeof BIG_PLAN_STATUS_INTENTS)[number];

/** The status a big plan ends up in after ``intent``; "update" keeps ``current``. */
export function bigPlanStatusForIntent(
  intent: BigPlanStatusIntent,
  current: BigPlanStatus,
): BigPlanStatus {
  switch (intent) {
    case "update":
      return current;
    case "mark-done":
      return BigPlanStatus.DONE;
    case "mark-not-done":
      return BigPlanStatus.NOT_DONE;
    case "start":
    case "restart":
      return BigPlanStatus.IN_PROGRESS;
    case "block":
      return BigPlanStatus.BLOCKED;
    case "stop":
    case "reactivate":
      return BigPlanStatus.NOT_STARTED;
  }
}
