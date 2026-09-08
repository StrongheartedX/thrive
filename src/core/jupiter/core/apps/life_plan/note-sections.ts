import { RecurringTaskPeriod } from "@jupiter/webapi-client";

import { comparePeriods } from "#/core/common/recurring-task-period";

export function periodAllowsAspectsInNote(
  period: RecurringTaskPeriod,
): boolean {
  return comparePeriods(period, RecurringTaskPeriod.MONTHLY) >= 0;
}

export function periodAllowsGoalsInNote(period: RecurringTaskPeriod): boolean {
  return comparePeriods(period, RecurringTaskPeriod.QUARTERLY) >= 0;
}
