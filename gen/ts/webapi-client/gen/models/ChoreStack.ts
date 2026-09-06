/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ChoreStackName } from './ChoreStackName';
import type { EntityId } from './EntityId';
import type { RecurringTaskPeriod } from './RecurringTaskPeriod';
import type { Timestamp } from './Timestamp';
/**
 * A chore stack.
 */
export type ChoreStack = {
    ref_id: EntityId;
    version: number;
    archived: boolean;
    archival_reason?: (string | null);
    created_time: Timestamp;
    last_modified_time: Timestamp;
    archived_time?: (Timestamp | null);
    name: ChoreStackName;
    chore_collection_ref_id: string;
    period: RecurringTaskPeriod;
    aspect_ref_id: EntityId;
    chapter_ref_id?: (EntityId | null);
    goal_ref_id?: (EntityId | null);
};

