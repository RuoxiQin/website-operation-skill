# pi-with-skill

A pi agent that **does** load the `website-operation` skill from `.pi/skills/website-operation/`. That directory symlinks `SKILL.md`, `scripts/`, and `references/` back to the top-level skill so edits flow through.

## CLI mode

```bash
# from this directory, after `npm install`
npm run pi
```

`npm run pi` launches the locally-installed pi with `examples/.env` auto-loaded (via Node's `--env-file-if-exists` flag). Pi discovers the skill at `.pi/skills/website-operation/` automatically — confirm with `/skills` inside pi, then paste a prompt of your choice from `../prompts/sample-tasks.json` as your first message.

> If you run `npx pi` directly, your `.env` is NOT loaded. Either use `npm run pi`, or `export GEMINI_API_KEY=...` in the shell first.

## SDK mode

```bash
npm install
npx playwright install chromium       # one-time, ~120MB
# put GEMINI_API_KEY in examples/.env (see ../.env.example) — npm start auto-loads it
npm start                              # runs the first prompt in ../prompts/sample-tasks.json
npm start -- anthropic-recent-learnings  # or pick a specific prompt by name
```

Override the model with `MODEL=gemini-2.5-flash npm start` (default: `gemini-2.5-pro`), or set `MODEL=...` in `.env`.

The runner streams the assistant's text to stdout and tool calls to stderr — pipe stdout to a file and watch stderr live:

```bash
npm start > run.log 2>&1
```
