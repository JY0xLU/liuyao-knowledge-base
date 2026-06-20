import data from "./_shared/kb-data.mjs";
import { errorResponse, jsonResponse, searchKnowledgeBase } from "./_shared/search-core.mjs";

export default async (req: Request) => {
  if (req.method !== "GET") {
    return errorResponse("Method not allowed", 405);
  }

  const url = new URL(req.url);
  const payload = searchKnowledgeBase(data, {
    query: url.searchParams.get("q") || "",
    kind: url.searchParams.get("kind") || "",
    limit: url.searchParams.get("limit") || "30",
  });

  return jsonResponse({
    built_at: data.built_at,
    ...payload,
  });
};

export const config = {
  path: "/api/search",
  method: ["GET"],
};
