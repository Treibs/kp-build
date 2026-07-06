# Held-out tasks — sui-move falsification

Five contract-authoring tasks. None appears as a pack fixture; none is named in any claim.
Each answer is a single Move module dropped into a scaffold (`Move.toml`, edition 2024) we
provide — only the module body is the model's.

1. **shared-counter** — A shared counter where anyone can increment, but only the creator can
   reset it to zero.
2. **capped-token** — A fungible token "KITS" with a capped total supply enforced at mint time.
3. **soulbound-badge** — A soulbound badge: an object that can never be transferred after mint.
4. **escrow-swap** — An escrow that atomically swaps two objects between two addresses.
5. **guestbook-clock** — A timestamped guestbook entry using on-chain time.

## Protocol

- **base** arm: a fresh agent context receives ONLY the task text ("Write a complete Sui Move
  module for: …"). No pack, no docs, no compiler access, no file/tool access.
- **kp** arm: identical prompt PLUS the pack (`examples/sui-move/CONTEXT.md` + all
  `examples/sui-move/claims/*.md`). Same model, same settings, fresh context per task.
- Both arms: answer is the Move source only; we place it verbatim into
  `answers/{base,kp}/task-N/sources/module.move` with an identical minimal `Move.toml`.
- **Metric:** compile-pass on the pinned toolchain (`sui 1.74.1-8fc60f1fa966`,
  `sui move build`). The compiler does not care what the pack says — this is the
  non-circular axis.
- Model for both arms: claude-sonnet-4-6 (held constant; the pack is the only variable).
