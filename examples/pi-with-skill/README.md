# pi-with-skill

A pi agent that **does** load the `website-operation` skill from `.pi/skills/website-operation/SKILL.md` (a symlink to the top-level `SKILL.md`).

## CLI mode

```bash
# from this directory, after `npm install`
npm run pi
```

`npm run pi` launches the locally-installed pi with `examples/.env` auto-loaded (via Node's `--env-file-if-exists` flag). Pi discovers the skill at `.pi/skills/website-operation/` automatically — confirm with `/skills` inside pi, then paste the contents of `../prompts/sample-task.txt` as your first message.

> If you run `npx pi` directly, your `.env` is NOT loaded. Either use `npm run pi`, or `export GEMINI_API_KEY=...` in the shell first.

## SDK mode

```bash
npm install
npx playwright install chromium       # one-time, ~120MB
# put GEMINI_API_KEY in examples/.env (see ../.env.example) — npm start auto-loads it
npm start                              # runs ../prompts/sample-task.txt
npm start -- ./my-prompt.txt           # or pass a custom prompt file
```

Override the model with `MODEL=gemini-2.5-flash npm start` (default: `gemini-2.5-pro`), or set `MODEL=...` in `.env`.

The runner streams the assistant's text to stdout and tool calls to stderr — pipe stdout to a file and watch stderr live:

```bash
npm start > run.log 2>&1
```
