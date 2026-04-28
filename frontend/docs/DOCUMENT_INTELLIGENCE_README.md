---
doc_id: frontend_docs_document_intelligence_readme
title: Document Intelligence Setup
type: readme
status: active
domain: project_documentation
layer: operations
projects:
  []
tags:
  - operations
  - project_documentation
related_docs:
  []
key_claims:
  []
---

# Document Intelligence Setup

This guide describes how to organize the documents in this repository as a lightweight knowledge system that can be used by both humans and AI.

The recommended approach is a hybrid document intelligence layer:

- Markdown remains the source format.
- Obsidian provides backlinks, graph navigation, and human concept mapping.
- MkDocs provides the publishable documentation site.
- A document registry provides structured metadata for AI.
- A relationship table records explicit document-to-document links.
- AnythingLLM provides chat with the document corpus.
- Optional custom RAG can be added later if AnythingLLM is not enough.

## 1. Problem This Solves

The project contains many documents across research papers, reports, schemas, project pages, templates, and methodology notes. A normal folder tree is not enough because the important information is relational.

The system should answer:

- What is this document?
- What project does it belong to?
- What analytical layer does it belong to?
- What other documents does it depend on?
- What documents extend, support, or supersede it?
- What claims does it make?
- What should AI remember when using it?

The goal is not only search. The goal is structured memory, concept mapping, and reliable chat with the documents.

## 2. Recommended Architecture

Use five layers:

1. **Documents**
   - Markdown, HTML, PDF, CSV, YAML, and other source files already in the repository.

2. **Metadata**
   - YAML frontmatter in important Markdown files.
   - A central `doc_registry.yaml` file.

3. **Relationships**
   - A `doc_relationships.csv` file that records explicit document links.
   - Obsidian wiki links for human navigation.

4. **Retrieval**
   - Obsidian search and graph view for human navigation.
   - MkDocs search for published documentation.
   - AnythingLLM for chat over the curated document corpus.

5. **Chat**
   - AnythingLLM workspaces should ingest the curated Markdown notes, document registry, claims registry, relationship table, and selected source documents.
   - Chat should use the metadata layer to avoid confusing drafts, archived files, superseded documents, and unrelated analytical layers.

This avoids a common RAG problem: retrieving text without knowing the document's role, status, layer, or relationship to other documents. AnythingLLM is the chat interface, but the repository remains the source of truth.

## 3. Install Core Tools On Arch Linux

Install common command-line tools:

```bash
sudo pacman -S ripgrep fd jq yq graphviz
```

Install Obsidian.

If Obsidian is available from your configured repositories:

```bash
sudo pacman -S obsidian
```

If Obsidian is not available, install it from the AUR using your preferred AUR helper:

```bash
yay -S obsidian
```

or:

```bash
paru -S obsidian
```

On Manjaro, you may also use:

```bash
pamac build obsidian
```

Optional tools:

```bash
sudo pacman -S sqlitebrowser
```

## 4. Install And Configure AnythingLLM For Document Chat

Use AnythingLLM as the chat layer over the curated document corpus. Obsidian organizes the knowledge graph. AnythingLLM lets you ask questions against the documents.

There are two practical installation paths on Arch Linux or Manjaro.

### Option A: Desktop App

Install the AnythingLLM desktop application from the official AnythingLLM release page or from the AUR if an up-to-date package is available in your environment.

Check the AUR:

```bash
yay -Ss anythingllm
```

If a maintained desktop package is available:

```bash
yay -S anythingllm-desktop-bin
```

Package names can change, so verify the package before installing.

### Option B: Docker

Install Docker:

```bash
sudo pacman -S docker docker-compose
sudo systemctl enable docker
sudo systemctl start docker
```

Add your user to the Docker group if you want to run Docker without `sudo`:

```bash
sudo usermod -aG docker "$USER"
```

Log out and back in after changing group membership.

Then follow the current AnythingLLM Docker instructions from the official project documentation. Prefer mounting a persistent storage directory under the repo-adjacent workspace, not inside source-controlled project folders.

Example storage location:

```text
/home/jw/.local/share/anythingllm-tv
```

Do not store AnythingLLM databases, embeddings, or uploaded document copies inside Git unless you intentionally want them versioned.

### Recommended AnythingLLM Workspace

Create one workspace for this repository:

```text
TrueValue Analytics Documents
```

Add these sources first:

