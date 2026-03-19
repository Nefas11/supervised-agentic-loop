"""CLI entrypoint for supervised-agentic-loop.

Usage:
    sal run --target train.py --metric "python train.py" --parser val_bpb
    sal status
    sal unsuspend --agent <id> --reason "verified by human"
"""

import argparse
import logging
import sys

from sal import __version__


def cmd_run(args: argparse.Namespace) -> None:
    """Execute a supervised evolution run."""
    from sal.config import EvolveConfig
    from sal.evolve_loop import EvolveLoop

    # Build config from CLI args
    config = EvolveConfig(
        target_file=args.target,
        metric_command=args.metric,
        metric_parser=args.parser,
        minimize=not args.no_minimize,
        time_budget=args.time_budget,
        max_iterations=args.max_iterations,
        plateau_patience=args.plateau_patience,
        work_dir=args.work_dir,
    )

    # Default agent: echo-back stub (for testing)
    # In production, inject a real agent via the Python API
    def stub_agent(prompt: str) -> str:
        """Stub agent that returns a blocked result."""
        return (
            '```json\n'
            '{"task_id": "stub", "status": "blocked", '
            '"what_failed": "No real agent configured", '
            '"what_i_need": "Set up a real agent via Python API"}\n'
            '```'
        )

    agent_id = args.agent_id or "cli-default"

    loop = EvolveLoop(config=config, agent=stub_agent, agent_id=agent_id)
    summary = loop.run()

    print(f"\n{'='*60}")
    print(f"Run complete: {summary['stop_reason']}")
    print(f"Iterations: {summary['iterations']}")
    print(f"Best metric: {summary['best_metric']}")
    print(f"Reputation: {summary['reputation']}")
    print(f"{'='*60}")


def cmd_status(args: argparse.Namespace) -> None:
    """Show current status: reputation, history, learnings."""
    from sal.learnings import LearningsLog
    from sal.reputation import ReputationDB
    from sal.results_log import ResultsLog

    work_dir = args.work_dir

    # Reputation
    db = ReputationDB(f"{work_dir}/.state/reputation.db")
    agent_id = args.agent_id or "cli-default"
    level = db.get_level(agent_id)
    history = db.get_history(agent_id, limit=5)
    db.close()

    print(f"Agent: {agent_id}")
    print(f"Reputation: {level['reputation']:.4f} ({level['level']})")
    print()

    # Results
    log = ResultsLog(f"{work_dir}/results.tsv")
    best = log.best()
    if best:
        print(f"Best metric: {best['metric_value']:.6f} (iteration {best['iteration']})")
    print(f"Total iterations: {log.count}")
    print()

    # Learnings
    learnings = LearningsLog(f"{work_dir}/.state/learnings")
    print(learnings.get_summary())
    print()

    # Recent history
    if history:
        print("Recent iterations:")
        for h in history:
            print(
                f"  #{h['iteration']:3d}  {h['status']:8s}  "
                f"score={h['score']:+.1f}  rep={h['reputation_after']:.3f}  "
                f"{h['hypothesis'][:50]}"
            )


def cmd_unsuspend(args: argparse.Namespace) -> None:
    """Unsuspend an agent — human-only, with audit trail."""
    from sal.reputation import ReputationDB

    if not args.reason:
        print("ERROR: --reason is required for unsuspend (audit trail)")
        sys.exit(1)

    db = ReputationDB(f"{args.work_dir}/.state/reputation.db")
    result = db.unsuspend(args.agent_id, args.reason)
    db.close()

    print(f"Agent '{result['agent_id']}' unsuspended:")
    print(f"  Reputation: {result['reputation_before']:.4f} → {result['reputation_after']:.4f}")
    print(f"  Reason: {result['reason']}")


def main() -> None:
    """CLI main entrypoint."""
    parser = argparse.ArgumentParser(
        prog="sal",
        description="supervised-agentic-loop — Self-improving AI agent loop",
    )
    parser.add_argument("--version", action="version", version=f"sal {__version__}")
    parser.add_argument(
        "--work-dir", default=".", help="Working directory (default: .)"
    )
    parser.add_argument(
        "--agent-id", default=None, help="Agent identifier"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # sal run
    run_parser = sub.add_parser("run", help="Start an evolution run")
    run_parser.add_argument("--target", required=True, help="File to modify")
    run_parser.add_argument("--metric", required=True, help="Metric command")
    run_parser.add_argument("--parser", required=True, help="Metric parser (named or regex)")
    run_parser.add_argument("--no-minimize", action="store_true", help="Higher is better")
    run_parser.add_argument("--time-budget", type=int, default=300)
    run_parser.add_argument("--max-iterations", type=int, default=100)
    run_parser.add_argument("--plateau-patience", type=int, default=5)

    # sal status
    sub.add_parser("status", help="Show current status")

    # sal unsuspend
    unsuspend_parser = sub.add_parser("unsuspend", help="Unsuspend an agent")
    unsuspend_parser.add_argument("--reason", required=True, help="Audit reason")

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    commands = {
        "run": cmd_run,
        "status": cmd_status,
        "unsuspend": cmd_unsuspend,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
