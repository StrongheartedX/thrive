/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EntityId } from './EntityId';
/**
 * Chore stack find parameters.
 */
export type ChoreStackFindArgs = {
    allow_archived?: (boolean | null);
    include_tags?: (boolean | null);
    include_notes?: (boolean | null);
    include_life_plan?: (boolean | null);
    include_chores?: (boolean | null);
    filter_ref_ids?: (Array<EntityId> | null);
    filter_aspect_ref_ids?: (Array<EntityId> | null);
};

