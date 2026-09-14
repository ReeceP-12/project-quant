# ADR 0002: gRPC for the order plane, ZeroMQ for the market data plane

**Status:** Accepted
**Date:** 2026-09-14

## Context

Given ADR 0001, the C++ execution core and Python broker gateway are separate
processes that need a fast, reliable internal transport. Two distinct kinds
of traffic cross this boundary: high-frequency market data (gateway → core)
and lower-frequency, correctness-critical order/fill events (core ↔ gateway).

## Options considered

- **ZeroMQ** (PUB/SUB, DEALER/ROUTER, etc.) — lightweight, no broker process,
  low latency, mature Python and C++ bindings, common in real trading
  systems. Messages are just bytes, so schema discipline is on us.
- **gRPC + Protobuf** — schema-first: `.proto` files generate typed stubs in
  both languages, so field names/types can't silently drift between the two
  codebases. Slightly more overhead than raw ZeroMQ, and less natural for
  high-frequency fan-out.
- **Redis pub/sub or a message queue (NATS, Kafka)** — easy to stand up,
  gives durability/replay, but adds an external broker dependency and more
  latency. Better suited to logging/replay than the hot path.
- **Shared memory ring buffer** — lowest possible latency, but real
  complexity (lock-free structures, memory layout, lifecycle management).
  Only worth it once we've measured that ZeroMQ/gRPC is actually the
  bottleneck.

## Decision

Use both, for different planes:

- **Market data plane (gateway → core):** ZeroMQ PUB/SUB. High frequency,
  fan-out shaped, latency-sensitive, doesn't need strict per-message typing
  beyond what we define ourselves in `proto/` (used here just as a shared
  schema reference, not necessarily gRPC-transported).
- **Order/control plane (core → gateway → core):** gRPC + Protobuf. Lower
  frequency, but this is where correctness matters most — an order intent
  or a fill event with a mismatched field is a real-money bug, not a
  cosmetic one. Typed, generated stubs make that class of bug much harder
  to introduce.

## Consequences

- Two transport libraries to depend on instead of one — acceptable given
  they're solving genuinely different problems.
- `proto/` becomes the single source of truth for message shapes across
  both planes, even where ZeroMQ is the transport, so schemas stay
  consistent and documented in one place.
- Revisit if profiling ever shows the order plane's gRPC overhead actually
  matters, or if the market data plane needs stronger delivery guarantees
  than ZeroMQ PUB/SUB provides.
