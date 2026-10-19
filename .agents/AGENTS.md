# Git Commit Instructions

At the end of EVERY response, you MUST:

1. Always provide the complete set of commands: `git add .`, `git commit`, and `git push`.
2. Ensure the commit message is **concise, precise, and single-line**:
   - Format: `git commit -m "<type>(<scope>): <concise action-oriented summary>"`
   - Must look authentic and human-written by the developer, NEVER robotic or generic.
   - High-signal and recruiter-friendly: immediately communicates exact technical work done.
   - Avoid buzzwords, corporate fluff, or multi-line paragraphs.
3. Ensure the commands are formatted inside a single standard fenced markdown code block with the `bash` language tag (e.g. ````bash ... ````).
4. The code block must be directly executable and terminal-clickable so that the IDE displays the terminal insertion button (`>_`), allowing the user to click and paste/run it directly into their terminal.

Example format:

```bash
git add .
git commit -m "feat(database): configure engine, sessionmaker, and session dependency"
git push
```
