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
- Content: Research publication hub.
- Subareas: Alignment, Interpretability, Societal Impacts, Frontier Red Team, Economic Research, Policy.
- Date Format: `MMM D, YYYY` (e.g., `Apr 2, 2026`). Single-digit days are NOT zero-padded.
- Navigation: Use "See more" links at the bottom of each section to load older papers.
- Use for: new findings, safety papers, jailbreak/red-team work, evaluation methods, AI impact studies.
- Skip for: applied agent-building (→ engineering), product news (→ news), deep mechanistic interp (→ transformer-circuits.pub).

### anthropic.com/engineering
- Content: Engineering systems blog — building reliable AI systems. 
- Format: List of articles with title, snippet, and publication date.
- Date Format: Typically uses `MMM DD, YYYY` (e.g., `Apr 08, 2026`). Note the leading zero on the day.
- Structure: Featured article at the top, followed by a grid/list of historical posts.
- Use for: how to build/evaluate agents, design tools for agents, harness patterns, infra tradeoffs, failure reports.
- Skip for: product announcements (→ news), scientific findings (→ research).
- Note: Usually the most practically useful section for LLM/agent developers.
- Tooling: A dedicated scraping script is available for this section. Run `python3 scripts/anthropic.engineering.py [output_path]` (requires `beautifulsoup4` and `markdownify`) to fetch and convert the engineering blog into a clean markdown file with absolute URLs and fixed formatting.

### anthropic.com/news
- Content: Newsroom. 
- Format: Articles tagged by type (Product, Announcements).
- Date Format: `MMM D, YYYY` (e.g., `Apr 7, 2026`). Single-digit days are NOT zero-padded.
- Use for: official announcements, model releases, product launches, partnerships, policy/election/safety announcements.
- Skip for: technical depth (→ engineering or release notes).

### claude.com/blog
- Content: Claude product + best-practices blog. 
- Categories: 
  - **Category**: Agents, Claude Code, Enterprise AI, Product announcements.
  - **Product**: Claude Enterprise, Claude apps, Claude Platform, Claude Code.
  - **Use case**: Agents, Business, Coding, Content Creation, Design, Education, Financial services, Government, Healthcare, Learning, Legal, Productivity, Sales, Work.
- Date Format: Typically uses `MMM DD, YYYY` (e.g., `Apr 08, 2026`).
- Navigation: Features a "Filter and sort" accordion for drilling down by Category, Product, or Use Case. 
- Pagination: Uses a "Next" button/link for more content. Some sections may have a "View more" link.
- Use for: productized agent patterns, Claude Code workflows, enterprise rollouts, MCP from a product angle. Sits between News and Engineering.
- Skip for: API changelog (→ release notes), academic findings (→ research).

### platform.claude.com/docs/en/release-notes/overview
- Content: Claude Platform release notes. 
- Structure: API, SDK, Console, model deprecations, beta headers, managed agents, rate limits.
- Navigation: Sidebar contains detailed version history and sub-sections for different services.
- Use for: authoritative "what changed in the API" lookups.
- Skip for: conceptual explanations or how-to (→ engineering / claude.com/blog).

### transformer-circuits.pub
- Content: Dedicated interpretability research site. 
- Structure: Mechanistic interp papers, research notes, interactive articles.
- Date Format: Grouped by month/year headers (e.g., `APRIL 2026`).
- Use for: sparse autoencoders, features, circuits, activation-level explanations, model internals.
- Skip for: alignment policy / red-team work (→ research or alignment.anthropic.com).

### alignment.anthropic.com
- Content: Alignment Science Blog. Research notes and early findings that don't warrant a full publication.
- Structure: Chronological list of articles grouped by month/year headers (e.g., `APRIL 2026`).
- Use for: alignment auditing, sandbagging, weak-to-strong generalization, automated alignment researchers, hidden behaviors, model organisms, safety evaluations.
- Skip for: production safety features (→ news / claude.com/blog).
- Note: The most important "hidden extra blog" beyond the main site.

### anthropic.com/economic-futures
- Content: Hub for AI economics + labor-impact research. Includes the Anthropic Economic Index.
- Structure: Latest updates are often displayed in a table with columns: `DATE`, `CATEGORY`, `TITLE`.
- Date Format: `MMM DD, YYYY` (e.g., `Jan 15, 2026`).
- Use for: how Claude is used across jobs, labor-market impact, adoption patterns, policy implications of AI deployment.

### github.com/anthropics
- Content: Anthropic GitHub org. 
- Key Repositories:
  - `claude-code`: Agentic terminal tool.
  - `skills`: Agent Skills repository.
  - `claude-cookbooks`: Recipes and notebooks for Claude use cases.
  - `prompt-eng-interactive-tutorial`: Interactive prompt engineering.
  - `courses`: Educational content.
- Use for: SDK source / changelog, code examples and recipes, official plugins/skills, open-source eval or tooling projects.
- Skip for: prose blog content (→ engineering / claude.com/blog).

## Combined loops

- Research loop: research → alignment.anthropic.com → transformer-circuits.pub → economic-futures
- Build loop: engineering → claude.com/blog → release notes → github.com/anthropics
- Release loop: news → claude.com/blog → release notes

**Core loop** = research + engineering + platform release notes. Add alignment + transformer-circuits for the deeper safety/interpretability layer.
