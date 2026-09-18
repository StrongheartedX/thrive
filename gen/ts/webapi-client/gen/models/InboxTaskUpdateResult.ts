/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BigPlanStats } from './BigPlanStats';
import type { InboxTask } from './InboxTask';
import type { RecordScoreResult } from './RecordScoreResult';
/**
 * InboxTaskUpdate result.
 */
export type InboxTaskUpdateResult = {
    record_score_result?: (RecordScoreResult | null);
    updated_inbox_task: InboxTask;
    updated_big_plan_stats?: (BigPlanStats | null);
};

