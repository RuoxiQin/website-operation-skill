# anthropic.com

`anthropic.com` is the website of **Anthropic**, the company that created Claude. It's a rich source for LLM development tips, learning material, safety/interpretability research, and new product launches. Anthropic also runs several adjacent properties (Claude product site, alignment blog, interpretability site, GitHub) that are part of the same ecosystem — they're listed below because they're usually what you actually want when someone says "check Anthropic's site."

Use this map to pick the right section *before* you browse or search. Going to the wrong sub-section is the most common reason agents fail to find Anthropic content that does exist.

## Mental model

| Section | What it is | Best for |
|---|---|---|
| `anthropic.com/research` | Anthropic's research publication hub. Alignment, interpretability, societal impacts, frontier red-teaming, economic research, policy, science. | New research findings, safety papers, interpretability work, evaluation methods, AI impact studies. Start here for **"what did Anthropic discover?"** |
| `anthropic.com/engineering` | Technical engineering blog about building reliable AI systems and agent infrastructure. | Agent design, evals, Claude Code, MCP / tool use, context engineering, harnesses, infrastructure lessons, postmortems. Start here for **"how do they build agents/systems?"** |
| `anthropic.com/news` | Company newsroom: product launches, partnerships, announcements, press-facing updates. | Model releases, product announcements, policy announcements, partnerships. Less "researchy." |

## Section details

### 1. anthropic.com/research

The closest thing to Anthropic's research blog / publication index. Teams investigate "the safety, inner workings, and societal impacts of AI models," divided into Alignment, Economic Research, Interpretability, Societal Impacts, and Frontier Red Team.

Track here:

- interpretability findings (emotion concepts, model internals, circuit tracing)
- alignment and scalable oversight work
- jailbreak, red-team, safety and classifier work
- societal impact and economic-index studies
- policy-adjacent technical research

**Research = Anthropic's "new findings" layer.**

### 2. anthropic.com/engineering

Anthropic's engineering systems blog: "Engineering at Anthropic: Inside the team building reliable AI systems." Recent posts cover managed agents, Claude Code auto mode, long-running application harnesses, infrastructure noise in agentic coding evals, technical evaluations, tool use, MCP, context engineering, and agent best practices.

For an LLM/agent developer, this is often the most practically useful section. Less "what did we discover scientifically?" and more:

- how to build agent harnesses
- how to evaluate agents
- how to design tools for agents
- how Claude Code is secured and improved
- how Anthropic thinks about context engineering
- failure reports and postmortems

**Engineering = applied lessons for building LLM/agent systems.**

### 3. anthropic.com/news

The newsroom. Product launches, company announcements, partnerships, policy updates, press contact info.

Read this for:

- new Claude model releases
- product launches
- Anthropic partnerships
- public policy / election / safety announcements
- company-level strategic moves

**News = official announcements, not technical depth.**

## Adjacent official properties

These are not on `anthropic.com` itself but are part of the same ecosystem and frequently the right destination.

### claude.com/blog

The Claude product and best-practices blog: "Product news and best practices for teams building with Claude." Categories include Agents, Claude Code, Enterprise AI, Product announcements, Coding, Productivity, Work.

Sits between News and Engineering — more practical than News, less research-heavy than Research. Useful for Claude Code, agents, enterprise workflows, MCP, productized agent patterns.

### platform.claude.com/docs/en/release-notes/overview

Claude Platform release notes. Covers API, SDK, Console, model deprecations, beta headers, managed agents, rate limits, and platform-level changes.

Important because blog posts explain concepts but **release notes tell you what actually changed in the API**.

### transformer-circuits.pub

Anthropic's dedicated interpretability research site — "Anthropic's Interpretability Research." Mechanistic interpretability papers, notes, updates, interactive research articles.

Use for:

- mechanistic interpretability
- sparse autoencoders
- features
- circuits
- model internals
- activation-level explanations

More specialized and research-heavy than the main Research page.

### alignment.anthropic.com

Anthropic's Alignment Science Blog. Releases research notes and early findings that may not warrant a full publication but are still useful to researchers.

Use for:

- alignment auditing
- sandbagging
- weak-to-strong generalization
- automated alignment researchers
- hidden behaviors
- model organisms
- safety evaluations

Probably the most important "hidden extra blog" beyond the main website.

### anthropic.com/economic-futures

Hub for Anthropic's AI economics and labor impact research. Supports research and policy development for AI's economic impacts; includes the Anthropic Economic Index.

Use for:

- how Claude is used across jobs
- labor-market impact
- AI adoption patterns
- policy implications of AI deployment

### Anthropic GitHub (github.com/anthropics)

Anthropic's GitHub org. Includes claude-code, SDKs, cookbooks, prompt engineering tutorials, courses, skills, and plugins.

Use for:

- SDK changes
- Claude Code changelogs
- examples and recipes
- official plugins / skills
- open-source evaluation or tooling projects

## Recommended reading workflow

**For new research findings:**

1. anthropic.com/research
2. alignment.anthropic.com
3. transformer-circuits.pub
4. anthropic.com/economic-futures (if interested in AI labor/economics)

**For agent-building practice:**

1. anthropic.com/engineering
2. claude.com/blog
3. Claude Platform release notes
4. Anthropic GitHub

**For model/product changes:**

1. anthropic.com/news
2. claude.com/blog
3. Claude Platform release notes

Treat **Research + Engineering + Claude Platform release notes** as the core loop. Add the Alignment Science Blog and Transformer Circuits for the deeper safety/interpretability layer.
