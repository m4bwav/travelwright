# AGENTS.md: travelwright

Claude Code plugin (one skill) that plans family trips from bookings in email, Drive and family-tree pages.

- Layout: `.claude-plugin/plugin.json`; `skills/travelwright/` (SKILL.md, references/trip-schema.md, scripts/tw.py, evals/ with fixtures, evergreen files); `tests/`.
- Before committing: `python -m unittest discover -s tests` with `TRAVELWRIGHT_HOME` set to the private home, so the leak test runs with the full term list (it skips when the variable is unset).
- Private repo. Even so, family names, medicines, addresses, bookings and confirmation codes never go in a tracked file, ai-docs/ included; they live in the user's trips folder and `TRAVELWRIGHT_HOME`. Fixtures use made-up people and places.
- State and handoff: [ai-docs/HANDOFF.md](ai-docs/HANDOFF.md), log [ai-docs/log.md](ai-docs/log.md).
