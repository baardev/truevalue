# Cognee Notes

## Graph Visualization Customization

### Source file to edit

```
/home/jw/src/cognee/cognee/modules/visualization/cognee_network_visualization.py
```

(Cognee is installed as an editable local clone at `/home/jw/src/cognee`, not in the system site-packages.)

GitHub reference:
https://github.com/topoteretes/cognee/blob/main/cognee/modules/visualization/cognee_network_visualization.py

---

### What this file does

This is the file that generates the interactive HTML graph you see in the Cognee UI and via `visualize_graph()`. It uses D3.js (v7) embedded in a self-contained HTML file.

---

### Node color map (lines 25-36)

This dictionary maps node types to hex colors. Edit these values to change node colors:

```python
color_map = {
    "Entity":             "#6510F4",   # purple
    "EntityType":         "#A550FF",   # lighter purple
    "DocumentChunk":      "#0DFF00",   # bright green
    "TextSummary":        "#6510F4",   # purple
    "TableRow":           "#A550FF",
    "TableType":          "#6510F4",
    "ColumnValue":        "#747470",   # grey
    "SchemaTable":        "#A550FF",
    "DatabaseSchema":     "#6510F4",
    "SchemaRelationship": "#323332",
    "default":            "#7c3aed",   # violet fallback
}
```

To add your own node types with custom colors, add entries to this dictionary. For example:

```python
"Location":      "#FF6B00",   # orange
"Commodity":     "#00C8FF",   # cyan
"Organization":  "#FFD700",   # gold
"Concept":       "#FF3366",   # red
```

---

### 2-hop neighbor highlighting (HIGHLIGHT_DEPTH)

/home/jw/src/cognee/cognee/modules/visualization/cognee_network_visualization.py

The visualization now uses a configurable BFS depth for node highlighting on hover. The variable is near the top of the `draw()` function:

```javascript
var HIGHLIGHT_DEPTH = 2;
```

- `1` = original behavior (only direct neighbors highlighted)
- `2` = direct neighbors AND their neighbors (default after edit)
- `3+` = will light up large portions of a dense graph, use with caution

The BFS loop builds `neighborSet` by walking `adjMap` outward for `HIGHLIGHT_DEPTH` hops. Edges where both endpoints are in `neighborSet` are also highlighted at reduced opacity (`alpha=0.35`, `lineW=1.0`), while edges directly touching the hovered node remain at full brightness (`alpha=0.6`, `lineW=1.5`).

To change depth, search for `var HIGHLIGHT_DEPTH=` in the source file above and change the value, then regenerate the graph HTML with `visualize_graph()`.

---

### Edge thickness (line ~498)

Edge stroke width is currently hardcoded:

```javascript
.attr('stroke-width', 1.5)
```

Change `1.5` to any value to make edges thicker or thinner. Edge weight values (if present on your data) can also drive thickness dynamically.

---

### Color-by modes (built into the UI)

The visualization already has buttons to switch node coloring by:

| Button | Colors nodes by |
|--------|----------------|
| Type | Node type (Entity, DocumentChunk, etc.) |
| Task | Which cognify task created the node |
| Pipeline | Which pipeline it came from |
| Node Set | Which node set it belongs to |
| User | Which user ingested the data |

To use pipeline or node set coloring meaningfully, run separate `cognify()` calls with different pipeline/nodeset names for each topic (e.g. shea, olive oil, argentina). Each will get its own auto-generated color.

---

### Editing the generated HTML directly (no Python needed)

Every time you call `visualize_graph()` it produces a plain HTML file. You can open that file in a text editor, find the `color_map` JavaScript object, change hex values, save, and refresh in the browser. This is a one-off edit and does not affect future generations.

Default output location if no path is specified:

```
~/graph_visualization.html
```

Custom path example:

```python
from cognee.api.v1.visualize.visualize import visualize_graph
await visualize_graph("./my_graph.html")
```

---

### Cognee docs references

- Graph visualization guide: https://docs.cognee.ai/guides/graph-visualization
- Graph stores (backends): https://docs.cognee.ai/setup-configuration/graph-stores.md
- Vector stores: https://docs.cognee.ai/setup-configuration/vector-stores.md
- Custom data models: https://docs.cognee.ai/guides/custom-data-models.md
- Infer schema from text: https://docs.cognee.ai/api-reference/llm/infer-schema.md
- Dataset schema (get/set): https://docs.cognee.ai/api-reference/datasets/get-dataset-schema.md
