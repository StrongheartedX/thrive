import { NamedEntityTag } from "@jupiter/webapi-client";
import type { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { z } from "zod";
import { parseForm } from "zodix";
import { noteStdOwner } from "@jupiter/core/common/sub/notes/note-std-owner";
import { noErrorSomeData } from "@jupiter/core/infra/action-result";
import { handleActionApiError } from "@jupiter/core/infra/errors.server";

import { getLoggedInApiClient } from "~/api-clients.server";

// Creates an empty note for one of a time plan activity's targets, and returns
// it for the panel to show.
const CreateNoteFormSchema = z.object({
  ownerTag: z.nativeEnum(NamedEntityTag),
  ownerRefId: z.string(),
});

export async function action({ request }: ActionFunctionArgs) {
  const apiClient = await getLoggedInApiClient(request);
  const form = await parseForm(request, CreateNoteFormSchema);

  try {
    const result = await apiClient.notes.noteCreate({
      owner: noteStdOwner(form.ownerTag, form.ownerRefId),
      content: [],
    });

    return json(noErrorSomeData({ new_note: result.new_note }));
  } catch (error) {
    return handleActionApiError(error);
  }
}
