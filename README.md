# website-operation-skill

A skill that gives your agents a pre-built map of indexed websites so they can navigate and operate those sites faster and more accurately — no blind crawling, no URL guessing.

## Quick Install

```bash
npx skills add RuoxiQin/website-operation-skill
```

Or to install for specific agents:

**Claude Code**:

```bash
mkdir -p ~/.claude/skills && cd ~/.claude/skills && git clone https://github.com/RuoxiQin/website-operation-skill website-operation
```

**pi** (per-project):

```bash
mkdir -p .pi/skills && cd .pi/skills && git clone https://github.com/RuoxiQin/website-operation-skill website-operation
```

## Skill format

`SKILL.md` follows the [agentskills.io](https://agentskills.io) open standard. The frontmatter declares the skill's name, description (used by the agent to decide when to invoke it), and which tools are allowed:

```yaml
---
name: website-operation
description: Look up an indexed map of a website's structure before browsing or searching it. ...
allowed-tools: Bash, Read
---
```

The body is a plain Markdown playbook the agent follows:

1. **Identify** the apex domain of the target site (e.g. `anthropic.com`).
2. **Run** `bash scripts/check_domain.sh <domain>` — prints the path to the reference doc if indexed, or `not indexed` if not.
3. **Read** the reference doc before doing anything with the site. It maps sub-domains, sections, and URL patterns so the agent targets the right place immediately.

### Adding a new website

Drop a Markdown file into [`references/`](references/) named `<domain>.md` (e.g. `references/openai.com.md`). The check script discovers it automatically — no other changes needed. The reference doc should describe the site's structure: which sub-domains exist, what each section contains, and any URL patterns worth knowing.

## Comparison harness

The [`examples/`](examples/) directory contains a side-by-side test harness — two identical pi-agent setups where the only variable is whether the skill is loaded. It exists for **demonstration and evaluation purposes only**; it is not part of the skill itself.

See [examples/README.md](examples/README.md) for setup and run instructions.
