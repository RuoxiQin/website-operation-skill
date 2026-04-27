# anthropic.com

Anthropic's website + adjacent official properties. Picking the wrong section is the most common reason agents fail to find Anthropic content that does exist. **Read the router first, then jump to the matching entry.**

## Router (intent → destination)

- "what did Anthropic discover / research / find" → `anthropic.com/research`
- "how do they build agents / evals / Claude Code / MCP / harnesses" → `anthropic.com/engineering`
- "new model / product launch / partnership / press announcement" → `anthropic.com/news`
- "Claude product best practices, enterprise / agent patterns" → `claude.com/blog`
- "what actually changed in the API / SDK / Console" → `platform.claude.com/docs/en/release-notes/overview`
- "mechanistic interp, sparse autoencoders, features, circuits, model internals" → `transformer-circuits.pub`
- "alignment auditing, sandbagging, model organisms, early safety notes" → `alignment.anthropic.com`
- "AI labor impact, jobs, Anthropic Economic Index" → `anthropic.com/economic-futures`
- "SDK source, cookbooks, official plugins / skills, code examples" → `github.com/anthropics`

## Properties

### anthropic.com/research
- Content: Research publication hub. Subareas: Alignment, Interpretability, Societal Impacts, Frontier Red Team, Economic Research, Policy.
- Use for: new findings, safety papers, jailbreak/red-team work, evaluation methods, AI impact studies.
- Skip for: applied agent-building (→ engineering), product news (→ news), deep mechanistic interp (→ transformer-circuits.pub).

### anthropic.com/engineering
- Content: Engineering systems blog — building reliable AI systems. Recent topics: managed agents, Claude Code auto mode, long-running harnesses, agentic-coding eval noise, tool use, MCP, context engineering, postmortems.
- Use for: how to build/evaluate agents, design tools for agents, harness patterns, infra tradeoffs, failure reports.
- Skip for: product announcements (→ news), scientific findings (→ research).
- Note: Usually the most practically useful section for LLM/agent developers.

### anthropic.com/news
- Content: Newsroom. Model releases, product launches, partnerships, policy/election/safety announcements.
- Use for: official announcements only.
- Skip for: technical depth (→ engineering or release notes).

### claude.com/blog
- Content: Claude product + best-practices blog. Categories: Agents, Claude Code, Enterprise AI, Product announcements, Coding, Productivity, Work.
- Use for: productized agent patterns, Claude Code workflows, enterprise rollouts, MCP from a product angle. Sits between News and Engineering.
- Skip for: API changelog (→ release notes), academic findings (→ research).

### platform.claude.com/docs/en/release-notes/overview
- Content: Claude Platform release notes. API, SDK, Console, model deprecations, beta headers, managed agents, rate limits.
- Use for: authoritative "what changed in the API" lookups.
- Skip for: conceptual explanations or how-to (→ engineering / claude.com/blog).

### transformer-circuits.pub
- Content: Dedicated interpretability research site. Mechanistic interp papers, research notes, interactive articles.
- Use for: sparse autoencoders, features, circuits, activation-level explanations, model internals.
- Skip for: alignment policy / red-team work (→ research or alignment.anthropic.com).

### alignment.anthropic.com
- Content: Alignment Science Blog. Research notes and early findings that don't warrant a full publication.
- Use for: alignment auditing, sandbagging, weak-to-strong generalization, automated alignment researchers, hidden behaviors, model organisms, safety evaluations.
- Skip for: production safety features (→ news / claude.com/blog).
- Note: The most important "hidden extra blog" beyond the main site.

### anthropic.com/economic-futures
- Content: Hub for AI economics + labor-impact research. Includes the Anthropic Economic Index.
- Use for: how Claude is used across jobs, labor-market impact, adoption patterns, policy implications of AI deployment.

### github.com/anthropics
- Content: Anthropic GitHub org. claude-code, SDKs, cookbooks, prompt-engineering tutorials, courses, skills, plugins.
- Use for: SDK source / changelog, code examples and recipes, official plugins/skills, open-source eval or tooling projects.
- Skip for: prose blog content (→ engineering / claude.com/blog).

## Combined loops

- Research loop: research → alignment.anthropic.com → transformer-circuits.pub → economic-futures
- Build loop: engineering → claude.com/blog → release notes → github.com/anthropics
- Release loop: news → claude.com/blog → release notes

**Core loop** = research + engineering + platform release notes. Add alignment + transformer-circuits for the deeper safety/interpretability layer.
