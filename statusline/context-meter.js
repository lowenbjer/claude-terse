#!/usr/bin/env node
// Status line: model name and context-window fill percentage.
// Reads the status line JSON Claude Code passes on stdin. Uses
// context_window.remaining_percentage, the same field /context reports.
// Percentage only, no bar. Colours: green <37%, yellow <49%, orange <60%, skull and red blinking from 60%.
let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (c) => { raw += c; });
process.stdin.on('end', () => {
  let data = {};
  try { data = JSON.parse(raw); } catch (e) { data = {}; }
  const model = (data.model && (data.model.display_name || data.model.id)) || '';
  const remaining = data.context_window ? data.context_window.remaining_percentage : null;
  let meter = '';
  if (remaining != null && !isNaN(remaining)) {
    // Real fill shown. Colour thresholds sit at 3/4 of the usual 50/65/80,
    // because retrieval quality degrades well before a large window fills.
    const used = Math.max(0, Math.min(100, Math.round(100 - remaining)));
    let colour = '\x1b[32m';
    if (used >= 60) colour = '\x1b[5;31m\u{1F480} ';
    else if (used >= 49) colour = '\x1b[38;5;208m';
    else if (used >= 37) colour = '\x1b[33m';
    meter = colour + used + '%\x1b[0m';
  }
  process.stdout.write([model, meter].filter(Boolean).join('  '));
});
