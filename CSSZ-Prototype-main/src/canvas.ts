import { Request, BodyInit } from "node-fetch";
import { CANVAS_BASE_URL } from "./const";

/**
 * Initialises a request for the Canvas API.
 *
 * @param url The API endpoint.
 * @param body Optionally, data to send as the request body.
 * @param verb Optionally, the HTTP verb to use.
 * @returns Returns the initialised request.
 */
export function makeCanvasRequest(
  url: string,
  body?: BodyInit | undefined,
  verb?: "GET" | "POST" | "DELETE" | "PUT",
): Request {
  const request = new Request(`${CANVAS_BASE_URL}/${url}`, {
    method: verb === undefined ? (body === undefined ? "GET" : "POST") : verb,
    body,
  });
  request.headers.append("Authorization", `Bearer ${process.env.CANVAS_TOKEN}`);
  return request;
}