```text
frontend/docs/DOCUMENT_INTELLIGENCE_README.md
frontend/docs/doc_registry.yaml
frontend/docs/doc_relationships.csv
frontend/docs/doc_claims.yaml
frontend/docs/ai_notes/
frontend/docs/Research/modeling/
frontend/docs/Research/archive/
frontend/docs/Reports/
frontend/docs/Repos/intra/
```

Start with curated Markdown and AI notes before ingesting every PDF and generated HTML file. This gives better answers because the chat system sees summaries, document roles, claims, and relationships before raw bulk content.

Recommended ingestion priority:

1. AI notes.
2. Document registry.
3. Claims registry.
4. Relationship table.
5. Core methodology Markdown files.
6. Project-specific Markdown files.
7. Selected PDFs and HTML reports.

Avoid ingesting generated `viewable/` output at first. It may duplicate source content and make retrieval noisier.

### Recommended Chat Rules

Use a workspace instruction similar to this:

```text
You are answering questions about the TrueValue Analytics repository. Prefer active and reviewed documents. Treat Tholonic N-D-C patterns and relationships as fundamental to this model. The primary analytical task is to identify patterns of Negotiation, Definition, Contribution, D-C balance, phase coherence, recursion, opacity, lifecycle maintenance, and cross-phase propagation. Preserve the distinction between supply chain, system lifecycle, value chain, and financial abstraction. Use document IDs, paths, and relationship metadata when available. If a document is marked draft, archived, or superseded, say so. Do not infer financial claims from supply-chain documents unless the value-chain layer is explicitly in scope.
```

This makes AnythingLLM behave more like a project-aware research assistant rather than a generic document chatbot.

## 5. Configure The Project Conda Environment

Use Conda for the project Python environment. From the repository root:

```bash
cd /home/jw/src/tv
conda create -n tv-docs python=3.11
conda activate tv-docs
pip install -r requirements-docs.txt
```

If you already have a Conda environment for this repository, activate that environment instead of creating `tv-docs`:

```bash
cd /home/jw/src/tv
conda activate <your-existing-env>
pip install -r requirements-docs.txt
```

Using Conda keeps the documentation tooling separate from system Python while matching the project workflow.

## 6. Open The Repository As An Obsidian Vault

1. Open Obsidian.
2. Choose **Open folder as vault**.
3. Select:

```text
/home/jw/src/tv
```

4. Obsidian will treat the repository as a vault.

Recommended Obsidian core features:

- Backlinks
- Outgoing links
- Graph view
- Search
- Templates
- Tags

Recommended community plugins:

- Dataview, for querying Markdown metadata.
- Obsidian Git, for seeing document changes from inside Obsidian.
- Advanced Tables, for editing CSV-like Markdown tables.

Keep plugins minimal at first. The registry and relationship files should work even without plugins.

## 7. Proposed Folder Structure

Create the document intelligence layer under `frontend/docs/` so it can also be included in MkDocs.

Recommended structure:

```text
frontend/docs/
  DOCUMENT_INTELLIGENCE_README.md
  doc_registry.yaml
  doc_relationships.csv
  doc_claims.yaml
  ai_notes/
    README.md
    document_notes/
    concept_notes/
    project_notes/
```

Use this convention:

- `doc_registry.yaml` records what each document is.
- `doc_relationships.csv` records how documents relate to one another.
- `doc_claims.yaml` records reusable claims and where they are supported.
- `ai_notes/document_notes/` stores one AI note per important document.
- `ai_notes/concept_notes/` stores reusable concept notes.
- `ai_notes/project_notes/` stores project-level summaries.

## 8. Document Frontmatter Standard

Add YAML frontmatter to important Markdown documents.

Example body to place inside the standard Markdown frontmatter delimiter lines:

```yaml
doc_id: clarity_vs_kpmg_tvf
title: Clarity True Value Framework and KPMG True Value
type: research_paper
status: draft
domain: true_value_framework
layer: methodology
projects:
  - gold
  - shea
  - aubeb
tags:
  - true_value
  - kpmg
  - clarity
  - esg
  - ndc
related_docs:
  - tholonic_framework_supply_value_chain
  - sustainability_linked_loan_framework
key_claims:
  - clarity_preserves_adaptive_system_data
  - kpmg_monetizes_externalities
  - corporate_materiality_can_filter_system_signals
```

Recommended frontmatter fields:

```yaml
doc_id:
title:
type:
status:
domain:
layer:
project:
phase_id:
tags:
related_docs:
key_claims:
source_role:
```

Use `phase_id` only when a document maps to a specific supply-chain or value-chain phase.

Use `layer` to preserve the project's analytical separation:

