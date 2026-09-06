"""A habit stack — a group of habits done together."""

from jupiter.core.apps.habits.sub.stack.name import HabitStackName
from jupiter.core.common.recurring_task_period import RecurringTaskPeriod
from jupiter.core.common.sub.contacts.sub.link.root import ContactLink
from jupiter.core.common.sub.locations.sub.link.root import LocationLink
from jupiter.core.common.sub.notes.root import Note
from jupiter.core.common.sub.publish.sub.entity.root import PublishEntity
from jupiter.core.common.sub.tags.sub.link.root import TagLink
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.context import DomainContext
from jupiter.framework.entity import (
    IsEntityLinkStd,
    LeafEntity,
    OwnsAtMostOne,
    ParentLink,
    create_entity_action,
    entity,
    update_entity_action,
)
from jupiter.framework.update_action import UpdateAction


@entity("HabitCollection")
class HabitStack(LeafEntity):
    """A habit stack."""

    habit_collection: ParentLink
    name: HabitStackName
    period: RecurringTaskPeriod
    aspect_ref_id: EntityId
    chapter_ref_id: EntityId | None
    goal_ref_id: EntityId | None

    tag_link = OwnsAtMostOne(
        TagLink, owner=IsEntityLinkStd(NamedEntityTag.HABIT_STACK.value)
    )
    contact_link = OwnsAtMostOne(
        ContactLink, owner=IsEntityLinkStd(NamedEntityTag.HABIT_STACK.value)
    )
    location_link = OwnsAtMostOne(
        LocationLink, owner=IsEntityLinkStd(NamedEntityTag.HABIT_STACK.value)
    )
    note = OwnsAtMostOne(Note, owner=IsEntityLinkStd(NamedEntityTag.HABIT_STACK.value))
    publish_entity = OwnsAtMostOne(
        PublishEntity, owner=IsEntityLinkStd(NamedEntityTag.HABIT_STACK.value)
    )

    @staticmethod
    @create_entity_action
    def new_habit_stack(
        ctx: DomainContext,
        habit_collection_ref_id: EntityId,
        name: HabitStackName,
        period: RecurringTaskPeriod,
        aspect_ref_id: EntityId,
        chapter_ref_id: EntityId | None,
        goal_ref_id: EntityId | None,
    ) -> "HabitStack":
        """Create a habit stack."""
        return HabitStack._create(
            ctx,
            habit_collection=ParentLink(habit_collection_ref_id),
            name=name,
            period=period,
            aspect_ref_id=aspect_ref_id,
            chapter_ref_id=chapter_ref_id,
            goal_ref_id=goal_ref_id,
        )

    @update_entity_action
    def update(
        self,
        ctx: DomainContext,
        name: UpdateAction[HabitStackName],
        aspect_ref_id: UpdateAction[EntityId],
        chapter_ref_id: UpdateAction[EntityId | None],
        goal_ref_id: UpdateAction[EntityId | None],
    ) -> "HabitStack":
        """Update a habit stack's properties. Period cannot change after creation."""
        return self._new_version(
            ctx,
            name=name.or_else(self.name),
            aspect_ref_id=aspect_ref_id.or_else(self.aspect_ref_id),
            chapter_ref_id=chapter_ref_id.or_else(self.chapter_ref_id),
            goal_ref_id=goal_ref_id.or_else(self.goal_ref_id),
        )
