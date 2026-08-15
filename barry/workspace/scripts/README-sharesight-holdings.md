# Sharesight holdings fetcher

Fetches an up-to-date holdings valuation for these portfolios:

- Erika (`1231212`)
- Nick (`1231095`)
- GrumpyFund (`1259505`)

It uses Sharesight OAuth `client_credentials`, then the V2 valuation report endpoint:

- `POST /oauth2/token`
- `GET /api/v2/portfolios/{id}/valuation.json` once per portfolio

Default run = **4 HTTP requests total**. It does not call one endpoint per holding.

## Usage

No secrets are stored in the script.

By default, credentials are read from the unlocked Bitwarden item:

- `Nick's sharesight API key`

```bash
./run_sharesight_holdings
```

Operational note: Bitwarden is commonly locked at the start of a fresh session. Try `./run_sharesight_holdings` first, but expect it may fail with a locked-vault message. If it does, ask Nick to unlock Bitwarden and then rerun:

```bash
export BW_SESSION="$(bw unlock --raw)"
./run_sharesight_holdings
```

Write CSV to a file:

```bash
./run_sharesight_holdings --output holdings.csv
```

JSON output:

```bash
./run_sharesight_holdings --format json --output holdings.json
```

Use a different Bitwarden item name/id:

```bash
./run_sharesight_holdings --bw-item "Nick's sharesight API key"
```

You can still override credentials with environment variables if desired:

```bash
SHARESIGHT_CLIENT_ID="..." SECRET="..." ./run_sharesight_holdings
```

or:

```bash
SHARESIGHT_CLIENT_ID="..." SHARESIGHT_CLIENT_SECRET="..." ./run_sharesight_holdings --output holdings.csv
```

Optional date:

```bash
./run_sharesight_holdings --balance-date 2026-05-29
```

Override portfolios if needed:

```bash
./run_sharesight_holdings \
  --portfolio Nick=1231095 \
  --portfolio Erika=1231212
```
