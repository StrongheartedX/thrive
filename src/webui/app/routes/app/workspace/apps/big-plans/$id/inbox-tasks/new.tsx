import type { ActionFunctionArgs, LoaderFunctionArgs } from "@remix-run/node";
import { json, redirect } from "@remix-run/node";
import type { ShouldRevalidateFunction } from "@remix-run/react";
import { useActionData, useNavigation, useParams } from "@remix-run/react";
import { useContext } from "react";
import { z } from "zod";
import { parseForm, parseParams } from "zodix";
import { BigPlanInboxTaskCreateForm } from "@jupiter/core/apps/big_plans/component/inbox-task-create-form";
import {
  BigPlanInboxTaskCreateFormSchema,
  bigPlanInboxTaskCreateArgs,
} from "@jupiter/core/apps/big_plans/create-form";
import { makeLeafErrorBoundary } from "@jupiter/core/infra/component/error-boundary";
import { LeafPanel } from "@jupiter/core/infra/component/layout/leaf-panel";
import { DisplayType } from "@jupiter/core/infra/component/use-nested-entities";
import { TopLevelInfoContext } from "@jupiter/core/infra/top-level-context";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";
import {
  createAnotherLocation,
  isCreateAndAnother,
} from "@jupiter/core/infra/create-and-another";

import { getLoggedInApiClient } from "~/api-clients.server";
import { standardShouldRevalidate } from "~/rendering/standard-should-revalidate";
import { useLoaderDataSafeForAnimation } from "~/rendering/use-loader-data-for-animation";

const ParamsSchema = z.object({
  id: z.string(),
});

export const handle = {
  displayType: DisplayType.LEAFLET,
};

export async function loader({ request, params }: LoaderFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const { id: bigPlanId } = parseParams(params, ParamsSchema);
  const bigPlanResult = await apiClient.bigPlans.bigPlanLoad({
    allow_archived: false,
    ref_id: bigPlanId,
  });

  return json({
    bigPlan: bigPlanResult.big_plan,
    timePlan: null,
  });
}

export async function action({ request, params }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const { id: bigPlanId } = parseParams(params, ParamsSchema);
  const form = await parseForm(request, BigPlanInboxTaskCreateFormSchema);

  try {
    const result = await apiClient.bigPlans.bigPlanCreateInboxTask(
      bigPlanInboxTaskCreateArgs(form, bigPlanId),
    );

    if (isCreateAndAnother(form.intent)) {
      return redirect(createAnotherLocation(request));
    }

    return redirect(
      `/app/workspace/apps/big-plans/${bigPlanId}/inbox-tasks/${result.new_inbox_task.ref_id}`,
    );
  } catch (error) {
    return handleActionApiError(error);
  }
}

export const shouldRevalidate: ShouldRevalidateFunction =
  standardShouldRevalidate;

export default function BigPlanNewInboxTask() {
  const loaderData = useLoaderDataSafeForAnimation<typeof loader>();
  const actionData = useActionData<typeof action>();
  const navigation = useNavigation();
  const topLevelInfo = useContext(TopLevelInfoContext);
  const { id: bigPlanId } = useParams();

  const inputsEnabled = navigation.state === "idle";

  return (
    <LeafPanel
      key="big-plan-inbox-tasks/new"
      isLeaflet
      fakeKey="big-plan-inbox-tasks/new"
      returnLocation={`/app/workspace/apps/big-plans/${bigPlanId}`}
      inputsEnabled={inputsEnabled}
    >
      <BigPlanInboxTaskCreateForm
        {...loaderData}
        topLevelInfo={topLevelInfo}
        inputsEnabled={inputsEnabled}
        actionResult={actionData}
      />
    </LeafPanel>
  );
}

export const ErrorBoundary = makeLeafErrorBoundary("../..", ParamsSchema, {
  error: () => `There was an error creating the inbox task! Please try again!`,
});
