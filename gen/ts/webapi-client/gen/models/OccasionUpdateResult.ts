/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { InboxTask } from './InboxTask';
import type { Occasion } from './Occasion';
import type { TimeEventFullDaysBlock } from './TimeEventFullDaysBlock';
/**
 * OccasionUpdate result.
 */
export type OccasionUpdateResult = {
    updated_occasion: Occasion;
    updated_inbox_tasks: Array<InboxTask>;
    updated_time_event_full_days_blocks: Array<TimeEventFullDaysBlock>;
};

