# Comparison harness

Two pi-agent setups, identical except for one variable: whether the [`website-operation`](../SKILL.md) skill is loaded.

| Directory                                  | Skill loaded? | Purpose                                     |
| :----------------------------------------- | :------------ | :------------------------------------------ |
| [pi-with-skill/](pi-with-skill/)           | yes           | The treatment — agent gets the playbook     |
| [pi-without-skill/](pi-without-skill/)     | no            | The control — same model, same tools, no playbook |

Both run the same prompt from [prompts/sample-task.txt](prompts/sample-task.txt). The skill is a single source of truth: `pi-with-skill/.pi/skills/website-operation/SKILL.md` is a symlink to the top-level [`SKILL.md`](../SKILL.md).

Both agents also load [`AGENTS.md`](AGENTS.md) — environment facts (use the project's local `node_modules/`, write scripts in cwd, etc.) that aren't part of the variable being compared. Pi auto-discovers `AGENTS.md` by walking up from cwd.

## One-time setup

```bash
( cd pi-with-skill    && npm install )           # installs pi locally to this example
( cd pi-without-skill && npm install )           # ditto for the control
npx playwright install chromium                  # browser the agent will drive
cp .env.example .env && $EDITOR .env             # put your GEMINI_API_KEY here (one place, picked up by both runners)
```

No global install needed — pi is a local dependency of each example. CLI commands use `npx pi`, which resolves to the local copy in `node_modules/.bin`.

The SDK runners auto-load `examples/.env` via Node's built-in `--env-file-if-exists` flag (Node 20.6+). For CLI mode, either `export GEMINI_API_KEY=...` in your shell or `set -a; source .env; set +a` once per terminal (run from `examples/`).

## CLI mode (interactive, side-by-side)

Open two terminals:

```bash
# Terminal 1
cd examples/pi-with-skill
npm run pi                 # auto-loads ../.env
# inside pi: type /skills to confirm "website-operation" is listed,
# then paste the contents of ../prompts/sample-task.txt
```

```bash
# Terminal 2
cd examples/pi-without-skill
npm run pi                 # auto-loads ../.env, passes --no-skills
# inside pi: /skills should show nothing,
# then paste the same prompt
```

> `npm run pi` is a wrapper that loads `examples/.env` before launching pi. If you invoke `npx pi` directly, `.env` is **not** loaded — you'd need to `export GEMINI_API_KEY=...` in the shell first.

Watch them diverge in real time.

## SDK mode (scripted, captures transcripts)

```bash
( cd examples/pi-with-skill    && npm install && npm start ) > with-skill.log    2> with-skill.err    &
( cd examples/pi-without-skill && npm install && npm start ) > without-skill.log 2> without-skill.err &
wait

diff -u without-skill.log with-skill.log | less
```

Both runners stream the assistant's text to **stdout** and tool calls to **stderr**, so the `.log` files are clean transcripts you can diff directly.

## What to look for in the comparison

The skill teaches a specific Playwright playbook. With the skill, expect to see:

- A single Node script written to a tmp file and run once (not a series of one-shot bash calls)
- `chromium.launchPersistentContext` instead of `chromium.launch`
- `waitForSelector` / `waitForLoadState` instead of `setTimeout`
- `getByRole` / `getByText` selectors instead of brittle CSS
- An `hn-comments.png` screenshot actually saved (the skill explicitly tells the agent to capture evidence)
- Structured JSON output via `evaluateAll`, not paraphrased prose

Without the skill, common failure modes:

- Trying `curl` first and getting unrendered HTML
- Sleeping arbitrary seconds and missing the content
- Guessing CSS selectors that don't match
- Forgetting the screenshot
- Returning a summary instead of the requested JSON shape

## Customizing

- **Different prompt**: drop a file in `prompts/` and pass its path: `npm start -- ../prompts/my-task.txt`
- **Different model**: `MODEL=gemini-2.5-flash npm start` (use the same model in both runs; default is `gemini-2.5-pro`)
- **Edit the skill**: edit `../SKILL.md` — the with-skill agent picks up the change on next run, since the project skill file is a symlink to it
