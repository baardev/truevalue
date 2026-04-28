# AnythingLLM

**Type:** service

## Connection

- AppImage: `/home/jw/AnythingLLMDesktop.AppImage`
- API: `http://localhost:3001`
- API key: `2D0A7FZ-Z5MMGKS-PMCXE6Q-6Y196XE`

## Startup

Must be launched manually after reboot:
```bash
/home/jw/AnythingLLMDesktop.AppImage &
```

## Workspaces

- [[Tholonia_Workspace]] (slug: `my-workspace`)
- `LegallyBlind` (slug: `legallyblind`)
- [[TrueValue_Workspace]] (slug: `truevalue-analytics-documents`)

## LLM Model Notes

| Model | Speed | Status |
|---|---|---|
| `qwen3:1.7b` | Fast (5-10s) | Recommended |
| `qwen3:latest` (8B) | Slow (60-90s) | Causes backend crashes - avoid for MCP |
| Anthropic Claude | Very fast (2-5s) | API key configured, alternative option |

## Dependencies

- [[Ollama]]
- [[MCP_Setup]]
