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
import type { PublishEntity } from './PublishEntity';
import type { Tag } from './Tag';
import type { UserLight } from './UserLight';
/**
 * ChoreStackLoadResult.
 */
export type ChoreStackLoadResult = {
    chore_stack: ChoreStack;
    chores: Array<Chore>;
    aspect: Aspect;
    chapter?: (Chapter | null);
    goal?: (Goal | null);
    tags: Array<Tag>;
    contacts: Array<Contact>;
    location?: (Location | null);
    note?: (Note | null);
    publish_entity?: (PublishEntity | null);
    owner: UserLight;
    access_status?: (AccessStatus | null);
};

