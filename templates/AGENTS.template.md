# Agent Instructions

## Overview

This directory contains the world model for [your project]. Use this to answer
questions about the system's architecture, services, infrastructure, failure
modes, and operational procedures.

## How to Use This Knowledge

1. Check **state/** for facts about what exists (services, databases, topology)
2. Check **causal/** for understanding why things break and how failures propagate
3. Check **intent/** for understanding goals, migrations, and architectural invariants
4. Check **prediction/** for blast radius analysis and incident patterns
5. Check **ops/** for operational procedures and how-to workflows

## Routing Table

Map questions to files. Add entries as your world model grows.

| Question keywords | Look here |
|---|---|
| "auth", "login", "session" | `layers/state/auth.md` |
| "deploy", "release", "rollback" | `ops/deployment.md` |

## Key Principles

- **MAP, not mirror.** Point to live sources. Don't duplicate data that lives
  in dashboards, code, or issue trackers.
- **Default to execute, not instruct.** When the user asks about current state,
  run the query and return values. Don't explain how they could look it up.
- **Read indexes first.** Each layer has an INDEX.md. Scan it before opening
  individual files.
