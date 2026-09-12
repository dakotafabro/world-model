# world-model

Structured knowledge corpus for any codebase. Five-layer architecture with MCP
tools for querying, health monitoring, and bootstrapping.

## Why

Agents need system context to be useful beyond local code. A world model
captures how a system works (state), why things break (causal), what the team is
trying to achieve (intent), what could go wrong at scale (prediction), and how
to operate it (ops). The world model makes this queryable - not readable, queryable.

## Quick Start

```bash
bpm install world-model
```

Then bootstrap your world model:

1. Set `WM_REPO_DIR` to where your world model will live
2. Use the `wm_scaffold` tool to create the directory structure
3. Fill in state files for your major domains (week 1)
4. Add causal files for failure modes (week 2)
5. Add intent files for architectural decisions (week 3)
6. Add routing keywords and test with eval scenarios (week 4)

## MCP Tools

| Tool | What it does |
|---|---|
| `wm_query` | Route a question to the right file(s) via keyword matching |
| `wm_read` | Read a specific section (supports line ranges) |
| `wm_search` | Full-text search across all layers |
| `wm_health` | Report staleness, gaps, and drift |
| `wm_scaffold` | Bootstrap a new world model |
| `wm_index` | Regenerate INDEX.md files |

## Files

- `SKILL.md` - Full convention and usage instructions
- `mcp/` - MCP server implementation
- `templates/` - Starter files for new world models
