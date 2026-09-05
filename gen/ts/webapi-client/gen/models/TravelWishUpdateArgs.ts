/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EntityId } from './EntityId';
import type { TravelWishName } from './TravelWishName';
/**
 * Travel wish update parameters.
 */
export type TravelWishUpdateArgs = {
    ref_id: EntityId;
    name: {
        should_change: boolean;
        value?: TravelWishName;
    };
};

