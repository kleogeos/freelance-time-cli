# freelance-time-cli

[![Test CLI](https://github.com/kleogeos/freelance-time-cli/actions/workflows/test.yml/badge.svg)](https://github.com/kleogeos/freelance-time-cli/actions/workflows/test.yml)

Track billable hours per project from the command line. No dependencies, no sign-up, no cloud account — just a local JSON file you can commit, back up, or diff.

```bash
python3 track.py start acme --note "logo design"
# ... work ...
python3 track.py stop
python3 track.py add 3.5 acme --note "backfill yesterday"
python3 track.py report --rate 50
```

```
acme                     3.50h   $175.00
beta                     2.00h   $100.00
----------------------------------------
TOTAL                    5.50h   $275.00
```

### Install (optional)

```bash
pip install git+https://github.com/kleogeos/freelance-time-cli
freelance-time start acme
```

### Commands

| Command | What it does |
|---|---|
| `start [project] [--note TEXT]` | Start a live timer for a project (default project name: `default`) |
| `stop` | Stop the running timer and log the elapsed hours |
| `status` | Show the currently running timer, if any |
| `add HOURS [project] [--note TEXT]` | Manually log hours without a live timer (for work you forgot to start/stop) |
| `report [--project NAME] [--rate N] [--json]` | Totals per project, optionally valued at an hourly rate |

Global flag: `--file PATH` — use a different timesheet file (default `timesheet.json` in the current directory). Useful for keeping one file per client.

### Why a CLI instead of a time-tracking app

No account, no subscription, no browser tab that needs to stay open, nothing phoning home. The timesheet is a plain JSON file — read it, script against it, or point `report --rate` at it when it's invoice day. Pairs with [freelance-invoice-cli](https://github.com/kleogeos/freelance-invoice-cli) for turning the hours into an actual invoice, and [freelance-rate-cli](https://github.com/kleogeos/freelance-rate-cli) for figuring out what the rate should be in the first place.

Free web tools (no install): [invoice generator](https://kleogeos.github.io/freelancer-tools/invoice.html) · [rate calculator](https://kleogeos.github.io/freelancer-tools/rate-calculator.html) · [contract checklist](https://kleogeos.github.io/freelancer-tools/contract-checklist.html)

Need the paperwork beyond tracking — proposals, contracts, invoices, late-payment emails, client scripts? [Freelancer Starter Kit ($15, pay with crypto)](https://kleogeos.github.io/freelancer-tools/kit.html)

Free and will stay free. If it saved you time: [tip with crypto](https://kleogeos.github.io/freelancer-tools/donate.html).

## License

MIT — do whatever you want with it.
