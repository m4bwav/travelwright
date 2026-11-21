# GitHub wiki (2026-11-20, travelwright 0.2.0)

- Pages: Home, Getting-Started, Commands, Privacy, FAQ, _Sidebar, _Footer. Working copy: D:/m4bwa/Claude/Projects/Ai/travelwright.wiki (git init, branch master, remote set).
- Published: NOT YET. The wiki repo did not exist and Chrome was not connected, so the first page must be saved by hand at https://github.com/m4bwav/travelwright/wiki/_new. Then: `git -C ../travelwright.wiki push --force-with-lease origin master` (init'd copy, L-010) and `wikiwright.py live m4bwav/travelwright ../travelwright.wiki`.
- Verified: Commands outputs came from running tw.py on skills/travelwright/evals/fixtures; saved in 2026-11-20-wiki-verify.out.txt (commands are in Commands.md). `check` 0 errors, `outputs` 3/3, tells 0 strong.
- Update at a release: rerun the three commands, diff the output, update _Footer version and Commands' "since" notes.
- Not tested: the plain-skill route on Copilot/Codex/Cursor.
