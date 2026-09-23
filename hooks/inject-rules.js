#!/usr/bin/env node
// Emits rules/RULES.md as additionalContext for the hook event named in argv[2].
// Used for SubagentStart: the output style reaches the main agent only, and
// subagents run their own system prompt. This gives them the same rules.
const fs = require('fs');
const path = require('path');
const event = process.argv[2] || 'SubagentStart';
const root = process.env.CLAUDE_PLUGIN_ROOT || path.resolve(__dirname, '..');
let rules = '';
try { rules = fs.readFileSync(path.join(root, 'rules', 'RULES.md'), 'utf8'); } catch (e) { process.exit(0); }
process.stdout.write(JSON.stringify({
  hookSpecificOutput: { hookEventName: event, additionalContext: rules },
}));
