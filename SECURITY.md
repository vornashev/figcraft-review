# Security

Please report vulnerabilities privately through [GitHub's private vulnerability reporting](https://github.com/vornashev/figcraft-review/security/advisories/new), not in a public issue. You'll get an answer within a week.

What to know about the design:

- The chat's server listens on `127.0.0.1` only. It refuses requests with a foreign `Host` (DNS rebinding) and POSTs from a foreign `Origin`. The agents' MCP bridge also needs a per-run token.
- Agents run as your user, through their own CLIs and logins. In the **Только FigCraft** access mode they can edit the design and read project files, but can't run commands or write files. **Как в терминале** gives them their usual permissions.
- Design skills are prompts that go to the agent. Only install skills from sources you trust, as with any agent instructions.
