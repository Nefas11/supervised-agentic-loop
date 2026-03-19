---
name: supervised-agentic-loop
description: >
  Self-improving experiment loop: give an AI agent a target file and a metric,
  and it autonomously runs Brainstorm → Plan → Implement → Review → Verify → Evolve
  cycles — keeping improvements, discarding regressions, and learning persistently.
  Combines autoresearch-style keep/discard experimentation with governed-agents
  verification gates and reputation scoring.
install: pip install -e .
source: https://github.com/senox/supervised-agentic-loop
homepage: https://github.com/senox/supervised-agentic-loop
filesystem_writes: true
network_access:
  - host: "none"
    reason: "All operations are local. No network access required."
capabilities:
  - autonomous-experimentation
  - verification-gates
  - reputation-scoring
  - persistent-learnings
  - git-isolation
env_vars:
  SAL_DB_PATH: "Optional. Override reputation DB path."
---

# supervised-agentic-loop

## Quick Reference

| What | Details |
|---|---|
| **Loop** | Brainstorm → Plan → Implement → Review → Verify → Evolve |
| **Agent modifies** | One file only (`target_file`) |
| **Metric** | Any command that produces a numeric output |
| **Safety** | Git branch isolation + automatic rollback on failure |
| **Persistence** | `results.tsv` + `.state/learnings/` + `reputation.db` |

## How to Use

### As a Skill (in your agent instructions)

```markdown
Read the SKILL.md in supervised-agentic-loop/ and begin an experiment run.
Target file: train.py
Metric: python train.py (look for val_bpb, lower is better)
```

### As a CLI

```bash
sal run --target train.py --metric "python train.py" --parser val_bpb
sal status
sal unsuspend --agent codex --reason "verified by human"
```

### As a Python API

```python
from sal.config import EvolveConfig
from sal.evolve_loop import EvolveLoop

config = EvolveConfig(
    target_file="train.py",
    metric_command="python train.py",
    metric_parser="val_bpb",
    minimize=True,
)

def my_agent(prompt: str) -> str:
    # Your LLM call here — must return output with JSON block
    ...

loop = EvolveLoop(config, agent=my_agent, agent_id="my-model")
summary = loop.run()
```

## Phases

1. **Baseline** — Run metric on unmodified code (fails → HARD ABORT)
2. **Brainstorm** — Generate hypothesis from history + learnings
3. **Plan** — Create TaskContract with acceptance criteria
4. **Implement** — Agent modifies `target_file`
5. **Review** — Parse agent output for contract compliance
6. **Verify** — Run verification gates (files, syntax, tests, lint) + extract metric
7. **Evolve** — Compare metric → KEEP (commit) or DISCARD (rollback)

## Auto-Brake Conditions

The loop stops automatically when:
- **Reputation ≤ 0.2** → Agent suspended
- **Plateau** → No improvement for N iterations
- **Budget** → max_iterations reached
- **SIGINT** → Human interrupt (graceful)

## Built-in Metric Parsers

| Name | Extracts |
|---|---|
| `last_line_float` | Float from last line of output |
| `pytest_passed` | Number of passed tests |
| `pytest_failed` | Number of failed tests |
| `coverage_percent` | Coverage percentage |
| `val_bpb` | Validation BPB value |
| `benchmark_ms` | Milliseconds from benchmark output |
| Custom regex | Any regex with 1 capture group |

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SAL_DB_PATH` | `.state/reputation.db` | Reputation database path |

## Constraints

- Zero external dependencies (Python 3.11+ stdlib only)
- Agent modifies exactly ONE file per iteration
- All changes are git-isolated with automatic rollback
- Learnings persist across runs in `.state/learnings/`
