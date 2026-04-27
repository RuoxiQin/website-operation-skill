#!/usr/bin/env bash
# Check whether a given website domain is indexed by this skill.
# Usage: bash scripts/check_domain.sh <domain>
#   <domain> must be a bare apex domain like "anthropic.com" — no scheme,
#   no subdomain, no path. Examples of accepted input: "anthropic.com",
#   "example.co.uk". Examples that will be rejected: "https://anthropic.com",
#   "research.anthropic.com", "anthropic.com/news".
#
# On success: prints the relative path to the reference doc and exits 0.
# On miss:    prints "not indexed" and exits 1.
# On bad input: prints a usage error to stderr and exits 2.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: bash scripts/check_domain.sh <domain>" >&2
  echo "  <domain> must be a bare apex domain, e.g. anthropic.com" >&2
  exit 2
fi

domain="$1"

# Reject anything that isn't a plain apex domain.
if [[ "$domain" =~ ^https?:// ]] \
   || [[ "$domain" == */* ]] \
   || [[ ! "$domain" =~ ^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
  echo "error: '$domain' is not a bare apex domain (e.g. anthropic.com)" >&2
  exit 2
fi

# Normalize to lowercase and strip a leading "www." if present.
domain="$(echo "$domain" | tr '[:upper:]' '[:lower:]')"
domain="${domain#www.}"

# Resolve the references directory relative to this script, so the skill
# works regardless of the caller's current working directory.
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd "$script_dir/.." && pwd)"
ref_file="references/${domain}.md"

if [[ -f "${skill_root}/${ref_file}" ]]; then
  echo "${ref_file}"
  exit 0
fi

echo "not indexed"
exit 1
