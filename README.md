# supervised-agentic-loop

Self-improving AI agent loop: give it a file and a metric, wake up to a better codebase.

> **Brainstorm → Plan → Implement → Review → Verify → Evolve**

Combines:
- **[autoresearch](https://github.com/karpathy/autoresearch)** — autonomous keep/discard experimentation
- **[governed-agents](https://github.com/senox/governed-agents)** — verification gates + reputation scoring
- **[self-improving-agent](https://github.com/peterskoett/self-improving-agent)** — persistent learnings across sessions

**Zero external dependencies** — only Python 3.11+ stdlib.

## Install

```bash
pip install -e .
```

## Quick Start

```bash
# CLI
sal run --target train.py --metric "python train.py" --parser val_bpb

# Check status
sal status
```

## Python API

```python
from sal.config import EvolveConfig
from sal.evolve_loop import EvolveLoop

config = EvolveConfig(
    target_file="train.py",
    metric_command="python train.py",
    metric_parser="val_bpb",
    minimize=True,
)

loop = EvolveLoop(config, agent=my_agent, agent_id="codex")
summary = loop.run()
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   EvolveLoop                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │Brainstorm│→ │   Plan   │→ │    Implement     │  │
│  │(history) │  │(contract)│  │(agent_callable)  │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
│       ↑                              ↓              │
│  ┌──────────┐                 ┌──────────────────┐  │
│  │  Evolve  │←────────────── │  Review + Verify │  │
│  │keep/disc.│                 │  (gates+metric)  │  │
│  └──────────┘                 └──────────────────┘  │
│       │                                             │
│  ┌────┴─────────────────────────────────────────┐   │
│  │ Subsystems: Git | Reputation | Results | Log │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Safety

- **Git isolation** — every run on its own branch, auto-rollback on failure
- **Reputation scoring** — EMA-based, agents get suspended at ≤ 0.2
- **4 verification gates** — files exist, syntax, tests pass, lint
- **Persistent learnings** — avoid repeating the same failed experiments

## License

MIT
