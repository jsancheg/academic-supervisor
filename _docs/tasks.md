# Backlog — Academic Writing Supervisor

Stack decisions locked in: Ollama (local LLM runtime) + LangGraph (orchestration) +
LLM-based Grammar Agent (no LanguageTool) + PyMuPDF (PDF parsing) + Streamlit (UI).

Tasks are grouped by pipeline stage (see `_docs/plan.md` architecture, section 5).
Within a group, roughly top-to-bottom order.

## 0. Project setup
- [ ] Initialize Python project structure (src layout, `pyproject.toml`/`requirements.txt`)
- [ ] Install and verify Ollama on Ubuntu; pull baseline models (e.g. Qwen2.5-7B-Instruct Q4 for Coherence, a smaller quantized model for Clarity/Grammar)
- [ ] Verify GPU offload works within RTX 2070 8GB VRAM budget (single model resident at a time)
- [ ] Set up Streamlit app skeleton (single page, file upload widget)
- [ ] Set up LangGraph skeleton with placeholder nodes matching the pipeline diagram

## 1. Document ingestion & parsing
- [ ] Plain text ingestion (read + normalize encoding/whitespace)
- [ ] PDF ingestion via PyMuPDF
- [ ] Paragraph extraction (text + PDF)
- [ ] Section/heading detection
- [ ] Figure/table detection (PDF only) — caption + numbering extraction

## 2. Global context memory (Streamlit session state)
- [ ] Define session_state schema: `document`, `parsed_paragraphs`, `global_context`, `issues`, `citation_index`, `figure_table_registry`
- [ ] Thesis/main-argument extraction into `global_context`
- [ ] Section structure map builder
- [ ] Terminology consistency map builder
- [ ] Citation index builder
- [ ] Figure/table registry builder

## 3. Rule engine (deterministic layer)
- [ ] Citation format validator (APA / Harvard consistency)
- [ ] Figure/table numbering order checker
- [ ] Missing label detector (figures/tables referenced but not labeled, or vice versa)
- [ ] Structural consistency checks (e.g. missing sections, out-of-order headings)

## 4. LLM agents
- [ ] Grammar Agent (fast local model) — sentence-level correctness, snippet-only suggestions
- [ ] Clarity Agent (stable local model) — clarity/coherence rewriting suggestions at paragraph level
- [ ] Coherence Agent (Qwen) — global argument consistency using `global_context`
- [ ] Shared prompt scaffolding enforcing: problem description, location, why it's an issue, suggested fix
- [ ] Guardrail: agents must return snippets only, never full paragraph/document rewrites

## 5. Supervisor merge node
- [ ] Merge outputs from Grammar/Clarity/Coherence agents + rule engine
- [ ] De-duplicate overlapping issues (same location/problem from multiple sources)
- [ ] Conflict resolution logic when agents disagree
- [ ] Enforce strict academic tone in final report text

## 6. Output / reporting
- [ ] Corrected-snippet renderer (partial rewrites only)
- [ ] Structured feedback report renderer, sectioned: Grammar, Clarity & Flow, Coherence, Citations, Structure
- [ ] Per-issue fields enforced: what's wrong, why (academic reasoning), suggested fix
- [ ] Streamlit output view wiring (upload → run pipeline → render report)

## 7. LangGraph wiring
- [ ] Define graph state type covering all global-context fields
- [ ] Wire nodes: ingestion → parsing → global context builder → rule engine → LLM agents → supervisor merge → UI output
- [ ] Sequencing logic to respect single-model-at-a-time VRAM constraint (load/unload or reuse Ollama's model swapping)

## 8. Testing & validation
- [ ] Sample documents (text + PDF) covering: clean doc, bad citations, mislabeled figures, incoherent argument
- [ ] Manual QA pass: confirm no full-document rewrites ever produced
- [ ] Manual QA pass: confirm every issue includes all four required fields
- [ ] Basic latency check per paragraph on RTX 2070

## Future extensions (post-MVP, not scheduled)
- [ ] Local RAG system for citation verification against source PDFs
- [ ] Incremental/diff-based re-analysis on document edits
- [ ] Streamlit track-changes style highlighting
- [ ] Export report to Word with inline comments
- [ ] Fine-grained argument graph analysis
