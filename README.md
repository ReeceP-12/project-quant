# Project Quant

An algorithmic trading system built as a hybrid C++ / Python project: a low-latency
C++ execution core for strategy logic, order management, and risk, paired with a
Python gateway that owns all connectivity to our broker (Alpaca) and a Python
research stack for backtesting and model development.

This README is the front door. Deeper detail lives in [`docs/`](docs/).

## Why hybrid C++/Python

Alpaca only ships official SDKs for Python and JS/TS — there's no official (or
trustworthy unofficial) C++ client. Rather than build fragile broker connectivity
in C++, we split the system along a clean seam: Python owns "the outside world"
(broker auth, REST calls, WebSocket streams, reconnect logic), and C++ owns the
fast, correctness-critical core (strategy decisions, order state machine, position
book, risk checks). See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the
full reasoning and [`docs/decisions/`](docs/decisions/) for the specific calls we
made and why.

## Repo layout

```
project-quant/
├── cpp/                  # execution core (CMake project, C++20)
│   ├── src/
│   ├── include/
│   └── CMakeLists.txt
├── python/
│   ├── gateway/          # owns all Alpaca I/O (alpaca-py)
│   └── research/         # backtesting, feature engineering, ML
├── proto/                # shared message schemas — the C++/Python contract
├── docs/
│   ├── ARCHITECTURE.md
│   └── decisions/        # Architecture Decision Records (ADRs)
└── .github/workflows/    # CI for both languages
```

## Team

- **Lead Architect (Reece):** system design, C++ execution engine, core data
  structures, performance, project integration.
- **Cambridge collaborator:** quantitative research, mathematical modeling,
  strategy design.
- **Manchester collaborator:** data pipelines, feature engineering, ML models.

## Toolchain notes

- **C++ side:** built with CMake (C++20). Use whatever editor you like — CLion,
  VS Code with the CMake Tools extension, or Visual Studio all build the same
  `CMakeLists.txt`. There is no separate "combine it into one IDE" step; CI
  builds both languages on every push.
- **Python side:** standard `pyproject.toml` / virtualenv workflow.
- **Broker:** Alpaca, via the official `alpaca-py` SDK (paper trading during
  development).

## Getting started

_(Fill in once the first build is working: clone steps, dependency install,
how to run the gateway and core together against Alpaca paper trading.)_

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — system design and data flow
- [`docs/decisions/`](docs/decisions/) — why we made the calls we made
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — branch naming, PR flow, how to build
