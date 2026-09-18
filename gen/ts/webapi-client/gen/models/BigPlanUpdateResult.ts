/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BigPlan } from './BigPlan';
import type { InboxTask } from './InboxTask';
import type { RecordScoreResult } from './RecordScoreResult';
/**
 * BigPlanUpdate result.
 */
export type BigPlanUpdateResult = {
    record_score_result?: (RecordScoreResult | null);
    updated_big_plan: BigPlan;
    updated_inbox_tasks: Array<InboxTask>;
};

