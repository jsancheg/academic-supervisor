Academic Supervisor Agent — Project Specification
1. Overview
This project is a fully local, Streamlit-based academic writing assistant that behaves like a strict PhD supervisor. It reviews academic documents (text/PDF) and provides structured feedback without automatically rewriting full documents.

2. Scope
Included
*Grammar correction (suggestions only)
*Clarity and coherence analysis
*Academic argument structure review
&Citation format validation (APA / Harvard consistency)
*Figure/table numbering validation
*Paragraph-level logical consistency with global document context

Excluded (MVP)
*Full automatic rewriting of documents
*External API-based citation verification (optional future RAG extension)

3. Input / Output
Input
*Plain text
*PDF documents
Output
*Corrected suggestions (snippets only)
*Strict structured feedback report

4. System Behaviour
*Strict academic supervisor mode
*No full document rewriting
*Evidence-based critique required
*Every issue must include:
	*Problem description
	*Location (paragraph/sentence)
	*Why it is an issue
*Suggested fix


5. Architecture
Pipeline
*Document ingestion (text/PDF)
*Parsing into paragraphs and sections
*Global context builder
*Rule-based validation engine
*Multi-agent LLM review system
*Supervisor merge node
*Streamlit UI output


6. Core Components
6.1 Parser
*Paragraph extraction
*Section detection
*Figure/table detection (PDF only)


6.2 Global Context Memory (Session-based)

Stored in st.session_state:

*Thesis / main argument
*Section structure map
*Terminology consistency map
*Citation index
*Figure/table registry

6.3 Rule Engine (Deterministic Layer)
*Citation format validation
*Figure/table numbering order
*Missing labels detection
*Structural consistency checks

6.4 LLM Agents
*Grammar Agent (fast model) → sentence correctness
*Clarity Agent (stable model) → rewriting suggestions
*Coherence Agent (Qwen) → global argument consistency

6.5 Supervisor Agent
*Merges all outputs
*Removes duplicates
*Resolves conflicts
*Enforces strict academic tone

7. Output Format
Corrected Snippets
*Only partial rewrites allowed
*Never full document rewrite


Feedback Report (STRICT STYLE)

Sections:

]	*Grammar
	*Clarity & Flow
	*Coherence (global-aware)
	*Citations
	*Structure

Each issue includes:

	*What is wrong
	*Why it is wrong (academic reasoning)
	*Suggested fix

8. Session Memory (Streamlit)

Stored in:

*document
*parsed_paragraphs
*global_context
*issues
*citation_index
*figure_table_registry


9. Design Principles
*Fully local execution (no external APIs required)
*Strict supervisor personality
*Global document reasoning enabled
*Rule engine + LLM hybrid system
*Transparent, explainable feedback


10. Future Extensions
*Local RAG system for citation verification (PDF paper checking)
*Incremental document re-analysis (diff-based updates)
*Streamlit track-changes style highlighting
*Export to Word with comments
*Fine-grained argument graph analysis

11. Non-Functional Requirements
*Optimised for RTX 2070 (mixed model usage)
*Modular LangGraph architecture
*Low latency per paragraph review
*Deterministic + probabilistic hybrid system

End of Specification
