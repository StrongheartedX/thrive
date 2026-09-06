/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Aspect } from './Aspect';
import type { Habit } from './Habit';
import type { HabitStack } from './HabitStack';
/**
 * A habit stack with suitability for adding to a time plan.
 */
export type HabitStackFindSuitableForTimePlanResultEntry = {
    habit_stack: HabitStack;
    habits: Array<Habit>;
    aspect?: (Aspect | null);
    has_uncompleted_historical_inbox_tasks: boolean;
    would_generate_in_time_plan: boolean;
};

