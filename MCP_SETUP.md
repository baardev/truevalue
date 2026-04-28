---
doc_id: mcp_setup
title: MCP Setup Guide
type: documentation
status: active
domain: project_documentation
layer: infrastructure
---

# MCP Setup Guide

This project uses two MCP (Model Context Protocol) servers that give Cursor direct access to AnythingLLM workspaces and a persistent memory graph.

## Services Overview

| Service | What it does | Starts automatically |
|---|---|---|
| Ollama | Runs local LLM models | Yes (systemd service) |
| AnythingLLM | Document workspace RAG server | No (AppImage, launch manually) |
| MCP Python wrapper | Bridges Cursor to AnythingLLM API | Yes (Cursor spawns it) |
| MCP memory server | Persistent knowledge graph for Cursor | Yes (Cursor spawns it) |

---

## After Every Reboot

Only one manual step is required:

```bash
/home/jw/AnythingLLMDesktop.AppImage &
```

Wait about 15 seconds for the backend to initialize on port 3001, then open Cursor normally. The MCP servers start automatically when you open a chat.

### Optional: autostart AnythingLLM on login

To eliminate the manual step entirely, create a desktop autostart entry:

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/anythingllm.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=AnythingLLM
Exec=/home/jw/AnythingLLMDesktop.AppImage
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
```

---

## MCP Server Configuration

Config file: `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "anythingllm": {
      "command": "/home/jw/miniforge3/bin/python3",
      "args": ["/home/jw/src/tv/scripts/anythingllm_mcp_server.py"],
      "env": {
        "ANYTHINGLLM_API_KEY": "2D0A7FZ-Z5MMGKS-PMCXE6Q-6Y196XE",
        "ANYTHINGLLM_BASE_URL": "http://localhost:3001"
      }
    },
    "obsidian": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian", "/home/jw/src/tv"]
    }
  }
}
```

The MCP wrapper script is at `scripts/anythingllm_mcp_server.py`.

---

## AnythingLLM Workspaces

| Name | Slug | Contents |
|---|---|---|
| Tholonia Book | `my-workspace` | Full Tholonia book chapters |
| LegallyBlind | `legallyblind` | LegallyBlind project documents |
| TrueValue Analytics Documents | `truevalue-analytics-documents` | Project research and analysis docs |

---

## Available MCP Tools

### anythingllm server

| Tool | Description |
|---|---|
| `list_workspaces` | List all available workspaces and their slugs |
| `query_workspace` | Send a question to a workspace and get an answer grounded in its documents |
| `list_workspace_documents` | List all documents embedded in a workspace |

Example usage in Cursor chat:

- "List my AnythingLLM workspaces"
- "Query the truevalue-analytics-documents workspace: what are the key findings on blue carbon?"
- "Query the Tholonia Book workspace: explain the N-D-C triadic structure"
- "List documents in the my-workspace workspace"

### memory server

Provides a persistent knowledge graph across Cursor sessions. Tools: `create_entities`, `create_relations`, `add_observations`, `search_nodes`, `read_graph`, `open_nodes`, `delete_entities`, `delete_observations`, `delete_relations`.

### obsidian server

Reads directly from the Obsidian vault at `/home/jw/src/tv` (this project is the vault). No Obsidian plugin required. Tools expose note search and read operations.

Example usage:

- "Search my Obsidian vault for notes about blue carbon"
- "Read the note frontend/docs/ai_notes/concept_notes/mrv.md"
- "List all notes in frontend/docs/ai_notes/concept_notes/"

---

## Troubleshooting

### AnythingLLM not responding (port 3001 closed)

Check if it is running:

```bash
curl -s http://localhost:3001/api/v1/auth \
  -H "Authorization: Bearer 2D0A7FZ-Z5MMGKS-PMCXE6Q-6Y196XE"
```

If connection refused, relaunch:

```bash
pkill -9 -f "anythingllm-desktop" && pkill -9 -f "AnythingLLMDesktop"
sleep 2
/home/jw/AnythingLLMDesktop.AppImage &
```

Wait for the backend to come up:

```bash
until curl -s http://localhost:3001/api/v1/auth | grep -q authenticated; do
  sleep 2; echo "waiting..."
done && echo "AnythingLLM is ready"
```

### MCP server shows red dot in Cursor

Go to Settings > MCP and click the refresh icon on the `anythingllm` entry. If it stays red, check that AnythingLLM is running on port 3001 first.

### Ollama not running

```bash
sudo systemctl start ollama
sudo systemctl status ollama
```

Models are stored in `/data/ollama/models` (owned by the `ollama` system user). The workspace currently uses `qwen3:1.7b` for fast responses.

---

## LLM Model Notes

The workspace LLM is configured per-workspace inside AnythingLLM (Settings > workspace pencil icon > LLM Provider).

| Model | Size | Speed | Notes |
|---|---|---|---|
| `qwen3:1.7b` | ~1 GB | Fast (5-10s) | Recommended for MCP queries |
| `qwen3:latest` | 5.2 GB | Slow (60-90s) | Too slow for MCP, causes timeouts |
| Anthropic Claude | API | Very fast (2-5s) | Requires Anthropic API key (already configured) |

For reliable MCP queries, use `qwen3:1.7b` or Anthropic Claude as the workspace LLM.
