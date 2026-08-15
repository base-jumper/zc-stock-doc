---
name: install-script
description: Install a repository script as a command-line command using this workspace's scripts/bin wrapper convention. Use when the user asks to install a script, make a script runnable from the CLI or PATH, or gives a request such as "/install-script mobility_panels.py" or "make mobility_panels.py runnable from the cli".
---

# Install Script

Make a requested repository script runnable from any directory through the workspace's `scripts/bin` command-wrapper system.

## Workflow

1. Resolve the requested source file.

   - Treat a bare filename as a search request. Use `rg --files` to find it in the workspace, including untracked files.
   - If there is exactly one matching file, use its workspace-relative path. If there are multiple matches, use the user's context to choose; ask only when the choice cannot be made safely.
   - Confirm that the target is a script and inspect its shebang, extension, and nearby documentation for interpreter or virtual-environment requirements.
   - Keep the source script in its existing location. The installed command is a wrapper, not a copy.

2. Choose the command name.

   - For `name.py`, default to `name` (for example, `mobility_panels.py` becomes `mobility_panels`).
   - Preserve an explicitly requested command name.
   - Keep names safe for a shell command: lowercase letters, digits, underscores, hyphens, and periods only; do not use path separators.

3. Create or update `scripts/bin/<command>`.

   Use a symlink-safe wrapper that resolves the repository even when invoked through `~/.local/bin`:

   ```bash
   #!/usr/bin/env bash
   # Wrapper: resolves to the repo even when invoked via a symlink on PATH.
   self="$(readlink -f "${BASH_SOURCE[0]}")"
   root="$(cd "$(dirname "$self")/../.." && pwd)"
   exec python3 "$root/<workspace-relative-source.py>" "$@"
   ```

   For a shell script, use `exec bash "$root/<workspace-relative-source.sh>" "$@"` (or the interpreter required by its shebang). For a script requiring a dedicated environment, follow the existing specialized wrapper pattern, such as `scripts/bin/yfin`.

   Use `apply_patch` to create or update the wrapper, then run `chmod +x scripts/bin/<command>`.

4. Register the command.

   - Add the command to the `commands=(...)` array in `scripts/bin/install.sh` unless it is already present.
   - Add one row to the command table in `scripts/bin/README.md`, using the workspace-relative source path.
   - Keep existing ordering and formatting. Do not alter unrelated wrappers or documentation.

5. Validate the installation.

   - Confirm the source exists and the wrapper points to it.
   - Run `bash -n scripts/bin/<command>` and `bash -n scripts/bin/install.sh`.
   - If the target supports a harmless help/version invocation, run it through the wrapper from outside the repository to verify argument forwarding and path resolution. Do not run commands that mutate data merely to test installation.
   - Report the command name, source path, and the fact that `scripts/bin/install.sh` must be run (or re-run) to symlink it into `~/.local/bin`.
