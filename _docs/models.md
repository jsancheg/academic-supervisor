# Local LLM Models

Runtime: [Ollama](https://ollama.com), local HTTP API at `http://localhost:11434`.

| Agent      | Model                        | Size   | Notes                                             |
|------------|-------------------------------|--------|----------------------------------------------------|
| Coherence  | `qwen2.5:7b-instruct-q4_K_M`  | 4.7 GB | Matches spec (section 6.4); global argument review |
| Clarity    | `phi3:latest`                 | 2.2 GB | Mid-size, "stable" general-purpose model            |
| Grammar    | `llama3.2:3b`                 | 2.0 GB | Smallest/fastest, sentence-level grammar checks     |

All three were already pulled locally (`ollama list`) and smoke-tested via `curl` against
the Ollama HTTP API — each returns a response for a simple prompt.

GPU-offload/VRAM verification against the RTX 2070's 8GB budget (issue #3) must be run on
a machine with the GPU attached — this development sandbox has no NVIDIA device
(`/dev/nvidia*` absent, no `nvidia-smi`), so inference above ran on CPU.
