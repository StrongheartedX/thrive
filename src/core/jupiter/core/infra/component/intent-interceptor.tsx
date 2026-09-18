/**
 * Lets a view take over some form intents instead of submitting the form.
 *
 * The action buttons in a ``SectionCard`` (and a leaf panel's own controls,
 * like archiving) are submit buttons carrying an ``intent``. A view that
 * handles some intents itself - say, as a local edit posted to a resource
 * route - registers handlers for them here. Submitting one of those runs its
 * handler with the form's data; every other intent submits the form as usual.
 * Views that register nothing are unaffected.
 */
import type { FormEvent, PropsWithChildren } from "react";
import { createContext, useCallback, useContext, useMemo } from "react";

export type IntentHandler = (formData: FormData) => void;

export type IntentHandlers = Readonly<Record<string, IntentHandler>>;

const IntentInterceptorContext = createContext<IntentHandlers>({});

interface IntentInterceptorProviderProps {
  handlers: IntentHandlers;
}

export function IntentInterceptorProvider(
  props: PropsWithChildren<IntentInterceptorProviderProps>,
) {
  const outer = useContext(IntentInterceptorContext);
  const handlers = useMemo(
    () => ({ ...outer, ...props.handlers }),
    [outer, props.handlers],
  );

  return (
    <IntentInterceptorContext.Provider value={handlers}>
      {props.children}
    </IntentInterceptorContext.Provider>
  );
}

/**
 * Runs the handler for the intent that submitted ``event``'s form instead of
 * submitting it, when ``handlers`` has one.
 */
export function interceptIntentSubmit(
  event: FormEvent<HTMLFormElement>,
  handlers: IntentHandlers,
): void {
  const submitter = (event.nativeEvent as SubmitEvent).submitter;
  if (
    !(submitter instanceof HTMLButtonElement) ||
    submitter.name !== "intent"
  ) {
    return;
  }

  const handler = handlers[submitter.value];
  if (handler === undefined) {
    return;
  }

  event.preventDefault();
  handler(new FormData(event.currentTarget, submitter));
}

/** An ``onSubmit`` for forms whose intents may be intercepted. */
export function useInterceptedSubmit(): (
  event: FormEvent<HTMLFormElement>,
) => void {
  const handlers = useContext(IntentInterceptorContext);

  return useCallback(
    (event: FormEvent<HTMLFormElement>) =>
      interceptIntentSubmit(event, handlers),
    [handlers],
  );
}
