/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AccessStatus } from './AccessStatus';
import type { Aspect } from './Aspect';
import type { Chapter } from './Chapter';
import type { Contact } from './Contact';
import type { Goal } from './Goal';
import type { Habit } from './Habit';
import type { HabitStack } from './HabitStack';
import type { Location } from './Location';
import type { Note } from './Note';
import type { PublishEntity } from './PublishEntity';
import type { Tag } from './Tag';
import type { UserLight } from './UserLight';
/**
 * HabitStackLoadResult.
 */
export type HabitStackLoadResult = {
    habit_stack: HabitStack;
    habits: Array<Habit>;
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

