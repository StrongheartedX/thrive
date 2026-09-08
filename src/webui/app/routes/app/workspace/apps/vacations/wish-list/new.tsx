import { FormControl } from "@mui/material";
import type { ActionFunctionArgs } from "@remix-run/node";
import { redirect } from "@remix-run/node";
import type { ShouldRevalidateFunction } from "@remix-run/react";
import { useActionData, useNavigation } from "@remix-run/react";
import { z } from "zod";
import { parseForm } from "zodix";
import { useContext, useState } from "react";
import { LocationsEditor } from "@jupiter/core/common/sub/locations/component/locations-editor";
import { makeLeafErrorBoundary } from "@jupiter/core/infra/component/error-boundary";
import { FieldError, GlobalError } from "@jupiter/core/infra/component/errors";
import { LeafPanel } from "@jupiter/core/infra/component/layout/leaf-panel";
import {
  ActionsPosition,
  SectionCard,
} from "@jupiter/core/infra/component/section-card";
import {
  SectionActions,
  ActionSingle,
} from "@jupiter/core/infra/component/section-actions";
import { DisplayType } from "@jupiter/core/infra/component/use-nested-entities";
import { TopLevelInfoContext } from "@jupiter/core/infra/top-level-context";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";
import {
  CREATE_AND_ANOTHER_INTENT,
  createAnotherLocation,
  isCreateAndAnother,
} from "@jupiter/core/infra/create-and-another";

import { standardShouldRevalidate } from "~/rendering/standard-should-revalidate";
import { getLoggedInApiClient } from "~/api-clients.server";

const ParamsSchema = z.object({});

const CreateFormSchema = z.object({
  intent: z.string().optional(),
  locations: z.string(),
});

export const handle = {
  displayType: DisplayType.LEAF,
};

export async function action({ request }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const form = await parseForm(request, CreateFormSchema);

  try {
    const result = await apiClient.vacations.travelWishCreate({
      location_ref_id: form.locations.trim().split(",")[0] ?? "",
    });

    if (isCreateAndAnother(form.intent)) {
      return redirect(createAnotherLocation(request));
    }

    return redirect(
      `/app/workspace/apps/vacations/wish-list/${result.new_travel_wish.ref_id}`,
    );
  } catch (error) {
    return handleActionApiError(error);
  }
}

export const shouldRevalidate: ShouldRevalidateFunction =
  standardShouldRevalidate;

export default function NewTravelWish() {
  const navigation = useNavigation();
  const actionData = useActionData<typeof action>();
  const topLevelInfo = useContext(TopLevelInfoContext);
  const inputsEnabled = navigation.state === "idle";
  // Picking an address off the map makes the location in the background, and
  // there's no travel wish to make until that comes back with a ref id.
  const [locationRefIds, setLocationRefIds] = useState<Array<string>>([]);
  const hasLocation = locationRefIds.length > 0;

  return (
    <LeafPanel
      key="vacations/wish-list/new"
      fakeKey={"vacations/wish-list/new"}
      returnLocation="/app/workspace/apps/vacations/wish-list"
      inputsEnabled={inputsEnabled}
    >
      <GlobalError actionResult={actionData} />
      <SectionCard
        title="New Travel Wish"
        actionsPosition={ActionsPosition.BELOW}
        actions={
          <SectionActions
            id="travel-wish-create"
            topLevelInfo={topLevelInfo}
            inputsEnabled={inputsEnabled}
            actions={[
              ActionSingle({
                id: "travel-wish-create",
                text: "Create",
                value: "create",
                highlight: true,
                disabled: !hasLocation,
              }),
              ActionSingle({
                id: "travel-wish-create-and-another",
                text: "Create & Another",
                value: CREATE_AND_ANOTHER_INTENT,
                disabled: !hasLocation,
              }),
            ]}
          />
        }
      >
        <FormControl fullWidth>
          <LocationsEditor
            name="locations"
            aloneOnLine
            inputsEnabled={inputsEnabled}
            onSelectionChange={setLocationRefIds}
          />
          <FieldError actionResult={actionData} fieldName="/location_ref_id" />
        </FormControl>
      </SectionCard>
    </LeafPanel>
  );
}

export const ErrorBoundary = makeLeafErrorBoundary(
  "/app/workspace/apps/vacations/wish-list",
  ParamsSchema,
  {
    error: () =>
      `There was an error creating the travel wish! Please try again!`,
  },
);
