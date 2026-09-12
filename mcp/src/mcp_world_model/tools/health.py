"""Health and index tools for world model."""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import yaml


def _resolve_wm_dir(wm_dir: str = "") -> Path:
    if wm_dir:
        return Path(wm_dir).expanduser()
    env_dir = os.environ.get("WM_REPO_DIR")
    if env_dir:
        return Path(env_dir).expanduser()
    return Path.cwd()


def _load_frontmatter(file_path: Path) -> dict:
    text = file_path.read_text()
    if not text.startswith("---"):
        return {}
    end = text.index("---", 3)
    return yaml.safe_load(text[3:end]) or {}


def check_health(wm_dir: str = "") -> str:
    base = _resolve_wm_dir(wm_dir)
    layers_dir = base / "layers"
    if not layers_dir.exists():
        return json.dumps({"error": f"No layers/ directory found at {base}"})

    stale = []
    no_date = []
    total = 0
    layer_counts = {}
    today = datetime.now()
    stale_threshold = timedelta(days=30)

    for md_file in sorted(layers_dir.rglob("*.md")):
        if md_file.name == "INDEX.md" or md_file.name.startswith("_"):
            continue
        total += 1

        layer_name = md_file.parent.name
        layer_counts[layer_name] = layer_counts.get(layer_name, 0) + 1

        try:
            fm = _load_frontmatter(md_file)
        except Exception:
            continue

        last_verified = fm.get("last_verified")
        if not last_verified:
            no_date.append(str(md_file.relative_to(base)))
            continue

        try:
            verified_date = datetime.strptime(str(last_verified), "%Y-%m-%d")
            if today - verified_date > stale_threshold:
                stale.append({
                    "file": str(md_file.relative_to(base)),
                    "last_verified": str(last_verified),
                    "days_stale": (today - verified_date).days,
                })
        except ValueError:
            no_date.append(str(md_file.relative_to(base)))

    report = {
        "total_files": total,
        "layer_counts": layer_counts,
        "stale_files": len(stale),
        "stale": stale[:20],
        "missing_date": no_date[:20],
    }

    return json.dumps(report, indent=2)


def regenerate_indexes(wm_dir: str = "") -> str:
    base = _resolve_wm_dir(wm_dir)
    layers_dir = base / "layers"
    if not layers_dir.exists():
        return json.dumps({"error": f"No layers/ directory found at {base}"})

    generated = []

    for layer_dir in sorted(layers_dir.iterdir()):
        if not layer_dir.is_dir():
            continue

        entries = []
        for md_file in sorted(layer_dir.glob("*.md")):
            if md_file.name == "INDEX.md" or md_file.name.startswith("_"):
                continue
            try:
                fm = _load_frontmatter(md_file)
            except Exception:
                continue

            line_count = len(md_file.read_text().splitlines())
            entries.append({
                "file": md_file.name,
                "domain": fm.get("domain", ""),
                "summary": fm.get("summary", ""),
                "lines": line_count,
                "last_verified": str(fm.get("last_verified", "")),
            })

        index_lines = [
            f"# `{layer_dir.name}/` - Index\n",
            f"_Auto-generated from frontmatter. Do not edit by hand._\n",
            f"\n**{len(entries)} files** in this layer.\n",
            "\n| File | Domain | Summary | Lines | last_verified |",
            "|---|---|---|---:|---|",
        ]
        for e in entries:
            index_lines.append(
                f"| [`{e['file']}`]({e['file']}) | {e['domain']} | {e['summary']} | {e['lines']} | {e['last_verified']} |"
            )

        index_path = layer_dir / "INDEX.md"
        index_path.write_text("\n".join(index_lines) + "\n")
        generated.append(str(index_path.relative_to(base)))

    return json.dumps({"generated": generated}, indent=2)