```text
supply_chain
system_lifecycle
value_chain
financial_abstraction
methodology
research
operations
```

## 9. Document Registry

Create:

```text
frontend/docs/doc_registry.yaml
```

Example:

```yaml
documents:
  - doc_id: clarity_vs_kpmg_tvf
    title: Clarity True Value Framework and KPMG True Value
    path: frontend/docs/Research/modeling/CLARITY_TRUE_VALUE_VS_KPMG_TRUE_VALUE.md
    html_path: frontend/docs/Research/modeling/CLARITY_TRUE_VALUE_VS_KPMG_TRUE_VALUE.html
    type: research_paper
    status: draft
    domain: true_value_framework
    layer: methodology
    projects:
      - gold
      - shea
      - aubeb
    summary: >
      Compares Clarity True Value Framework with KPMG True Value, focusing on externality
      monetization, system coherence, ESG prerequisite screening, adaptive-system data,
      and long-duration investment analysis.
```

Recommended document types:

```text
research_paper
methodology
report
brief
schema
template
project_page
api_reference
source_note
ai_note
```

Recommended statuses:

```text
draft
active
reviewed
superseded
archived
external
```

## 10. Relationship Table

Create:

```text
frontend/docs/doc_relationships.csv
```

Example:

```csv
source_doc,target_doc,relationship_type,reason
clarity_vs_kpmg_tvf,tholonic_framework_supply_value_chain,extends,N-D-C framework provides conceptual foundation
clarity_vs_kpmg_tvf,sustainability_linked_loan_framework,supports,ESG screening logic informs sustainability-linked finance
clarity_vs_kpmg_tvf,tvf_research_agenda,informs,Identifies research gaps around true value methodology
```

Recommended relationship types:

```text
extends
supports
depends_on
summarizes
supersedes
contrasts_with
applies_to
derived_from
needs_review
```

The relationship table should be conservative. Add relationships only when there is a meaningful analytical connection.

## 11. Claims Registry

Create:

```text
frontend/docs/doc_claims.yaml
```

Example:

```yaml
claims:
  - claim_id: clarity_preserves_adaptive_system_data
    statement: >
      Clarity preserves pre-financial adaptive-system signals by mapping process structure
      before filtering impacts through corporate materiality or monetized value.
    supported_by:
      - clarity_vs_kpmg_tvf
    related_concepts:
      - adaptive_system_data
      - corporate_materiality
      - system_coherence

  - claim_id: kpmg_monetizes_externalities
    statement: >
      KPMG True Value is strongest when identified economic, social, and environmental
      externalities can be translated into financial terms.
    supported_by:
      - clarity_vs_kpmg_tvf
```

The claims registry helps AI avoid treating every paragraph as equal. It highlights the reusable claims that matter.

## 12. AI Notes

Create one AI note for each important document.

Example path:

```text
frontend/docs/ai_notes/document_notes/clarity_vs_kpmg_tvf.md
```

Template:

```markdown
# AI Note: Clarity True Value vs KPMG True Value

## Document ID

clarity_vs_kpmg_tvf

## One-Sentence Summary

Compares Clarity TVF as a system-coherence framework with KPMG True Value as a monetized externality framework.

## Key Claims

- KPMG is strongest after impacts can be bounded and monetized.
- Clarity is strongest before monetization, when system coherence must be tested.
- Corporate materiality boundaries can filter out adaptive-system data.
- Clarity preserves pre-financial signals such as feedback loops, stewardship, maintenance, phase dependencies, and resilience.

## Related Documents

- tholonic_framework_supply_value_chain
- sustainability_linked_loan_framework
- tvf_research_agenda

## AI Handling Notes

When using this document, preserve the distinction between:

- system structure
- lifecycle maintenance
- value-chain interpretation
- financial abstraction
```

## 13. Concept Notes

Create a note for recurring concepts.

Examples:

```text
frontend/docs/ai_notes/concept_notes/adaptive_system_data.md
frontend/docs/ai_notes/concept_notes/corporate_materiality.md
frontend/docs/ai_notes/concept_notes/ndc_balance.md
frontend/docs/ai_notes/concept_notes/system_coherence.md
```

Concept note template:

```markdown
# Adaptive System Data

## Definition

Signals inside a living, ecological, social, infrastructure, or institutional system that describe feedback, resilience, maintenance, phase dependency, or coherence before those signals become monetized impacts.

## Why It Matters

Corporate materiality filters can miss weak signals that are structurally important but not yet financially visible.

## Related Documents

- [[clarity_vs_kpmg_tvf]]

## Related Claims

- clarity_preserves_adaptive_system_data
- corporate_materiality_can_filter_system_signals
```

