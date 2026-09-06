/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EntityId } from './EntityId';
import type { TimePlanActivityFeasability } from './TimePlanActivityFeasability';
import type { TimePlanActivityKind } from './TimePlanActivityKind';
/**
 * Args.
 */
export type TimePlanAssociateWithHabitStacksArgs = {
    ref_id: EntityId;
    habit_stack_ref_ids: Array<EntityId>;
    kind: TimePlanActivityKind;
    feasability: TimePlanActivityFeasability;
};

