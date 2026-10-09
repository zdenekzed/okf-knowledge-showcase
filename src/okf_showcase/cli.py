"""okf-showcase command line: one subcommand per step of the flow, `build` runs them all."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from okf_showcase import bundles, dataplex, graph, index, tables
from okf_showcase.settings import load
from okf_showcase.validate import validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="okf-showcase", description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root with okf.yaml")
    sub = parser.add_subparsers(dest="command", required=True)
    tables_cmd = sub.add_parser("tables", help="1. generate table records from the Dataform repository")
    tables_cmd.add_argument("--check", action="store_true", help="fail if committed records are stale")
    index_cmd = sub.add_parser("index", help="1b. generate OKF index.md files for every vault directory")
    index_cmd.add_argument("--check", action="store_true", help="fail if committed indexes are stale")
    sub.add_parser("validate", help="2. validate the whole vault")
    sub.add_parser("bundles", help="3. compile agent context bundles to dist/bundles/")
    sub.add_parser("dataplex", help="4. write the glossary deployment plan to dist/dataplex/")
    sub.add_parser("graph", help="optional: export nodes and edges to dist/graph/")
    sub.add_parser("build", help="run every step: tables, index, validate, bundles, dataplex, graph")
    args = parser.parse_args(argv)
    settings = load(args.root.resolve())

    if args.command in ("tables", "index") and args.check:
        problems = (tables if args.command == "tables" else index).check(settings)
        for problem in problems:
            print(f"STALE {problem}")
        print(f"{args.command}: up to date" if not problems else f"run `okf-showcase {args.command}` and commit")
        return 1 if problems else 0

    steps = (
        ["tables", "index", "validate", "bundles", "dataplex", "graph"] if args.command == "build" else [args.command]
    )
    for step in steps:
        if step == "tables":
            print(f"tables: {len(tables.write(settings))} records written")
        elif step == "index":
            print(f"index: {len(index.write(settings))} index.md files written")
        elif step == "validate":
            issues = validate(settings)
            for issue in issues:
                print(f"ERROR {issue}")
            if issues:
                print(f"validate: {len(issues)} problems")
                return 1
            print("validate: vault is valid")
        elif step == "bundles":
            try:
                paths = bundles.build(settings)
            except bundles.BudgetExceeded as err:
                print(f"ERROR {err}")
                return 1
            print(f"bundles: {len(paths)} compiled to {settings.dist / 'bundles'}")
        elif step == "dataplex":
            path, plan = dataplex.write_plan(settings)
            print(
                f"dataplex: {len(plan['pass_1_terms'])} categories and terms, "
                f"{len(plan['pass_2_links'])} links -> {path} (dry run, nothing sent)"
            )
        elif step == "graph":
            print(f"graph: written to {graph.write(settings)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