## 14. Obsidian Linking Convention

Use Obsidian wiki links for concept notes and AI notes:

```markdown
[[adaptive_system_data]]
[[corporate_materiality]]
[[clarity_vs_kpmg_tvf]]
[[ndc_balance]]
```

Use normal Markdown links for published documents:

```markdown
[Clarity True Value vs KPMG True Value](Research/modeling/CLARITY_TRUE_VALUE_VS_KPMG_TRUE_VALUE.md)
```

Use both when helpful:

```markdown
See [[adaptive_system_data]] and the published paper:
[Clarity True Value vs KPMG True Value](../Research/modeling/CLARITY_TRUE_VALUE_VS_KPMG_TRUE_VALUE.md).
```

## 15. Daily Use Workflow

When adding or editing a major document:

1. Add YAML frontmatter.
2. Add or update the document in `doc_registry.yaml`.
3. Add meaningful relationships in `doc_relationships.csv`.
4. Add reusable claims in `doc_claims.yaml`.
5. Add an AI note if the document is important.
6. Add concept links where the document introduces or depends on recurring concepts.
7. Rebuild generated HTML and MkDocs if the document is published.

Useful commands from the repository root:

```bash
cd /home/jw/src/tv
./scripts/md2html.sh frontend/docs/Research/modeling/CLARITY_TRUE_VALUE_VS_KPMG_TRUE_VALUE.md
RUN_MKDOCS=1 ./scripts/rebuild-site.sh
```

## 16. Ingesting Documents Into AnythingLLM

Use the manifest-driven ingestion script when you want to upload many files into AnythingLLM.

Before ingestion, convert raw inbox files into clean Markdown and CSV outputs:

```bash
python scripts/convert_inbox_sources.py -dry-run -since-marker NOW
python scripts/convert_inbox_sources.py -since-marker NOW
```

To convert one file in place, pass the file path directly. The output is written beside the input with the converted extension:

```bash
python scripts/convert_inbox_sources.py "NEW/example.docx"
python scripts/convert_inbox_sources.py "NEW/example.xlsx"
python scripts/convert_inbox_sources.py -file "NEW/example.docx"
```

This script converts `.docx`, `.doc`, `.html`, `.xlsx`, and `.xls` files from `NEW/` into curated Markdown source notes and CSV tables. Office conversion for `.doc` and `.xls` requires LibreOffice. Excel conversion requires `openpyxl`, which is included in `requirements-docs.txt`.

The starter manifest is:

```text
frontend/docs/anythingllm_manifest.yaml
```

The ingestion script is:

```text
scripts/anythingllm_ingest.py
```

Set API access through environment variables:

```bash
export ANYTHINGLLM_BASE_URL="http://localhost:3001"
export ANYTHINGLLM_API_KEY="paste-your-anythingllm-api-key-here"
export ANYTHINGLLM_WORKSPACE="truevalue-analytics-documents"
```

For this repository, `ANYTHINGLLM_BASE_URL` should be `http://localhost:3001` if AnythingLLM is running locally. `ANYTHINGLLM_WORKSPACE` should match the workspace slug expected by the starter manifest: `truevalue-analytics-documents`.

The only value you must get from AnythingLLM is `ANYTHINGLLM_API_KEY`. In AnythingLLM, open the API or developer settings, create an API key, and paste it into the shell session before running the script. Do not save the API key in Git.

Run a dry run first:

```bash
cd /home/jw/src/tv
python scripts/anythingllm_ingest.py -n
```

Upload the selected files:

```bash
cd /home/jw/src/tv
python scripts/anythingllm_ingest.py
```

Use a custom manifest:

```bash
python scripts/anythingllm_ingest.py -m frontend/docs/anythingllm_manifest.yaml
```

Process only the first few files while testing:

```bash
python scripts/anythingllm_ingest.py -n -l 10
```

Write the exact ingestion file list to disk for review:

```bash
python scripts/anythingllm_ingest.py -n -file-list anythingllm_file_list.txt
```

Ingest only files newer than a marker file such as `NOW`:

```bash
python scripts/anythingllm_ingest.py -n -since-marker NOW -file-list anythingllm_newer_than_now.txt
python scripts/anythingllm_ingest.py -since-marker NOW
```

List documents that have already been uploaded to AnythingLLM:

