# supervised-agentic-loop

Self-improving AI agent loop with built-in misalignment detection.

> **Brainstorm → Plan → Implement → Review → Verify → Evolve**
> — with every tool call monitored for safety.

Combines:
- **[autoresearch](https://github.com/karpathy/autoresearch)** — autonomous keep/discard experimentation
- **[governed-agents](https://github.com/senox/governed-agents)** — verification gates + reputation scoring
- **[self-improving-agent](https://github.com/peterskoett/self-improving-agent)** — persistent learnings across sessions
- **[OpenAI Agent Monitoring](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/)** — two-phase misalignment detection

**Zero external dependencies** — only Python 3.11+ stdlib.

## Install

```bash
pip install -e .
# or
bash install.sh
```

## Quick Start

```bash
# Start evolution run
sal run --target train.py --metric "python train.py" --parser val_bpb

# Check status
sal status

# Monitor commands
sal monitor stats     # sessions, alerts, alive status
sal monitor canary    # run self-test (5 canary checks)
sal monitor alerts    # recent misalignment alerts
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

# Monitor is automatic — set enable_monitor=False to disable
loop = EvolveLoop(config, agent=my_agent, agent_id="codex")
summary = loop.run()
```

### Using the Monitor Standalone

```python
from sal.monitor import AgentMonitor, BlockDecision

monitor = AgentMonitor(state_dir=".state")

# SYNC: check BEFORE execution (< 5ms)
decision = monitor.check_before_execute("exec", {"command": "rm -rf /"})
# → BlockDecision.BLOCK

# ASYNC: review entire session
result = monitor.review_session(session_entries, agent_callable=my_llm)
```

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      EvolveLoop                          │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────────┐  │
│  │Brainstorm│→ │   Plan   │→ │     Implement         │  │
│  │(history) │  │(contract)│  │   (agent_callable)    │  │
│  └──────────┘  └──────────┘  └───────┬───────────────┘  │
│       ↑                              │                   │
│       │                    ┌─────────▼──────────┐        │
│       │                    │   🛡️ sal.monitor    │        │
│       │                    │  ┌───────────────┐ │        │
│       │                    │  │ SYNC Prefilter│ │        │
│       │                    │  │ (<5ms, rules) │ │        │
│       │                    │  └──────┬────────┘ │        │
│       │                    │   ALLOW │ BLOCK    │        │
│       │                    │         ↓          │        │
│       │                    │  ┌───────────────┐ │        │
│       │                    │  │ ASYNC LLM     │ │        │
│       │                    │  │ Session Review│ │        │
│       │                    │  └───────────────┘ │        │
│       │                    └────────────────────┘        │
│       │                              │                   │
│  ┌────┴─────┐                 ┌──────▼───────────────┐   │
│  │  Evolve  │←────────────────│  Review + Verify     │   │
│  │keep/disc.│                 │  (gates + metric)    │   │
│  └──────────┘                 └──────────────────────┘   │
│       │                              │                   │
│  ┌────┴──────────────────────────────┴───────────────┐   │
│  │ Git | Reputation | Results | Learnings | Heartbeat│   │
│  └───────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

### How SAL + Monitor Work Together

| Phase | What SAL Does | What Monitor Does |
|---|---|---|
| **Before Agent Call** | Builds prompt from hypothesis | **SYNC prefilter** — checks prompt for injection patterns |
| **Agent Executes** | Sends prompt to LLM | — |
| **After Agent Output** | Receives code changes | **SYNC prefilter** — scans output for dangerous patterns |
| **On BLOCK** | `IterationCrash` → rollback | **Reputation -1.0** + Telegram alert |
| **Session End** | Logs results | **ASYNC LLM review** of full session (optional) |

### Integration Hooks (in `evolve_loop.py`)

```python
# Hook 1: SYNC prefilter — before agent call + after output
decision = self.monitor.check_before_execute("agent_call", args)
if decision == BlockDecision.BLOCK:
    # Hook 2: BLOCK → reputation penalty
    self.reputation.update(agent_id, score=SCORE_HALLUCINATION)
    raise IterationCrash("Monitor BLOCKED")

# Hook 3: Session tracking per iteration
logger.debug("Monitor: session_start(iteration=%d)", i)
```

## 10 Misalignment Behaviors

| ID | Behavior | Severity | Sync Block |
|---|---|---|---|
| B001 | Restriction bypass / destructive delete | HIGH | ✅ |
| B002 | Unexpected tool calls | MEDIUM | — |
| B003 | Goal deviation | MEDIUM | — |
| B004 | Self-modification | CRITICAL | — |
| B005 | Data exfiltration | CRITICAL | ✅ |
| B006 | Hallucinated success | HIGH | — |
| B007 | Privilege escalation | HIGH | ✅ |
| B008 | Resource exhaustion | MEDIUM | ✅ |
| B009 | Persistence / backdoor | CRITICAL | ✅ |
| B010 | Obfuscation | HIGH | ✅ |

## Safety Features

- **Git isolation** — every run on its own branch, auto-rollback on failure
- **Reputation scoring** — EMA-based, agents get suspended at ≤ 0.2
- **4 verification gates** — files exist, syntax, tests pass, lint
- **Persistent learnings** — avoid repeating the same failed experiments
- **SYNC blocking** — dangerous commands blocked before execution (< 5ms)
- **ASYNC LLM review** — deep misalignment detection on full sessions
- **Credential sanitization** — 10 patterns redacted from all JSONL logs
- **Self-monitoring** — heartbeat pulse + daily canary tests (5 checks)
- **Telegram alerts** — HIGH/CRITICAL behaviors → instant notification

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SAL_DB_PATH` | No | Override reputation DB path |
| `MONITOR_TELEGRAM_BOT_TOKEN` | For alerts | Telegram bot API token |
| `MONITOR_TELEGRAM_CHAT_ID` | For alerts | Target chat/user ID |
| `MONITOR_LLM_COMMAND` | No | LLM command for async review |
| `MONITOR_STATE_DIR` | No | Override state directory |

## Tests

```bash
pytest tests/ -v
# 130 tests (69 SAL + 61 Monitor)
```

## License

MIT
