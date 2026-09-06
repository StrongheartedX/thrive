import type {
  EntityId,
  Chore,
  RecurringTaskPeriod,
} from "@jupiter/webapi-client";
import { Autocomplete, TextField } from "@mui/material";
import { useEffect, useMemo, useState } from "react";

import { autocompleteSingleLineSx } from "#/core/common/component/autocomplete";
import { PeriodTag } from "#/core/common/component/period-tag";
import { sortChoresNaturally } from "#/core/apps/chores/root";

interface ChoreSelectMultipleProps {
  name: string;
  label: string;
  allChores: Chore[];
  defaultValue?: EntityId[];
  value?: EntityId[];
  onChange?: (value: EntityId[]) => void;
  filterPeriod?: RecurringTaskPeriod;
  inputsEnabled?: boolean;
}

export function ChoreSelectMultiple(props: ChoreSelectMultipleProps) {
  const filteredChores = useMemo(() => {
    const matching = props.filterPeriod
      ? props.allChores.filter(
          (chore) => chore.gen_params.period === props.filterPeriod,
        )
      : props.allChores;
    return sortChoresNaturally(matching);
  }, [props.allChores, props.filterPeriod]);

  const allChoresByRefId = useMemo(
    () => new Map(filteredChores.map((chore) => [chore.ref_id, chore])),
    [filteredChores],
  );

  const [selectedChores, setSelectedChores] = useState(
    selectedChoresToOptions(props.value, props.defaultValue, allChoresByRefId),
  );

  useEffect(() => {
    setSelectedChores(
      selectedChoresToOptions(
        props.value,
        props.defaultValue,
        allChoresByRefId,
      ),
    );
  }, [props.value, props.defaultValue, props.allChores, allChoresByRefId]);

  return (
    <>
      <Autocomplete
        autoHighlight
        multiple
        filterSelectedOptions
        disabled={props.inputsEnabled === false}
        id={props.name}
        options={filteredChores.map(choreToOption)}
        sx={autocompleteSingleLineSx}
        value={selectedChores}
        onChange={(e, v) => {
          setSelectedChores(v);
          if (props.onChange) {
            props.onChange(v.map((option) => option.chore_ref_id));
          }
        }}
        isOptionEqualToValue={(o, v) => o.chore_ref_id === v.chore_ref_id}
        getOptionLabel={(option) => option.label}
        renderOption={(optionProps, option) => (
          <li
            {...optionProps}
            key={option.chore_ref_id}
            style={{ display: "flex", alignItems: "center", gap: 1 }}
          >
            {option.label} <PeriodTag period={option.period} />
          </li>
        )}
        renderInput={(params) => <TextField {...params} label={props.label} />}
      />
      <input
        type="hidden"
        name={props.name}
        value={selectedChores.map((option) => option.chore_ref_id).join(",")}
      />
    </>
  );
}

function selectedChoresToOptions(
  value: EntityId[] | undefined,
  defaultValue: EntityId[] | undefined,
  allChoresByRefId: Map<EntityId, Chore>,
) {
  const choreRefIds = value ?? defaultValue ?? [];
  return choreRefIds
    .map((refId) => allChoresByRefId.get(refId))
    .filter((chore): chore is Chore => chore !== undefined)
    .map(choreToOption);
}

function choreToOption(chore: Chore) {
  return {
    chore_ref_id: chore.ref_id,
    label: chore.name,
    period: chore.gen_params.period,
  };
}
