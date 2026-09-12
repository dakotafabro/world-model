---
name: world-model
description: >
  Structured knowledge corpus for any codebase. Five-layer architecture with
  MCP tools for querying, health monitoring, and bootstrapping. The map that
  makes your code navigable by agents and engineers.
author: dakotafabro
version: "0.1.0"
tags:
  - world-model
  - knowledge
  - architecture
  - system-context
  - mcp
---

# World Model

A structured knowledge corpus that captures how a system works, why things
break, what the team is trying to achieve, and what to do when things go wrong.

## What a World Model Is

A world model is not documentation. Documentation is written to be read. A world
model is written to be queried. The difference:

- Documentation organizes by topic. A world model organizes by question type.
- Documentation assumes a human reader. A world model assumes an agent reader.
- Documentation goes stale silently. A world model tracks its own freshness.
- Documentation lives in one place. A world model has layers that answer
  different questions about the same domain.

## The Five Layers

| Layer | Question it answers | What lives here |
|---|---|---|
| **State** | What is true right now? | Services, topology, entities, APIs, databases, configurations |
| **Causal** | What drives what? | Failure modes, error propagation, decision trees |
| **Intent** | What are we trying to do? | Strategy, migrations, ADRs, architectural invariants |
| **Prediction** | What will happen next? | Blast radius, leading indicators, incident patterns |
| **Ops** | How do we operate it? | Runbooks, commands, queries, tools |

Not every world model needs all five layers on day one. Start with State.
Add Causal when you have incident data. Add Intent when you have ADRs.
Prediction and Ops come as the system matures.

## MCP Tools

The world-model package provides MCP tools for interacting with any world model
that follows the five-layer convention:

| Tool | What it does |
|---|---|
| `wm_query` | Route a question to the right world model file(s) using keyword matching against frontmatter |
| `wm_read` | Read a specific section of a world model file (supports line ranges from frontmatter routing) |
| `wm_search` | Full-text search across all layers |
| `wm_health` | Report staleness, coverage gaps, and drift signals |
| `wm_scaffold` | Bootstrap a new world model from templates |
| `wm_index` | Regenerate INDEX.md files from frontmatter |

## Bootstrapping a New World Model

Run `wm_scaffold` or manually create the structure:

```
my-world-model/
├── MANIFEST.yaml           # Domain name, description, platform
├── AGENTS.md               # Routing table (keywords -> files)
└── layers/
    ├── state/
    │   ├── INDEX.md         # Auto-generated from frontmatter
    │   └── {domain}.md      # One file per domain area
    ├── causal/
    │   ├── INDEX.md
    │   └── {domain}-failures.md
    └── intent/
        ├── INDEX.md
        └── decisions.md
```

See the templates/ directory for starter files with the right frontmatter
structure and inline instructions.

## The 4-Week Bootstrap

**Week 1: State layer.** For each major module or service boundary, write a
state file: what is this, what does it connect to, what are the key entities?

**Week 2: Causal layer.** For each state file, write the failure file: what
breaks, how does it break, what are the symptoms?

**Week 3: Intent layer.** One file: what are we trying to achieve, what
migrations are in flight, what architectural decisions constrain the codebase?

**Week 4: Routing and eval.** Add frontmatter keywords to every file. Write 10
eval scenarios (real questions engineers ask). Test whether the world model
improves answers.

## Key Principles

**Queryable, not readable.** Routing keywords in frontmatter + line ranges mean
an agent finds the answer in seconds without reading everything.

**MAP, not mirror.** The world model tells you where to look. Live data is the
truth for current state. Don't duplicate information that already lives in an
authoritative source - point to it.

**Layers, not categories.** The same domain appears in multiple layers. One
question, multiple angles, no need to know which angle to ask from.

**Freshness-tracked.** Every file has a `last_verified` date in frontmatter.
The `wm_health` tool reports what's stale.

## Configuration

Set the world model location:

```bash
export WM_REPO_DIR=~/path/to/your/world-model
```

Or create `~/.config/world-model/active.env`:

```
WM_REPO_DIR=~/path/to/your/world-model
WM_REPO_SLUG=your-org/your-world-model
```

## Peer Packages

- **translator** - When both are installed, the translator grounds its code
  narrations in world model context automatically.
- **world-model-learner** - Background daemon that trains the world model from
  real agent threads.
