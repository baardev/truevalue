# Obsidian Vault

**Type:** infrastructure

## Location

`/home/jw/src/tv` - the project IS the vault.

The `.obsidian` config folder is at `/home/jw/src/tv/.obsidian`.

## MCP Access

```json
{
  "obsidian": {
    "command": "npx",
    "args": ["-y", "mcp-obsidian", "/home/jw/src/tv"]
  }
}
```

No Obsidian plugin required. The MCP server reads vault files directly.

## Example Cursor Queries

- "Search my Obsidian vault for notes about blue carbon"
- "Read the note frontend/docs/ai_notes/concept_notes/mrv.md"
- "List all notes in frontend/docs/ai_notes/concept_notes/"

## Part Of

- [[Project]]
- [[MCP_Setup]]
