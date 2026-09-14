# Contributing

## Branches

- `main` — always buildable, both languages.
- `feature/<short-description>` — e.g. `feature/order-state-machine`,
  `feature/market-data-websocket`.
- `fix/<short-description>` for bug fixes.

Open a PR into `main` when a feature branch is ready; don't push directly to
`main`.

## Commits

Write commit messages that explain *why*, not just *what* — especially for
anything touching the Python↔C++ contract in `proto/`, since that affects
everyone.

## Building the C++ core

Requires CMake and a C++20-capable compiler. Any editor works (CLion, VS Code
with the CMake Tools extension, Visual Studio) — they all build the same
`CMakeLists.txt`.

```
cd cpp
cmake -B build -S .
cmake --build build
```

## Building the Python side

```
cd python
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -e .
```

## Changing the Python↔C++ contract

Anything in `proto/` is the shared contract between the execution core and
the gateway. If you change a message schema:

1. Update the `.proto` file.
2. Regenerate stubs for both languages.
3. Flag it to the team — a schema change can break the other side silently
   if they're mid-way through building against the old shape.

## Documentation

- Significant design decisions get an ADR in `docs/decisions/` (copy the
  format of an existing one). "Significant" means: would someone reasonably
  ask "why did we do it this way?" in three months.
- Keep `docs/ARCHITECTURE.md` in sync with reality — if the design changes,
  update it in the same PR.
- Public functions/classes in C++ get Doxygen-style comments; Python gets
  docstrings.
