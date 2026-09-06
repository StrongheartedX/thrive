import type { ChoreStack } from "@jupiter/webapi-client";

import { LinkTag } from "#/core/infra/component/link-tag";

interface Props {
  choreStack: ChoreStack;
}

export function ChoreStackTag(props: Props) {
  return <LinkTag label={props.choreStack.name} color="info" />;
}
