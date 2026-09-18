import { NamedEntityTag } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  CREATE_NOTE,
  createdNoteKey,
} from "#/core/apps/time_plans/store/mutations/create-note";
import {
  createTimePlanStore,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

describe("CREATE_NOTE", () => {
  const args = { ownerTag: NamedEntityTag.BIG_PLAN, ownerRefId: "500" };

  it("posts the note's owner", () => {
    expect(CREATE_NOTE.toFormFields(args)).toEqual({
      ownerTag: NamedEntityTag.BIG_PLAN,
      ownerRefId: "500",
    });
  });

  it("leaves the store alone", () => {
    const entities = selectTimePlanEntities(createTimePlanStore());

    expect(CREATE_NOTE.applyOptimistic(entities, args)).toBe(entities);
    expect(CREATE_NOTE.toDelta({ new_note: {} as never })).toEqual({});
  });

  it("keys notes by owner", () => {
    expect(createdNoteKey(NamedEntityTag.HABIT, "7")).not.toBe(
      createdNoteKey(NamedEntityTag.CHORE, "7"),
    );
  });
});
