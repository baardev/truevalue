# Ollama

**Type:** service

## Connection

- Port: `11434`
- Models directory: `/data/ollama/models` (owned by `ollama` system user)
- Starts automatically on boot via systemd

## Downloaded Models

| Model | Size | Notes |
|---|---|---|
| `qwen3:1.7b` | ~1 GB | Recommended for AnythingLLM MCP |
| `qwen3:latest` | 5.2 GB | Too slow/unstable for MCP queries |
| `gpt-4o-mini:latest` | 9.6 GB | Available |
| `gemma4:latest` | 9.6 GB | Available |

## Used By

- [[AnythingLLM]]
