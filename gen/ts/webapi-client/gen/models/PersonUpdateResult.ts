/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Contact } from './Contact';
import type { InboxTask } from './InboxTask';
import type { Person } from './Person';
/**
 * PersonUpdate result.
 */
export type PersonUpdateResult = {
    updated_person: Person;
    updated_contact: Contact;
    updated_inbox_tasks: Array<InboxTask>;
};

