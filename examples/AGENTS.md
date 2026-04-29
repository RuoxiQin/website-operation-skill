# Project rules — read carefully, these override your defaults

These are environment facts and hard rules for any agent run from this directory tree. They are **not** suggestions.

## Rule 1: Never run `npm install` outside the project working directory

The user has deliberately opted out of global npm installs. Each example directory has its own pinned `node_modules/` (containing `playwright`, pi, etc.).

- **MUST**: write any Node script you intend to run inside the current working directory — typically at `./.tmp/script.mjs`. Create the `./.tmp/` directory first if it doesn't exist (`mkdir -p .tmp`).
- **MUST NOT**: write Node scripts to `/tmp/` or any directory outside cwd. Node resolves `node_modules/` by walking up from the script's directory, so a script in `/tmp` cannot see this project's installed packages. Putting it there forces a wasteful `npm install` in `/tmp`.
- **MUST NOT**: run `npm install <pkg>` in `/tmp` or anywhere outside the project to "fix" an `ERR_MODULE_NOT_FOUND`. If a required dep genuinely isn't available, **stop and tell the user** — they will run `npm install` here themselves.

## Rule 2: Path conventions for ephemeral artifacts

| Artifact                           | Where it goes                                           |
| :--------------------------------- | :------------------------------------------------------ |
| Node scripts you author and run    | `./.tmp/<name>.mjs` (cwd, so `import` finds local deps) |
| Browser user-data-dirs             | `os.tmpdir()` (truly throwaway)                         |
| Screenshots, HTML dumps, JSON      | cwd, `./.tmp/`, or wherever the user explicitly asked   |

`./.tmp/` is in `.gitignore`, so it won't pollute the repo.

## Rule 3: Install missing packages inside `./.tmp/` if needed

If a required package is missing, install it inside `./.tmp/` — never in `/tmp`, globally, or anywhere outside cwd. Create `./.tmp/` first if it doesn't exist (`mkdir -p .tmp`).

- **For Python**: create a virtual environment at `./.tmp/.venv` (`python3 -m venv .tmp/.venv`), activate it (`source .tmp/.venv/bin/activate`), then run `pip install <pkg>`. Write and run any Python scripts inside `./.tmp/` as well.
- **For Node**: run `npm install <pkg>` inside `./.tmp/` so the package lands in `./.tmp/node_modules/`. Write and run any Node scripts inside `./.tmp/`.
- **MUST NOT**: install packages globally, in `/tmp`, or anywhere outside `./.tmp/`.
