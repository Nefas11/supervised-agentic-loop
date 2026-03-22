# supervised-agentic-loop — Claude Code Context

When working in this repo, read these files to understand the system:

## Core Files

- `sal/evolve_loop.py` — 6-phase loop orchestrator (Brainstorm → Evolve)
- `sal/config.py` — `EvolveConfig` dataclass, all run parameters
- `sal/contract.py` — `AgentCallable` protocol, `TaskContract`, `TaskResult`
- `sal/reputation.py` — EMA scoring, suspension logic
- `sal/verification.py` — 4 verification gates (files, syntax, tests, lint)
- `sal/git_isolation.py` — branch-per-run, auto-rollback
- `sal/learnings.py` — persistent pattern detection
- `sal/brainstorm.py` — hypothesis generation from history
- `sal/cli.py` — CLI entrypoint (`sal run`, `sal status`, `sal monitor ...`)

## Monitor (Safety Layer)

- `sal/monitor/monitor.py` — two-phase detection engine
- `sal/monitor/behaviors.py` — 10 misalignment behaviors (B001–B010)
- `sal/monitor/sanitizer.py` — credential redaction (10 regex patterns)
- `sal/monitor/heartbeat.py` — self-monitoring + canary checks
- `sal/monitor/alerter.py` — Telegram alerts (optional)

## Key Rules

- `sal/` imports `monitor/`, NEVER the reverse
- Agent modifies exactly ONE file per iteration (`target_file`)
- All changes are git-isolated with automatic rollback
- Monitor is optional — disable with `enable_monitor=False`
- Zero external dependencies — Python 3.11+ stdlib only

## Tests

```bash
pytest tests/ -v
# 130 tests (69 SAL + 61 Monitor)
```
