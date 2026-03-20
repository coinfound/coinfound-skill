# CoinFound RWA Skills

CoinFound RWA skill set for data access and schema probing.

## Available Skills

- `coinfound-rwa-read`
  - Read CoinFound RWA data
- `coinfound-rwa-schema-probe`
  - Probe endpoint schemas when documentation is incomplete

## Installation

After publishing this repository to GitHub, install skills from their skill directories:

```text
$skill-installer install https://github.com/<your-org>/<your-repo>/tree/main/skills/coinfound-rwa-read
$skill-installer install https://github.com/<your-org>/<your-repo>/tree/main/skills/coinfound-rwa-schema-probe
```

## Quick Usage

Read RWA overview:

```bash
python3 shared/coinfound_rwa/scripts/fetch_rwa.py \
  --endpoint-key market-overview.main-asset-classes.summary
```

Read stablecoin overview:

```bash
python3 shared/coinfound_rwa/scripts/fetch_rwa.py \
  --endpoint-key stable-coin.aggregates
```

Probe a dataset schema:

```bash
python3 shared/coinfound_rwa/scripts/probe_schema.py \
  --endpoint-key stable-coin.dataset \
  --path-params '{"ticker":"USDT"}'
```

Run tests:

```bash
python3 -m unittest discover -s shared/coinfound_rwa/tests -v
```

## License

MIT. See `LICENSE`.
