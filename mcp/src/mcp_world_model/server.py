from fastmcp import FastMCP

INSTRUCTIONS = """
World Model MCP server. Provides tools for querying, scaffolding, and
maintaining five-layer world models (state, causal, intent, prediction, ops).

Use wm_query to route questions to the right file. Use wm_read to read
specific sections. Use wm_health to check freshness and coverage.
Use wm_scaffold to bootstrap a new world model.
"""

mcp = FastMCP("world-model", instructions=INSTRUCTIONS)


@mcp.tool()
def wm_query(question: str, wm_dir: str = "") -> str:
    """Route a question to the right world model file(s) using keyword matching
    against frontmatter routing tables. Returns file paths and relevant sections."""
    from mcp_world_model.tools.query import route_question
    return route_question(question, wm_dir)


@mcp.tool()
def wm_read(file_path: str, section: str = "", start_line: int = 0, end_line: int = 0) -> str:
    """Read a specific section or line range from a world model file."""
    from mcp_world_model.tools.query import read_section
    return read_section(file_path, section, start_line, end_line)


@mcp.tool()
def wm_search(query: str, layer: str = "", wm_dir: str = "") -> str:
    """Full-text search across all world model layers. Optionally filter by layer."""
    from mcp_world_model.tools.query import search_layers
    return search_layers(query, layer, wm_dir)


@mcp.tool()
def wm_health(wm_dir: str = "") -> str:
    """Report world model health: staleness (files past last_verified TTL),
    coverage gaps (domains without state files), and structural issues."""
    from mcp_world_model.tools.health import check_health
    return check_health(wm_dir)


@mcp.tool()
def wm_scaffold(project_name: str, target_dir: str = "") -> str:
    """Bootstrap a new world model from templates. Creates directory structure,
    MANIFEST.yaml, AGENTS.md routing table, and starter layer files."""
    from mcp_world_model.tools.scaffold import create_world_model
    return create_world_model(project_name, target_dir)


@mcp.tool()
def wm_index(wm_dir: str = "") -> str:
    """Regenerate INDEX.md files for each layer from file frontmatter."""
    from mcp_world_model.tools.health import regenerate_indexes
    return regenerate_indexes(wm_dir)


def main() -> None:
    mcp.run()
