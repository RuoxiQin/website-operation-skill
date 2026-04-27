# pi-without-skill

A pi agent with **no** skills loaded. This is the control: same model, same tools, same prompt as `pi-with-skill` — only the skill is missing.

## CLI mode

```bash
# from this directory, after `npm install`
npm run pi
```

`npm run pi` launches the locally-installed pi with `examples/.env` auto-loaded and `--no-skills` already passed (so the comparison stays clean even if you have personal skills installed).

> If you run `npx pi --no-skills` directly, your `.env` is NOT loaded. Either use `npm run pi`, or `export GEMINI_API_KEY=...` in the shell first.

## SDK mode

```bash
npm install
npx playwright install chromium       # one-time, ~120MB
# put GEMINI_API_KEY in examples/.env (see ../.env.example) — npm start auto-loads it
npm start                              # runs ../prompts/sample-task.txt
```

The SDK runner explicitly passes `noSkills: true` to `DefaultResourceLoader`, so it doesn't matter whether `.pi/skills/` exists in this directory.

Override the model with `MODEL=gemini-2.5-flash npm start` (default: `gemini-2.5-pro`). Use the **same** model in both runs — the variable being compared is the skill.
