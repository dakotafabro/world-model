"""Scaffold tool for bootstrapping new world models."""
from __future__ import annotations

import json
import os
from pathlib import Path


def create_world_model(project_name: str, target_dir: str = "") -> str:
    base = Path(target_dir).expanduser() if target_dir else Path.cwd() / f"{project_name}-world-model"

    if base.exists() and any(base.iterdir()):
        return json.dumps({"error": f"Target directory is not empty: {base}"})

    base.mkdir(parents=True, exist_ok=True)

    manifest = f"""domain: {project_name}
domain_slug: {project_name}
description: >
  World model for {project_name}. Fill in a description of what this system
  does and who it serves.

coverage:
  domains: []
"""
    (base / "MANIFEST.yaml").write_text(manifest)

    agents = f"""# Agent Instructions - {project_name} World Model

## Overview

This directory contains the world model for {project_name}. Use this to answer
questions about the system's architecture, services, failure modes, and
operational procedures.

## How to Use

1. Check **state/** for facts about what exists
2. Check **causal/** for understanding why things break
3. Check **intent/** for understanding goals and architectural decisions

## Routing Table

| Question keywords | Look here |
|---|---|
| | `layers/state/` |

Add routing entries as your world model grows. Each state file should have
`routing.keywords` in its YAML frontmatter for automated routing.
"""
    (base / "AGENTS.md").write_text(agents)

    for layer in ["state", "causal", "intent", "prediction", "ops"]:
        layer_dir = base / "layers" / layer
        layer_dir.mkdir(parents=True, exist_ok=True)
        (layer_dir / "INDEX.md").write_text(
            f"# `{layer}/` - Index\n\n_Auto-generated. Run `wm_index` to refresh._\n"
        )

    created = []
    for p in sorted(base.rglob("*")):
        if p.is_file():
            created.append(str(p.relative_to(base)))

    return json.dumps({
        "created_at": str(base),
        "files": created,
        "next_steps": [
            f"Set WM_REPO_DIR={base} in your environment or ~/.config/world-model/active.env",
            "Create your first state file: layers/state/core.md (use the template from the world-model package)",
            "Add routing keywords to the frontmatter",
            "Run wm_index to generate INDEX.md files",
        ]
    }, indent=2)
