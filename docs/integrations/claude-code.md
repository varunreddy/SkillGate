# Claude Code Integration

SkillMesh can be used in Claude Code via MCP or by calling the router script directly.

## Option A: MCP server (recommended)

Add to your Claude Code MCP settings (`.claude/settings.json` or via `claude mcp add`):

```json
{
  "mcpServers": {
    "skillmesh": {
      "command": "uvx",
      "args": ["--from", "skillmesh[mcp]", "skillmesh-mcp"]
    }
  }
}
```

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/). No env vars or file paths needed.

Once configured, Claude Code can call `route_with_skillmesh()` and `retrieve_skillmesh_cards()` automatically.
It can also manage roles directly over MCP:
- `list_skillmesh_roles()`
- `list_installed_skillmesh_roles()`
- `install_skillmesh_role(role="Data-Analyst")`

## Option B: Skill bundle + CLI

### 1) Install the skill bundle in Codex-style layout

```bash
$skill-installer install https://github.com/varunreddy/SkillMesh/tree/main/skills/skillmesh
```

Restart Codex after install.

### 2) Route for Claude output format

```bash
~/.codex/skills/skillmesh/scripts/route.sh \
  --provider claude \
  --backend auto \
  --registry /absolute/path/to/tools.json \
  --query "build an opencv contour pipeline" \
  --top-k 5
```

### 3) Role commands (optional)

Interactive role install (recommended):

```bash
skillmesh roles
```

List roles:

```bash
skillmesh roles list
```

Install a specific role:

```bash
skillmesh DevOps-Engineer install
```

Defaults:
- Catalog defaults to `SKILLMESH_CATALOG`, then `SKILLMESH_REGISTRY`, then bundled registry.
- Target role registry defaults to `SKILLMESH_ROLE_REGISTRY`, then `SKILLMESH_REGISTRY`, then `~/.codex/skills/skillmesh/installed.registry.yaml`.
- Existing cards are deduplicated; only missing dependency cards are added.

If you prefer skill-bundle wrappers, use:
`~/.codex/skills/skillmesh/scripts/roles.sh` (interactive)

### 4) Use in Claude Code workflow

- Run the command above.
- Paste the returned XML block into Claude Code.
- Ask Claude to proceed using only those top-5 cards/tools.

## Optional helper alias

```bash
alias skillmesh-claude='~/.codex/skills/skillmesh/scripts/route.sh --provider claude --top-k 5'
```

Then run:

```bash
skillmesh-claude --registry /path/to/tools.json --query "your task"
```
