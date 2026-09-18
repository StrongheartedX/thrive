/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BigPlanStats } from './BigPlanStats';
import type { InboxTask } from './InboxTask';
import type { TimePlanActivity } from './TimePlanActivity';
/**
 * BigPlanCreateInboxTask result.
 */
export type BigPlanCreateInboxTaskResult = {
    new_inbox_task: InboxTask;
    new_time_plan_activity?: (TimePlanActivity | null);
    new_big_plan_time_plan_activity?: (TimePlanActivity | null);
    updated_big_plan_stats?: (BigPlanStats | null);
};

