#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

DEFAULT_FILE = "timesheet.json"


def _load(path):
    if not os.path.exists(path):
        return {"running": None, "entries": []}
    with open(path) as f:
        return json.load(f)


def _save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def cmd_start(args):
    data = _load(args.file)
    if data["running"] is not None:
        print(f"Already tracking '{data['running']['project']}' since {data['running']['start']}. Run 'stop' first.", file=sys.stderr)
        sys.exit(1)
    data["running"] = {
        "project": args.project or "default",
        "start": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": args.note or "",
    }
    _save(args.file, data)
    print(f"Started tracking '{data['running']['project']}' at {data['running']['start']}")


def cmd_stop(args):
    data = _load(args.file)
    running = data["running"]
    if running is None:
        print("Not currently tracking anything. Run 'start' first.", file=sys.stderr)
        sys.exit(1)
    start = datetime.fromisoformat(running["start"])
    end = datetime.now(timezone.utc)
    hours = (end - start).total_seconds() / 3600
    entry = {
        "project": running["project"],
        "start": running["start"],
        "end": end.isoformat(timespec="seconds"),
        "hours": round(hours, 4),
        "note": running["note"],
    }
    data["entries"].append(entry)
    data["running"] = None
    _save(args.file, data)
    print(f"Stopped '{entry['project']}' — {entry['hours']:.2f}h logged.")


def cmd_status(args):
    data = _load(args.file)
    running = data["running"]
    if running is None:
        print("Not currently tracking.")
        return
    start = datetime.fromisoformat(running["start"])
    elapsed = (datetime.now(timezone.utc) - start).total_seconds() / 3600
    print(f"Tracking '{running['project']}' — {elapsed:.2f}h so far (started {running['start']}).")


def cmd_add(args):
    data = _load(args.file)
    data["entries"].append({
        "project": args.project or "default",
        "start": None,
        "end": None,
        "hours": round(args.hours, 4),
        "note": args.note or "",
    })
    _save(args.file, data)
    print(f"Added {args.hours:.2f}h to '{args.project or 'default'}'.")


def cmd_report(args):
    data = _load(args.file)
    entries = data["entries"]
    if args.project:
        entries = [e for e in entries if e["project"] == args.project]
    by_project = {}
    for e in entries:
        by_project.setdefault(e["project"], 0.0)
        by_project[e["project"]] += e["hours"]
    total_hours = sum(by_project.values())
    rate = args.rate or 0

    if args.json:
        print(json.dumps({
            "by_project": {k: round(v, 2) for k, v in by_project.items()},
            "total_hours": round(total_hours, 2),
            "rate": rate,
            "total_due": round(total_hours * rate, 2) if rate else None,
        }, indent=2))
        return

    if not entries:
        print("No logged time yet.")
        return
    for project, hours in sorted(by_project.items(), key=lambda kv: -kv[1]):
        line = f"{project:<20} {hours:>8.2f}h"
        if rate:
            line += f"   ${hours * rate:,.2f}"
        print(line)
    print("-" * 40)
    total_line = f"{'TOTAL':<20} {total_hours:>8.2f}h"
    if rate:
        total_line += f"   ${total_hours * rate:,.2f}"
    print(total_line)


def main():
    p = argparse.ArgumentParser(
        prog="freelance-time",
        description="Track billable hours per project from the command line. No dependencies, no sign-up, no cloud — just a local JSON file.",
    )
    p.add_argument("--file", default=DEFAULT_FILE, help=f"Timesheet file (default: {DEFAULT_FILE} in current directory)")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("start", help="Start tracking time for a project")
    sp.add_argument("project", nargs="?", help="Project or client name (default: 'default')")
    sp.add_argument("--note", help="Optional note for this session")
    sp.set_defaults(func=cmd_start)

    sp = sub.add_parser("stop", help="Stop the currently running timer and log it")
    sp.set_defaults(func=cmd_stop)

    sp = sub.add_parser("status", help="Show the currently running timer, if any")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("add", help="Manually add hours without timing live (e.g. for work you forgot to track)")
    sp.add_argument("hours", type=float, help="Hours to add")
    sp.add_argument("project", nargs="?", help="Project or client name (default: 'default')")
    sp.add_argument("--note", help="Optional note")
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser("report", help="Summarize logged hours, optionally valued at an hourly rate")
    sp.add_argument("--project", help="Only report this project")
    sp.add_argument("--rate", type=float, help="Hourly rate to compute $ owed")
    sp.add_argument("--json", action="store_true", help="Output as JSON")
    sp.set_defaults(func=cmd_report)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