```bash
python scripts/anythingllm_ingest.py -list-documents
```

List available workspace slugs:

```bash
python scripts/anythingllm_ingest.py -list-workspaces
```

The default manifest includes Markdown, text, YAML, and selected CSV files. It excludes generated `viewable/` and `site/` output, most generated HTML, PDFs, images, spreadsheets, archives, and large files. This keeps AnythingLLM from ingesting duplicate or noisy content before the curated notes exist.

If you want selected HTML reports included, add them under `allow_html` in the manifest.

## 17. Querying With Command-Line Tools

Search document IDs:

```bash
rg "doc_id:" frontend/docs
```

Search relationships:

```bash
rg "clarity_vs_kpmg_tvf" frontend/docs/doc_relationships.csv
```

Validate YAML:

```bash
yq '.' frontend/docs/doc_registry.yaml >/dev/null
yq '.' frontend/docs/doc_claims.yaml >/dev/null
```

Validate CSV shape:

```bash
python - <<'PY'
import csv
from pathlib import Path

path = Path("frontend/docs/doc_relationships.csv")
with path.open(newline="") as f:
    rows = list(csv.DictReader(f))

required = {"source_doc", "target_doc", "relationship_type", "reason"}
missing = required - set(rows[0].keys()) if rows else required
if missing:
    raise SystemExit(f"Missing columns: {sorted(missing)}")

print(f"OK: {len(rows)} relationships")
PY
```

## 18. Optional Custom RAG Layer

AnythingLLM is the recommended first chat layer. Add a custom RAG layer only after the registry is stable and only if AnythingLLM does not provide enough control over chunking, metadata filters, model routing, or retrieval behavior.

Recommended custom architecture:

- Chunk Markdown by headings.
- Store chunk text plus metadata.
- Use `doc_registry.yaml` as the metadata source.
- Retrieve by metadata first, then semantic similarity.
- Keep AI notes as high-priority retrieval documents.

Suggested chunk metadata:

```yaml
doc_id:
title:
path:
type:
status:
domain:
layer:
project:
phase_id:
tags:
heading_path:
```

Recommended local vector stores:

```text
ChromaDB
LanceDB
SQLite with sqlite-vss
```

Start simple. Obsidian plus AnythingLLM plus a good registry will usually produce better behavior than a large unstructured vector database.

## 19. RAG Retrieval Rules

AnythingLLM workspace instructions and any future custom RAG layer should follow these rules:

1. Never retrieve from superseded documents unless specifically requested.
2. Prefer `active` and `reviewed` documents.
3. Prefer documents with matching `layer`.
4. Preserve the distinction between supply chain, system lifecycle, value chain, and financial abstraction.
5. Retrieve AI notes before long source documents when the question is conceptual.
6. Retrieve source documents before AI notes when the question asks for evidence.
7. Include document path and `doc_id` in every retrieved result.

## 20. Minimum Viable Setup

The minimum useful system is:

```text
frontend/docs/doc_registry.yaml
frontend/docs/doc_relationships.csv
frontend/docs/doc_claims.yaml
frontend/docs/ai_notes/document_notes/
frontend/docs/ai_notes/concept_notes/
```

Use these files with Obsidian and AnythingLLM before adding a custom vector database.

## 21. Recommended First Documents To Register

Start with the documents that define the project vocabulary:

- `CLARITY_TRUE_VALUE_VS_KPMG_TRUE_VALUE.md`
- `THOLONIC_FRAMEWORK_SUPPLY_AND_VALUE_CHAIN_APPLICATION.md`
- `THOLONIC_INTEGRATION.md`
- `SUPPLY_CHAIN_RULES.md`
- `VALUE_CHAIN_RULES.md`
- `NDC-global-support.md`
- `SUSTAINABILITY_LINKED_LOAN_CREDIT_RATING_FRAMEWORK.md`

Then add project-specific documents for gold, shea, AUBEB, water, and grid systems.

## 22. Summary

The recommended system is not just RAG and not just Obsidian. It is a structured knowledge and chat layer:

- Obsidian for human navigation.
- MkDocs for publishing.
- AnythingLLM for chat with the curated document corpus.
- YAML frontmatter for per-document metadata.
- `doc_registry.yaml` for AI-readable document inventory.
- `doc_relationships.csv` for explicit concept mapping.
- `doc_claims.yaml` for reusable analytical claims.
- AI notes for durable summaries and handling instructions.
- Custom RAG later, only if AnythingLLM is not enough.

This gives the AI a map before asking it to answer questions from the documents.
