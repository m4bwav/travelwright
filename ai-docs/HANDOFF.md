# HANDOFF: travelwright

State 2026-11-20: v0.4.0 released (real-Gmail parser fixes: stacked airline legs, hotel mail with a car-rental ad, date-range stays, split addresses, 11-digit phones) and installed as travelwright@mark-local. Wiki live at https://github.com/m4bwav/travelwright/wiki, updated for 0.4.0. Repo is PUBLIC: run the leak test before every push.

- Public repo history restarts at one root commit (e6d6eaa). The old private history lives in PRIVATE m4bwav/travelwright-private-archive; never make it public or push to it. Local clone has it as remote `archive`.
- Gate tests on exit code and last line OK; never pipe into tail/head before a commit. Leak list includes common medicine names: say 'ADHD stimulants' in public files.
- Real trip data (raw Gmail output, trip.json, packing plan) lives only under ~/.travelwright/trips/; regression fixtures in the repo are synthetic.
- Next, in order: (1) render prints the "Abroad" passport and controlled-medicine lines on domestic trips: show them only when a leg leaves the US; (2) more real layouts as they arrive (rides, rental cars: none in the first real run).
- Waits on Mark: nothing.
- Continue prompt: [plugin-backlog/ai-docs/plans/2026-11-20-travelwright-continue-prompt.md](../../plugin-backlog/ai-docs/plans/2026-11-20-travelwright-continue-prompt.md)
