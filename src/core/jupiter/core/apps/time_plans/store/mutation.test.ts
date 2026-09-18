import { afterEach, describe, expect, it, vi } from "vitest";

import { postMutation } from "#/core/apps/time_plans/store/mutation";

describe("postMutation", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("posts the fields as a form and returns the action result", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(
        new Response(
          JSON.stringify({ theType: "no-error-some-data", data: { a: 1 } }),
          { status: 200 },
        ),
      );
    vi.stubGlobal("fetch", fetchMock);

    const result = await postMutation<{ a: number }>("/some/route", {
      id: "100",
    });

    expect(result).toEqual({ theType: "no-error-some-data", data: { a: 1 } });
    const [action, init] = fetchMock.mock.calls[0];
    expect(action).toBe("/some/route");
    expect(init.method).toBe("POST");
    expect(String(init.body)).toBe("id=100");
  });

  it("turns a failed response into a global error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("nope", { status: 500 })),
    );

    const result = await postMutation("/some/route", {});

    expect(result.theType).toBe("some-error-no-data");
  });

  it("turns a network error into a global error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));

    const result = await postMutation("/some/route", {});

    expect(result.theType).toBe("some-error-no-data");
  });
});
