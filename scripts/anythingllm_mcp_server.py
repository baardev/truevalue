#!/usr/bin/env python3
"""MCP server that exposes AnythingLLM workspaces as queryable tools for Cursor.

Environment variables (required):
    ANYTHINGLLM_API_KEY   API key from AnythingLLM Settings > Tools > Developer API
    ANYTHINGLLM_BASE_URL  Default: http://localhost:3001

Usage (stdio, called by Cursor via mcp.json):
    python3 scripts/anythingllm_mcp_server.py
"""

import json
import os
import sys
import urllib.request
import urllib.error

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

BASE_URL = os.environ.get("ANYTHINGLLM_BASE_URL", "http://localhost:3001")
API_KEY = os.environ.get("ANYTHINGLLM_API_KEY", "")


def _api(path: str, method: str = "GET", body: dict | None = None) -> dict:
    url = f"{BASE_URL}/api/v1/{path.lstrip('/')}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Connection": "close",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        return {"error": f"HTTP {exc.code}: {exc.reason}"}
    except Exception as exc:
        return {"error": str(exc)}


server = Server("anythingllm")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_workspaces",
            description=(
                "List all AnythingLLM workspaces available on the local instance. "
                "Returns workspace names and their slug identifiers."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="query_workspace",
            description=(
                "Send a question or prompt to an AnythingLLM workspace and get an "
                "answer grounded in the documents embedded in that workspace. "
                "Use list_workspaces first to find the correct slug."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "slug": {
                        "type": "string",
                        "description": (
                            "Workspace slug (e.g. 'truevalue-analytics-documents'). "
                            "Use list_workspaces to discover available slugs."
                        ),
                    },
                    "message": {
                        "type": "string",
                        "description": "The question or prompt to send to the workspace.",
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["query", "chat"],
                        "description": (
                            "'query' returns answers only from embedded documents. "
                            "'chat' uses both documents and LLM knowledge. "
                            "Default: query"
                        ),
                    },
                },
                "required": ["slug", "message"],
            },
        ),
        types.Tool(
            name="list_workspace_documents",
            description=(
                "List the documents embedded in a specific AnythingLLM workspace. "
                "Useful to understand what sources are available before querying."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "slug": {
                        "type": "string",
                        "description": "Workspace slug (from list_workspaces).",
                    }
                },
                "required": ["slug"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if not API_KEY:
        return [types.TextContent(
            type="text",
            text="Error: ANYTHINGLLM_API_KEY environment variable is not set.",
        )]

    if name == "list_workspaces":
        result = _api("workspaces")
        if result.get("error"):
            text = f"Error: {result['error']}"
        else:
            workspaces = result.get("workspaces", [])
            lines = [f"- {w['name']} (slug: {w['slug']})" for w in workspaces]
            text = "Available workspaces:\n" + "\n".join(lines)

    elif name == "query_workspace":
        slug = arguments["slug"]
        message = arguments["message"]
        mode = arguments.get("mode", "query")
        result = _api(
            f"workspace/{slug}/chat",
            method="POST",
            body={"message": message, "mode": mode},
        )
        if result.get("error"):
            text = f"Error: {result['error']}"
        else:
            text = result.get("textResponse") or result.get("response") or json.dumps(result)

    elif name == "list_workspace_documents":
        slug = arguments["slug"]
        result = _api(f"workspace/{slug}")
        if result.get("error"):
            text = f"Error: {result['error']}"
        else:
            workspace = result.get("workspace", {})
            docs = workspace.get("documents", [])
            if not docs:
                text = f"No documents found in workspace '{slug}'."
            else:
                lines = [f"- {d.get('title', d.get('docpath', 'unknown'))}" for d in docs]
                text = f"Documents in '{slug}' ({len(docs)} total):\n" + "\n".join(lines)

    else:
        text = f"Unknown tool: {name}"

    return [types.TextContent(type="text", text=text)]


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
