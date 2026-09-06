/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AccessStatus } from './AccessStatus';
import type { Aspect } from './Aspect';
import type { Chapter } from './Chapter';
import type { Chore } from './Chore';
import type { ChoreStack } from './ChoreStack';
import type { Contact } from './Contact';
import type { Goal } from './Goal';
import type { Location } from './Location';
import type { Note } from './Note';
import type { Tag } from './Tag';
import type { UserLight } from './UserLight';
/**
 * A single entry in the find chore stacks response.
 */
export type ChoreStackFindResultEntry = {
    chore_stack: ChoreStack;
    chores?: (Array<Chore> | null);
    aspect?: (Aspect | null);
    chapter?: (Chapter | null);
    goal?: (Goal | null);
    tags: Array<Tag>;
    contacts: Array<Contact>;
    location?: (Location | null);
    note?: (Note | null);
    owner: UserLight;
    access_status: AccessStatus;
};

