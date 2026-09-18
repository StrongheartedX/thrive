"""Use case for updating a contact."""

from jupiter.core.common.sub.contacts.root import ContactDomain
from jupiter.core.common.sub.contacts.sub.contact.name import ContactName
from jupiter.core.common.sub.contacts.sub.contact.root import Contact
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.leaf_support_entity_support import (
    JupiterUpdateLeafSupportEntityArgs,
    JupiterUpdateLeafSupportEntityUseCase,
)
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.update_action import UpdateAction
from jupiter.framework.use_case import mutation_use_case
from jupiter.framework.use_case_io import (
    UseCaseResultBase,
    use_case_args,
    use_case_result,
)


@use_case_args
class ContactUpdateArgs(JupiterUpdateLeafSupportEntityArgs):
    """ContactUpdate args."""

    ref_id: EntityId
    name: UpdateAction[ContactName]


@use_case_result
class ContactUpdateResult(UseCaseResultBase):
    """ContactUpdate result."""

    updated_contact: Contact


@mutation_use_case()
class ContactUpdateUseCase(
    JupiterUpdateLeafSupportEntityUseCase[ContactUpdateArgs, ContactUpdateResult]
):
    """Use case for updating a contact."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: ContactUpdateArgs,
    ) -> ContactUpdateResult:
        """Execute the command's action."""
        _, contact = await self.load_in_parent(
            uow,
            ContactDomain,
            Contact,
            args.ref_id,
            context.workspace.ref_id,
        )
        contact = contact.update(
            ctx=context.domain_context,
            name=args.name,
        )
        contact = await uow.get_for(Contact).save(contact)

        return ContactUpdateResult(updated_contact=contact)
