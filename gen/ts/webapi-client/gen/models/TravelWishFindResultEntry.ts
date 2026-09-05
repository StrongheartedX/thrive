/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AccessStatus } from './AccessStatus';
import type { Contact } from './Contact';
import type { Location } from './Location';
import type { Tag } from './Tag';
import type { TravelWish } from './TravelWish';
import type { UserLight } from './UserLight';
/**
 * A travel wish find result entry.
 */
export type TravelWishFindResultEntry = {
    travel_wish: TravelWish;
    tags: Array<Tag>;
    contacts: Array<Contact>;
    locations: Array<Location>;
    owner: UserLight;
    access_status: AccessStatus;
};

