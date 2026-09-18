"""UseCase for updating a workspace."""

from jupiter.core.config import (
    JupiterLoggedInMutationContext,
    JupiterTransactionalLoggedInMutationUseCase,
)
from jupiter.core.workspaces.name import WorkspaceName
from jupiter.core.workspaces.root import Workspace
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.update_action import UpdateAction
from jupiter.framework.use_case import (
    mutation_use_case,
)
from jupiter.framework.use_case_io import (
    UseCaseArgsBase,
    UseCaseResultBase,
    use_case_args,
    use_case_result,
)


@use_case_args
class WorkspaceUpdateArgs(UseCaseArgsBase):
    """PersonFindArgs."""

    name: UpdateAction[WorkspaceName]


@use_case_result
class WorkspaceUpdateResult(UseCaseResultBase):
    """WorkspaceUpdate result."""

    updated_workspace: Workspace


@mutation_use_case()
class WorkspaceUpdateUseCase(
    JupiterTransactionalLoggedInMutationUseCase[
        WorkspaceUpdateArgs, WorkspaceUpdateResult
    ]
):
    """UseCase for updating a workspace."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: WorkspaceUpdateArgs,
    ) -> WorkspaceUpdateResult:
        """Execute the command's action."""
        workspace = context.workspace

        workspace = workspace.update(
            context.domain_context,
            name=args.name,
        )

        workspace = await uow.get_for(Workspace).save(workspace)

        return WorkspaceUpdateResult(updated_workspace=workspace)
