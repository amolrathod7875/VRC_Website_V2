import { redirect } from "next/navigation";

export default function GlobalPresenceRedirect() {
  redirect("/about#global-presence");
}
