/**
 * React bindings for the time plan store.
 */
import type { PropsWithChildren } from "react";
import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
} from "react";

import type {
  PendingTimePlanMutation,
  TimePlanEntities,
  TimePlanEntityDelta,
  TimePlanStore,
  TimePlanStoreSources,
} from "#/core/apps/time_plans/store/store";
import {
  createTimePlanStore,
  enqueueTimePlanMutation,
  rejectTimePlanMutation,
  resolveTimePlanMutation,
  selectTimePlanEntities,
  syncTimePlanSources,
} from "#/core/apps/time_plans/store/store";

interface TimePlanStoreContextValue {
  entities: TimePlanEntities;
  // How many edits are applied locally but not yet confirmed.
  pendingMutations: number;
  enqueueMutation: (mutation: PendingTimePlanMutation) => void;
  resolveMutation: (
    mutationId: string,
    delta: TimePlanEntityDelta,
    source: string,
  ) => void;
  rejectMutation: (mutationId: string) => void;
}

const TimePlanStoreContext = createContext<TimePlanStoreContextValue | null>(
  null,
);

interface TimePlanStoreProviderProps {
  // One snapshot per loader, memoised on the loader data - a new object means
  // the loader ran again.
  sources: TimePlanStoreSources;
}

interface ProviderState {
  sources: TimePlanStoreSources;
  store: TimePlanStore;
}

export function TimePlanStoreProvider(
  props: PropsWithChildren<TimePlanStoreProviderProps>,
) {
  const [state, setState] = useState<ProviderState>(() => ({
    sources: props.sources,
    store: syncTimePlanSources(createTimePlanStore(), {}, props.sources),
  }));

  // Loader data only shows up while rendering, and the first render can be on
  // the server, so the store catches up with new sources right here instead of
  // in an effect.
  let store = state.store;
  if (state.sources !== props.sources) {
    store = syncTimePlanSources(state.store, state.sources, props.sources);
    setState({ sources: props.sources, store });
  }

  const enqueueMutation = useCallback((mutation: PendingTimePlanMutation) => {
    setState((prev) => ({
      ...prev,
      store: enqueueTimePlanMutation(prev.store, mutation),
    }));
  }, []);
  const resolveMutation = useCallback(
    (mutationId: string, delta: TimePlanEntityDelta, source: string) => {
      setState((prev) => ({
        ...prev,
        store: resolveTimePlanMutation(prev.store, mutationId, delta, source),
      }));
    },
    [],
  );
  const rejectMutation = useCallback((mutationId: string) => {
    setState((prev) => ({
      ...prev,
      store: rejectTimePlanMutation(prev.store, mutationId),
    }));
  }, []);

  const entities = useMemo(() => selectTimePlanEntities(store), [store]);
  const pendingMutations = store.pending.length;
  const value = useMemo(
    () => ({
      entities,
      pendingMutations,
      enqueueMutation,
      resolveMutation,
      rejectMutation,
    }),
    [
      entities,
      pendingMutations,
      enqueueMutation,
      resolveMutation,
      rejectMutation,
    ],
  );

  return (
    <TimePlanStoreContext.Provider value={value}>
      {props.children}
    </TimePlanStoreContext.Provider>
  );
}

export function useTimePlanStore(): TimePlanStoreContextValue {
  const value = useContext(TimePlanStoreContext);
  if (value === null) {
    throw new Error("useTimePlanStore needs a TimePlanStoreProvider above it");
  }
  return value;
}
