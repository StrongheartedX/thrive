/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ChoreStackName } from './ChoreStackName';
import type { EntityId } from './EntityId';
/**
 * Chore stack update parameters.
 */
export type ChoreStackUpdateArgs = {
    ref_id: EntityId;
    name: {
        should_change: boolean;
        value?: ChoreStackName;
    };
    chore_ref_ids: {
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

