# ADR 0001: No direct C++ connection to Alpaca

**Status:** Accepted
**Date:** 2026-09-14

## Context

The execution core is written in modern C++ for performance and correctness.
Our broker is Alpaca. Alpaca officially maintains SDKs for Python (`alpaca-py`)
and JS/TS only — no official C++ SDK exists. A community C++ client
(`marpaia/alpaca-trade-api-cpp`) exists but is small and largely unmaintained.

## Decision

The C++ execution core will never talk to Alpaca directly. All broker I/O
(authentication, REST order calls, WebSocket market data and trade-update
streams, reconnect/backoff handling) is owned exclusively by a Python
service (`python/gateway/`) built on `alpaca-py`. The C++ core communicates
only with this gateway, over an internal contract we control (see ADR 0002).

## Rationale

- Reimplementing Alpaca's auth, rate limiting, and reconnect logic in C++
  (or depending on an unmaintained wrapper) is pure risk with no upside.
- The system's latency floor is set by Alpaca's own network round-trip and
  WebSocket cadence, not by which language talks to Alpaca. Cutting Python
  out of that leg would not meaningfully reduce latency.
- This gives a clean separation of concerns: Python owns "the outside
  world," C++ owns the fast, correctness-critical core.

## Consequences

- The Python gateway becomes a single point of failure for connectivity —
  it needs its own reconnect/health-check logic and should be built to fail
  loudly and recover cleanly.
- The internal Python↔C++ contract (message schemas, transport) becomes a
  first-class piece of the system that needs versioning discipline, since
  it's now the actual API boundary between "broker world" and "execution
  world."
