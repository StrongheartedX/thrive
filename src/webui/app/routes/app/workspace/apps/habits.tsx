import type { LoaderFunctionArgs } from "@remix-run/node";
import { json, redirect } from "@remix-run/node";
import { Outlet } from "@remix-run/react";

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const pathname = url.pathname.replace(/\/$/, "");
  if (pathname === "/app/workspace/apps/habits") {
    return redirect(`/app/workspace/apps/habits/habits${url.search}`);
  }
  return json({});
}

export default function HabitsLayout() {
  return <Outlet />;
}
