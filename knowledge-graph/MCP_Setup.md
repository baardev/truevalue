# MCP Setup

**Type:** infrastructure

## Config File

`.cursor/mcp.json`

## Three Servers

| Server | Command | Purpose |
|---|---|---|
| `memory` | `npx @modelcontextprotocol/server-memory` | Persistent knowledge graph |
| `anythingllm` | `/home/jw/miniforge3/bin/python3 scripts/anythingllm_mcp_server.py` | AnythingLLM workspace queries |
| `obsidian` | `npx mcp-obsidian /home/jw/src/tv` | Vault note search and read |

## Important

- Use `/home/jw/miniforge3/bin/python3` (not system `python3`) for the AnythingLLM server
- Full setup documentation: `MCP_SETUP.md`

## Connects To

- [[AnythingLLM]]
- [[Obsidian_Vault]]
