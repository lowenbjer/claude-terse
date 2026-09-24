#!/usr/bin/env node
// Emits a rules file as additionalContext for the hook event named in argv[2].
// argv[3] names the file, relative to the plugin root. Default: rules/RULES.md.
//   node inject-rules.js SubagentStart                        emits rules/RULES.md
//   node inject-rules.js UserPromptSubmit rules/REMINDER.md   emits the reminder
// SubagentStart: the output style reaches the main agent only. Subagents run
// their own system prompt, so this hands them the same rules.
// UserPromptSubmit: the output style sits at the top of the context. After 20
// or 30 turns it is 100k tokens before the prompt and replies stop following
// it. The reminder lands in the current user turn, next to the prompt.
const fs = require('fs');
const path = require('path');
const event = process.argv[2] || 'SubagentStart';
const file = process.argv[3] || path.join('rules', 'RULES.md');
const root = process.env.CLAUDE_PLUGIN_ROOT || path.resolve(__dirname, '..');
let text = '';
try { text = fs.readFileSync(path.resolve(root, file), 'utf8').trim(); } catch (e) { process.exit(0); }
if (!text) process.exit(0);
process.stdout.write(JSON.stringify({
  hookSpecificOutput: { hookEventName: event, additionalContext: text },
}));
