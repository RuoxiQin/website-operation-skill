---
name: website-operation
description: Look up an indexed map of a website's structure before browsing or searching it. Use when a task involves reading, browsing, or searching a specific website (e.g. "find Anthropic's interpretability research", "check the Claude release notes") so you know which sub-domain or section to target. Skip this skill if the website you need is not indexed.
allowed-tools: Bash, Read
---

# Website operation

This skill ships a small index of websites whose structure has been mapped out for you. Before you spend time crawling, searching, or guessing URLs on a website, check whether it's indexed here — if it is, you get a reference doc that tells you exactly which section / sub-domain to read for which kind of question.

## How to use

1. Identify the **main domain** of the website you want to operate on. Use the bare apex domain only — e.g. `anthropic.com`, not `https://www.anthropic.com/research` or `research.anthropic.com`.

2. Run the check script with that domain:

   ```bash
   bash scripts/check_domain.sh <domain>
   ```

   - If indexed, the script prints the path to the reference doc. **Read that file** before doing anything else with the site — it will tell you which sub-section to target.
   - If not indexed, the script prints `not indexed` and exits non-zero. In that case this skill has nothing useful for the site; skip it and proceed with your usual browsing/search approach.

3. Use the guidance in the reference doc to pick the right section, then browse / fetch / search as you normally would.

## Example

```bash
$ bash scripts/check_domain.sh anthropic.com
references/anthropic.com.md

$ bash scripts/check_domain.sh example.com
not indexed
```

When indexed, follow up by reading the printed reference file.
