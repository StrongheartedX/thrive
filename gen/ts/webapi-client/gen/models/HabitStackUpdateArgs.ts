/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EntityId } from './EntityId';
import type { HabitStackName } from './HabitStackName';
/**
 * Habit stack update parameters.
 */
export type HabitStackUpdateArgs = {
    ref_id: EntityId;
    name: {
        should_change: boolean;
        value?: HabitStackName;
    };
    habit_ref_ids: {
        should_change: boolean;
        value?: Array<EntityId>;
    };
    aspect_ref_id: {
        should_change: boolean;
        value?: EntityId;
    };
    chapter_ref_id: {
        should_change: boolean;
        value?: (EntityId | null);
    };
    goal_ref_id: {
        should_change: boolean;
        value?: (EntityId | null);
    };
};

