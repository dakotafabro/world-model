"""Query tools for world model: route, read, search."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

import yaml


def _resolve_wm_dir(wm_dir: str = "") -> Path:
    if wm_dir:
        return Path(wm_dir).expanduser()
    env_dir = os.environ.get("WM_REPO_DIR")
    if env_dir:
        return Path(env_dir).expanduser()
    active_env = Path("~/.config/world-model/active.env").expanduser()
    if active_env.exists():
        for line in active_env.read_text().splitlines():
            if line.startswith("WM_REPO_DIR="):
                return Path(line.split("=", 1)[1].strip()).expanduser()
    return Path.cwd()


def _load_frontmatter(file_path: Path) -> dict:
    text = file_path.read_text()
    if not text.startswith("---"):
        return {}
    end = text.index("---", 3)
    return yaml.safe_load(text[3:end]) or {}


def route_question(question: str, wm_dir: str = "") -> str:
    base = _resolve_wm_dir(wm_dir)
    layers_dir = base / "layers"
    if not layers_dir.exists():
        return json.dumps({"error": f"No layers/ directory found at {base}"})

    question_lower = question.lower()
    matches = []

    for md_file in sorted(layers_dir.rglob("*.md")):
        if md_file.name == "INDEX.md":
            continue
        try:
            fm = _load_frontmatter(md_file)
        except Exception:
            continue

        routing = fm.get("routing", [])
        for route in routing:
            keywords = [k.lower() for k in route.get("keywords", [])]
            for kw in keywords:
                if kw in question_lower:
                    matches.append({
                        "file": str(md_file.relative_to(base)),
                        "section": route.get("section", ""),
                        "lines": route.get("lines", []),
                        "matched_keyword": kw,
                        "domain": fm.get("domain", ""),
                        "summary": fm.get("summary", ""),
                    })
                    break

    return json.dumps(matches[:10], indent=2)


def read_section(file_path: str, section: str = "", start_line: int = 0, end_line: int = 0) -> str:
    path = Path(file_path).expanduser()
    if not path.exists():
        return json.dumps({"error": f"File not found: {file_path}"})

    lines = path.read_text().splitlines()

    if start_line and end_line:
        return "\n".join(lines[max(0, start_line - 1):end_line])

    if section:
        in_section = False
        result = []
        section_lower = section.lower()
        for line in lines:
            if line.startswith("#") and section_lower in line.lower():
                in_section = True
                result.append(line)
            elif in_section and line.startswith("#") and len(line) - len(line.lstrip("#")) <= 2:
                break
            elif in_section:
                result.append(line)
        if result:
            return "\n".join(result)
        return json.dumps({"error": f"Section '{section}' not found in {file_path}"})

    return "\n".join(lines)


def search_layers(query: str, layer: str = "", wm_dir: str = "") -> str:
    base = _resolve_wm_dir(wm_dir)
    layers_dir = base / "layers"
    if not layers_dir.exists():
        return json.dumps({"error": f"No layers/ directory found at {base}"})

    search_dir = layers_dir / layer if layer else layers_dir
    if not search_dir.exists():
        return json.dumps({"error": f"Layer directory not found: {search_dir}"})

    query_lower = query.lower()
    results = []

    for md_file in sorted(search_dir.rglob("*.md")):
        if md_file.name == "INDEX.md":
            continue
        try:
            text = md_file.read_text()
        except Exception:
            continue

        for i, line in enumerate(text.splitlines(), 1):
            if query_lower in line.lower():
                results.append({
                    "file": str(md_file.relative_to(base)),
                    "line": i,
                    "text": line.strip()[:120],
                })

    return json.dumps(results[:20], indent=2)
