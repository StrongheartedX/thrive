import type {
  Contact,
  ChoreStackFindResultEntry,
  Tag,
} from "@jupiter/webapi-client";
import { DocsHelpSubject } from "@jupiter/webapi-client";
import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import type { ShouldRevalidateFunction } from "@remix-run/react";
import { useContext } from "react";
import { EntityNameComponent } from "@jupiter/core/common/component/entity-name";
import { EntityNoNothingCard } from "@jupiter/core/infra/component/entity-no-nothing-card";
import {
  EntityCard,
  EntityLink,
} from "@jupiter/core/infra/component/entity-card";
import { EntityStack } from "@jupiter/core/infra/component/entity-stack";
import { makeBranchErrorBoundary } from "@jupiter/core/infra/component/error-boundary";
import { NestingAwareBlock } from "@jupiter/core/infra/component/layout/nesting-aware-block";
import { NestedOutlet } from "@jupiter/core/infra/component/layout/nested-outlet";
import { BranchPanel } from "@jupiter/core/infra/component/layout/branch-panel";
import {
  DisplayType,
  useBranchNeedsToShowLeaf,
} from "@jupiter/core/infra/component/use-nested-entities";
import { TopLevelInfoContext } from "@jupiter/core/infra/top-level-context";
import {
  NavSingle,
  SectionActions,
} from "@jupiter/core/infra/component/section-actions";
import { PeriodTag } from "@jupiter/core/common/component/period-tag";
import { TagTag } from "#/core/common/sub/tags/component/tag-tag";
import { ContactTag } from "#/core/common/sub/contacts/component/contact-tag";
import { LocationTag } from "#/core/common/sub/locations/component/location-tag";
import { UserLightChip } from "#/core/users/components/user-light-chip";
import { sortChoreStacksNaturally } from "@jupiter/core/apps/chores/root";
import { z } from "zod";

import { useLoaderDataSafeForAnimation } from "~/rendering/use-loader-data-for-animation";
import { basicShouldRevalidate } from "~/rendering/standard-should-revalidate";
import { getLoggedInApiClient } from "~/api-clients.server";

const ParamsSchema = z.object({});

export const handle = {
  displayType: DisplayType.BRANCH,
};

export async function loader({ request }: LoaderFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const response = await apiClient.chores.choreStackFind({
    allow_archived: false,
    include_tags: true,
    include_notes: false,
    include_life_plan: false,
    include_chores: false,
  });

  return json({
    entries: response.entries as Array<ChoreStackFindResultEntry>,
  });
}

export const shouldRevalidate: ShouldRevalidateFunction = basicShouldRevalidate;

export default function ChoreStacks() {
  const loaderData = useLoaderDataSafeForAnimation<typeof loader>();
  const topLevelInfo = useContext(TopLevelInfoContext);
  const shouldShowALeaf = useBranchNeedsToShowLeaf();

  const sortedStacks = sortChoreStacksNaturally(
    loaderData.entries.map((entry) => entry.chore_stack),
  );
  const entriesByRefId = new Map(
    loaderData.entries.map((entry) => [entry.chore_stack.ref_id, entry]),
  );

  return (
    <BranchPanel
      key="chores-stacks"
      createLocation="/app/workspace/apps/chores/stacks/new"
      returnLocation="/app/workspace/apps/chores"
      actions={
        <SectionActions
          id="chore-stacks-actions"
          topLevelInfo={topLevelInfo}
          inputsEnabled={true}
          actions={[
            NavSingle({
              id: "chores-all",
              text: "All chores",
              link: "/app/workspace/apps/chores",
            }),
          ]}
        />
      }
    >
      <NestingAwareBlock shouldHide={shouldShowALeaf}>
        {sortedStacks.length === 0 && (
          <EntityNoNothingCard
            title="You Have To Start Somewhere"
            message="There are no chore stacks to show. You can create a new stack."
            newEntityLocations="/app/workspace/apps/chores/stacks/new"
            helpSubject={DocsHelpSubject.CHORES}
          />
        )}
        <EntityStack>
          {sortedStacks.map((stack) => {
            const entry = entriesByRefId.get(stack.ref_id);
            if (!entry) {
              return null;
            }
            return (
              <EntityCard
                key={`chore-stack-${stack.ref_id}`}
                entityId={`chore-stack-${stack.ref_id}`}
              >
                <UserLightChip
                  user={entry.owner}
                  currentUserRefId={topLevelInfo.user.ref_id}
                />
                <EntityLink
                  to={`/app/workspace/apps/chores/stacks/${stack.ref_id}`}
                >
                  <EntityNameComponent name={stack.name} />
                  <PeriodTag period={stack.period} />
                  {entry.tags?.map((tag: Tag) => (
                    <TagTag key={tag.ref_id} tag={tag} />
                  ))}
                  {entry.contacts?.map((contact: Contact) => (
                    <ContactTag key={contact.ref_id} contact={contact} />
                  ))}
                  {entry.location && <LocationTag location={entry.location} />}
                </EntityLink>
              </EntityCard>
            );
          })}
        </EntityStack>
      </NestingAwareBlock>

      <NestedOutlet />
    </BranchPanel>
  );
}

export const ErrorBoundary = makeBranchErrorBoundary(
  "/app/workspace/apps/chores",
  ParamsSchema,
  {
    error: () => `There was an error loading chore stacks! Please try again!`,
  },
);
