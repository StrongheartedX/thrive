/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Aspect } from './Aspect';
import type { Chore } from './Chore';
import type { ChoreStack } from './ChoreStack';
/**
 * A chore stack with suitability for adding to a time plan.
 */
export type ChoreStackFindSuitableForTimePlanResultEntry = {
    chore_stack: ChoreStack;
    chores: Array<Chore>;
    aspect?: (Aspect | null);
    has_uncompleted_historical_inbox_tasks: boolean;
    would_generate_in_time_plan: boolean;
};

