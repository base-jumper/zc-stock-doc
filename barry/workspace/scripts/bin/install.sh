#!/usr/bin/env bash
# Symlink the stock-analysis command wrappers into a directory on your PATH.
#
# Usage:
#   ./install.sh            # installs into ~/.local/bin
#   BIN=~/bin ./install.sh  # installs into a different directory
set -euo pipefail

here="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
root="$(cd "$here/../.." && pwd)"
BIN="${BIN:-$HOME/.local/bin}"
mkdir -p "$BIN"

# The yahoo-finance skill ships a Python CLI (yfin) that needs yfinance. Build a
# dedicated, pinned virtualenv for it so the wrapper has deterministic deps.
YF_VERSION="${YF_VERSION:-1.4.1}"
yf_venv="$root/.venv/yahoo-finance"
echo "installing yfinance==$YF_VERSION (+lxml) into the yahoo-finance venv at $yf_venv"
if command -v uv >/dev/null 2>&1; then
  [[ -x "$yf_venv/bin/python" ]] || uv venv --quiet "$yf_venv"
  VIRTUAL_ENV="$yf_venv" uv pip install --quiet "yfinance==$YF_VERSION" lxml
else
  [[ -x "$yf_venv/bin/python" ]] || python3 -m venv "$yf_venv"
  "$yf_venv/bin/python" -m pip install --quiet --upgrade pip
  "$yf_venv/bin/python" -m pip install --quiet "yfinance==$YF_VERSION" lxml
fi

commands=(company_score asymmetric_payoff exit_multiple tam_capture tam_capture_inputs
          weighted_average conservative_debt returns_on_capital free_cash_flow earnings_quality
          durable_growth capital_allocation organic_growth fundamental_stability downside_support
          stock_doc stock_queue market_queue yfin edgar market_doc penetration_fit concentration_fit
          mobility_panels mobility_fit stock_announcements test_stock_announcements)

for cmd in "${commands[@]}"; do
  chmod +x "$here/$cmd"
  ln -sf "$here/$cmd" "$BIN/$cmd"
  echo "linked $BIN/$cmd -> $here/$cmd"
done

case ":$PATH:" in
  *":$BIN:"*) ;;
  *) echo "NOTE: $BIN is not on your PATH. Add it, e.g.:"
     echo '      echo '\''export PATH="$HOME/.local/bin:$PATH"'\'' >> ~/.bashrc' ;;
esac

echo "Done. Open a new shell (or run 'hash -r') and try: company_score HMC.AX freeroll --dry-run"
