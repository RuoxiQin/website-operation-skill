# website-operation-skill

An LLM **skill** that teaches an agent to operate a website through a real browser — navigate, fill forms, click, extract rendered content, capture screenshots — plus a side-by-side comparison harness that demonstrates the difference the skill makes.

## What's here

- [`SKILL.md`](SKILL.md) — the skill itself. A short Playwright playbook the agent follows when handed a browser-automation task.
- [`examples/`](examples/) — two pi-agent setups (`pi-with-skill`, `pi-without-skill`) configured to run the same prompt against the same model with only the skill toggled. See [examples/README.md](examples/README.md) for how to run the comparison.

## Skill format

`SKILL.md` follows the [agentskills.io](https://agentskills.io) open standard, which means the same file works in:

- **[pi](https://pi.dev/docs/latest)** — drop into `<cwd>/.pi/skills/website-operation/SKILL.md` (pi can be installed locally per-project; no global install required)
- **[Claude Code](https://docs.claude.com/en/docs/claude-code/skills)** — drop into `~/.claude/skills/website-operation/SKILL.md` or `.claude/skills/website-operation/SKILL.md`
- Any other tool that implements the standard

## Quick start

```bash
git clone <this-repo> && cd website-operation-skill
cd examples && cat README.md   # follow the harness instructions
```
