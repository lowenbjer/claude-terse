# Privacy

terse runs on your machine and sends nothing anywhere.

- The plugin makes no network calls. Its two hooks run a 21-line Node script that reads a text file inside the plugin directory and prints it for Claude Code to add to the prompt.
- The plugin collects no data, writes no logs and stores nothing about you or your sessions.
- The context meter reads the status line JSON that Claude Code passes it on standard input and prints one line. Nothing is kept.
- The install skill, which only you can run, copies the meter script to the plugin's data directory and writes one `statusLine` entry to your `~/.claude/settings.json`. It touches no other key.
- Your prompts and Claude's replies go to Anthropic through Claude Code as they do without the plugin. The plugin adds its rule text to that request and nothing else.

Questions go to the [issue tracker](https://github.com/lowenbjer/claude-terse/issues).
