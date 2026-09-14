# Architecture

_Last updated: 2026-09-14. This document is the living source of truth for the
system design — update it whenever a design decision changes, and add an ADR
in `docs/decisions/` for any decision significant enough to need a "why."_

## Goals

- A low-latency C++ execution core for strategy logic, order management, and
  risk checks.
- A Python layer that owns all Alpaca broker connectivity (REST + WebSocket)
  and a separate Python research stack for backtesting and ML model
  development.
- A clean, typed contract between the two languages so multiple people can
  build against the interface without needing to read each other's internals.

## Why not talk to Alpaca from C++ directly

Alpaca officially maintains SDKs for Python (`alpaca-py`) and JS/TS. There is
no official C++ SDK, and the community C++ wrapper that exists is a small,
largely unmaintained side project — not something to build production order
flow on.

Reimplementing Alpaca's auth, rate limiting, and WebSocket reconnect/backoff
logic in C++ would be pure risk for no latency benefit: the system is still
bound by Alpaca's own network round-trip and WebSocket cadence, which is far
above where C++-level latency gains would matter. So Python owns the broker
relationship entirely, and C++ talks to a service we control instead.

See [`docs/decisions/0001-no-cpp-alpaca-sdk.md`](decisions/0001-no-cpp-alpaca-sdk.md).

## System overview

```
        Alpaca (REST + WebSocket)
              ↕  alpaca-py
   ┌─────────────────────────────┐
   │   Python Broker Gateway      │   owns ALL Alpaca I/O
   │  (auth, orders, streams,     │   (auth, retries, reconnects)
   │   reconnect/backoff logic)   │
   └─────────────────────────────┘
              ↕  internal IPC (gRPC + ZeroMQ — see below)
   ┌─────────────────────────────┐
   │      C++ Execution Core      │   strategy, OMS, risk, positions
   └─────────────────────────────┘
              ↕
   ┌─────────────────────────────┐
   │  Python Research / ML        │   offline: backtesting, feature eng,
   │  (reads logged data, not     │   model training
   │   in the live path)          │
   └─────────────────────────────┘
```

## Components

### Python Broker Gateway (`python/gateway/`)

Owns everything Alpaca-facing:

- Authentication and account/session management via `alpaca-py`.
- REST calls: order submission, cancellation, position/account queries.
- WebSocket streams: market data (trades/quotes/bars) and trade updates
  (fills, acks, rejects), including reconnect/backoff handling.
- Normalizes Alpaca's message formats into our own internal schema (defined
  in `proto/`) before anything crosses into the C++ side.

### C++ Execution Core (`cpp/`)

Owns the fast, correctness-critical logic:

- Strategy decision logic (consumes market data, produces order intents).
- Order management (state machine: pending → submitted → filled/rejected/
  cancelled).
- Position book and risk checks.
- Never talks to Alpaca directly — only to the Python gateway, over the
  internal contract.

### Python Research / ML (`python/research/`)

Offline only — not in the live trading path:

- Backtesting against historical data.
- Feature engineering and model training.
- Should consume the *same* event schema (from `proto/`) that the live
  system uses, so a strategy tested offline behaves the same way live.

## Data planes between Python and C++

Two logical planes cross the Python↔C++ boundary, and they don't have to
use the same transport:

1. **Market data plane** (gateway → core): ticks/quotes/bars, high frequency,
   fan-out to potentially multiple consumers. Recommended: **ZeroMQ PUB/SUB**
   — lightweight, no broker process required, low latency, mature bindings
   in both languages.
2. **Order/control plane** (core → gateway → core): order intents out, fills/
   acks/rejects back. Lower frequency, but correctness-critical — you want
   strict typing and a clear versioned schema. Recommended: **gRPC +
   Protobuf** — the `.proto` files in `proto/` are the single source of
   truth, and both languages generate typed stubs from them, so the C++ and
   Python sides can never silently drift out of sync on field names/types.

See [`docs/decisions/0002-grpc-zeromq-ipc.md`](decisions/0002-grpc-zeromq-ipc.md)
for the reasoning and the alternatives considered (shared memory, Redis/NATS,
gRPC-only).

## Explicitly out of scope for now

- Shared-memory ring buffers for the hot path — only worth the complexity
  once we've measured ZeroMQ/gRPC latency as an actual bottleneck, which at
  this stage of the project it isn't.
- Multi-broker support — Alpaca only, for now.
