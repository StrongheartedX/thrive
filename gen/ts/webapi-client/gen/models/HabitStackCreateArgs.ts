/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EntityId } from './EntityId';
import type { HabitStackName } from './HabitStackName';
import type { RecurringTaskPeriod } from './RecurringTaskPeriod';
/**
 * Habit stack creation parameters.
 */
export type HabitStackCreateArgs = {
    name: HabitStackName;
    period: RecurringTaskPeriod;
    habit_ref_ids: Array<EntityId>;
    aspect_ref_id?: (EntityId | null);
    chapter_ref_id?: (EntityId | null);
    goal_ref_id?: (EntityId | null);
};

