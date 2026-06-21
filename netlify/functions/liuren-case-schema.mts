import data from "./_shared/kb-data.mjs";
import { errorResponse, jsonResponse } from "./_shared/search-core.mjs";

export default async (req: Request) => {
  if (req.method !== "GET") {
    return errorResponse("Method not allowed", 405);
  }

  return jsonResponse({
    built_at: data.built_at,
    schema: data.liuren_case_schema,
  });
};

export const config = {
  path: "/api/liuren-case-schema",
  method: ["GET"],
};
