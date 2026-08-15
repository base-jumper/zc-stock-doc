#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/.." && pwd)"
cd "$repo"

# Force the dedicated zc-stock-doc GitHub key even if global SSH config changes.
export GIT_SSH_COMMAND="ssh -i $HOME/.ssh/github-zc-stock-doc -o IdentitiesOnly=yes"

# Stage all tracked/untracked changes, respecting .gitignore.
git add -A

# Commit only when there is something staged.
if git diff --cached --quiet; then
  echo "No workspace changes to back up."
  exit 0
fi

commit_msg="Daily workspace backup: $(date +%Y-%m-%d)"
git commit -m "$commit_msg"

git push origin HEAD
