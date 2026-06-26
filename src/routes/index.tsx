import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "My Site" },
      { name: "description", content: "My site." },
      { property: "og:title", content: "My Site" },
      { property: "og:description", content: "My site." },
    ],
  }),
  component: Index,
});

function Index() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <h1 className="text-2xl font-semibold text-foreground">Hello world</h1>
    </div>
  );
}
