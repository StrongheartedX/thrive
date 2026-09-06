"""Shared service for loading a habit stack and its dependent entities."""

from jupiter.core.apps.habits.sub.habit.root import Habit
from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.apps.life_plan.sub.aspects.root import Aspect
from jupiter.core.apps.life_plan.sub.chapters.root import Chapter
from jupiter.core.apps.life_plan.sub.goals.root import Goal
from jupiter.core.common.sub.access.sub.grant.service.get_access_level_for_entity import (
    GetAccessLevelForEntityService,
)
from jupiter.core.common.sub.access.sub.grant.service.load_user_that_owns_entity import (
    LoadUserThatOwnsEntityService,
)
from jupiter.core.common.sub.access.sub.status.root import AccessStatus
from jupiter.core.common.sub.contacts.sub.contact.root import Contact
from jupiter.core.common.sub.contacts.sub.link.root import ContactLinkRepository
from jupiter.core.common.sub.locations.sub.link.root import LocationLinkRepository
from jupiter.core.common.sub.locations.sub.link.service.load import (
    LoadLocationForLinkService,
)
from jupiter.core.common.sub.locations.sub.location.root import Location
from jupiter.core.common.sub.notes.root import Note, NoteRepository
from jupiter.core.common.sub.publish.sub.entity.root import (
    PublishEntity,
    PublishEntityRepository,
)
from jupiter.core.common.sub.tags.sub.link.root import TagLinkRepository
from jupiter.core.common.sub.tags.sub.tag.root import Tag, TagRepository
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.core.users.user_light import UserLight
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.base.entity_link import EntityLink
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case_io import UseCaseResultBase, use_case_result


@use_case_result
class HabitStackLoadResult(UseCaseResultBase):
    """HabitStackLoadResult."""

    habit_stack: HabitStack
    habits: list[Habit]
    aspect: Aspect
    chapter: Chapter | None
    goal: Goal | None
    tags: list[Tag]
    contacts: list[Contact]
    location: Location | None
    note: Note | None
    publish_entity: PublishEntity | None
    owner: UserLight
    access_status: AccessStatus | None


class HabitStackLoadService:
    """Shared service for loading a habit stack and its dependent entities."""

    async def do_it(
        self,
        uow: DomainUnitOfWork,
        habit_stack: HabitStack,
        *,
        user_ref_id: EntityId | None = None,
        allow_archived: bool = False,
        include_publish_entity: bool = True,
    ) -> HabitStackLoadResult:
        """Load a habit stack together with the entities that hang off it."""
        habit_stack = await uow.get_for(HabitStack).load_by_id(
            habit_stack.ref_id, allow_archived=allow_archived
        )
        owner_link = EntityLink.std(
            NamedEntityTag.HABIT_STACK.value, habit_stack.ref_id
        )

        aspect = await uow.get_for(Aspect).load_by_id(habit_stack.aspect_ref_id)
        chapter = (
            await uow.get_for(Chapter).load_by_id(habit_stack.chapter_ref_id)
            if habit_stack.chapter_ref_id
            else None
        )
        goal = (
            await uow.get_for(Goal).load_by_id(habit_stack.goal_ref_id)
            if habit_stack.goal_ref_id
            else None
        )

        habits = await uow.get_for(Habit).find_all_generic(
            parent_ref_id=None,
            allow_archived=allow_archived,
            stack_ref_id=habit_stack.ref_id,
        )

        tag_link = await uow.get(TagLinkRepository).load_optional_for_owner(
            owner=owner_link,
        )
        if tag_link is not None:
            tags = await uow.get(TagRepository).find_all_generic(
                allow_archived=False,
                ref_id=tag_link.ref_ids,
            )
        else:
            tags = []

        contact_link = await uow.get(ContactLinkRepository).load_optional_for_owner(
            owner_link,
        )
        if contact_link is not None:
            contacts = await uow.get_for(Contact).find_all_generic(
                allow_archived=False,
                ref_id=contact_link.contacts_ref_ids,
            )
        else:
            contacts = []

        location_link = await uow.get(LocationLinkRepository).load_optional_for_owner(
            owner_link,
        )
        location = await LoadLocationForLinkService().do_it(uow, location_link)

        note = await uow.get(NoteRepository).load_optional_for_owner(
            owner_link,
            allow_archived=allow_archived,
        )

        publish_entity = None
        if include_publish_entity:
            publish_entity = await uow.get(
                PublishEntityRepository
            ).load_optional_for_owner(
                owner_link,
                allow_archived=allow_archived,
            )

        owner = await LoadUserThatOwnsEntityService().do_it(uow, owner_link)
        access_status = (
            await GetAccessLevelForEntityService().do_it(uow, owner_link, user_ref_id)
            if user_ref_id is not None
            else None
        )

        return HabitStackLoadResult(
            habit_stack=habit_stack,
            habits=habits,
            aspect=aspect,
            chapter=chapter,
            goal=goal,
            tags=tags,
            contacts=contacts,
            location=location,
            note=note,
            publish_entity=publish_entity,
            owner=owner,
            access_status=access_status,
        )
