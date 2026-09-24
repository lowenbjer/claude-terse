---
name: install-meter
description: Add the terse context meter to the Claude Code status line. Use when the user asks to install, enable or show the context meter or percentage in the status line.
---

Add this entry to the user's `~/.claude/settings.json` (create the key if missing, keep every other key as is):

```json
"statusLine": {
  "type": "command",
  "command": "node \"${CLAUDE_PLUGIN_ROOT}/statusline/context-meter.js\""
}
```

Use the absolute path shown above verbatim. Claude Code reloads the status line on save, no restart needed.
Then tell the user: the meter shows model name and context fill percentage. Colours: green below 37%, yellow from 37%, orange from 49%, skull from 60%. The thresholds are below the usual 50, 65 and 80 percent because retrieval quality degrades before a large window fills. Sources are linked in the README, meter section. The thresholds are the three numbers near the top of `context-meter.js`.
