/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ADate } from './ADate';
import type { EntityId } from './EntityId';
/**
 * Vacation creation from a travel wish parameters.
 */
export type VacationCreateFromTravelWishArgs = {
    travel_wish_ref_id: EntityId;
    start_date: ADate;
    end_date: ADate;
};

