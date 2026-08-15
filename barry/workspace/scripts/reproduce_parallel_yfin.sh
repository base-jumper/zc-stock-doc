#!/usr/bin/env bash
set -uo pipefail

# Reproduce all 15 calls launched concurrently by the stock-analysis FIFO cron
# run on 2026-08-12: eight yfin calls and seven Python analysis scripts.

ticker="${1:-005380.KS}"
output_dir="${2:-$(mktemp -d /tmp/parallel-yfin.XXXXXX)}"
script_path="$(readlink -f "${BASH_SOURCE[0]}")"
workspace_root="$(cd "$(dirname "$script_path")/.." && pwd)"
mkdir -p "$output_dir"

commands=(
  "yfin quote $ticker"
  "yfin info $ticker"
  "yfin income $ticker -n 5"
  "yfin balance $ticker -n 5"
  "yfin cashflow $ticker -n 5"
  "yfin metrics $ticker -n 5"
  "yfin dividends $ticker -n 12"
  "yfin estimates $ticker"
  "python3 skills/stock-analysis/scripts/downside_support.py $ticker --format json"
  "python3 skills/stock-analysis/scripts/fundamental_stability.py $ticker --format json"
  "python3 skills/stock-analysis/scripts/earnings_quality.py $ticker --format json"
  "python3 skills/stock-analysis/scripts/free_cash_flow.py $ticker --format json"
  "python3 skills/stock-analysis/scripts/conservative_debt.py $ticker --format json"
  "python3 skills/stock-analysis/scripts/returns_on_capital.py $ticker --format json"
  "python3 skills/stock-analysis/scripts/capital_allocation.py $ticker --format json"
)

printf 'Launching %d concurrent stock-data processes for %s\n' "${#commands[@]}" "$ticker"
printf 'Logs: %s\n' "$output_dir"
printf 'Working directory: %s\n' "$workspace_root"
printf 'Memory before:\n'
free -h

pids=()
for index in "${!commands[@]}"; do
  command_text="${commands[$index]}"
  log_prefix="$output_dir/$(printf '%02d' "$((index + 1))")"

  (
    printf 'Command: %s\n' "$command_text" >"$log_prefix.command"
    /usr/bin/time -v bash -lc "cd \"$workspace_root\" && $command_text" \
      >"$log_prefix.stdout" \
      2>"$log_prefix.stderr"
  ) &
  pids+=("$!")
done

failures=0
for index in "${!pids[@]}"; do
  if wait "${pids[$index]}"; then
    status=0
  else
    status=$?
    failures=$((failures + 1))
  fi
  printf '%02d exit=%d  %s\n' "$((index + 1))" "$status" "${commands[$index]}"
done

printf 'Memory after:\n'
free -h
printf 'Peak RSS by process:\n'
for stderr_file in "$output_dir"/*.stderr; do
  peak_rss="$(sed -n 's/^[[:space:]]*Maximum resident set size (kbytes):[[:space:]]*//p' "$stderr_file")"
  printf '%s\t%s kB\n' "$(basename "$stderr_file" .stderr)" "${peak_rss:-unknown}"
done

printf 'Completed with %d failed command(s). Logs retained at %s\n' "$failures" "$output_dir"
exit "$failures"
