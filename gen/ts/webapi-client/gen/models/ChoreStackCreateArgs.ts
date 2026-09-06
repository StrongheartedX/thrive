/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ChoreStackName } from './ChoreStackName';
import type { EntityId } from './EntityId';
import type { RecurringTaskPeriod } from './RecurringTaskPeriod';
/**
 * Chore stack creation parameters.
 */
export type ChoreStackCreateArgs = {
    name: ChoreStackName;
    period: RecurringTaskPeriod;
    chore_ref_ids: Array<EntityId>;
    aspect_ref_id?: (EntityId | null);
    chapter_ref_id?: (EntityId | null);
    goal_ref_id?: (EntityId | null);
};

