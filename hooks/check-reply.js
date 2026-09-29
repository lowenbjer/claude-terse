#!/usr/bin/env node
// Stop hook: checks the reply Claude just finished against the checkable rules and asks for one rewrite.
// Reads the Stop hook JSON on stdin. Uses last_assistant_message. Exits 0 silently when the reply passes,
// when the reply is empty, or when this stop already follows a rewrite (stop_hook_active).
// Checks: em and en dashes (rule 5), first person outside quotes and code (rule 19), closing offers (rule 9),
// banned words (rule 12). No length check: the hook cannot see whether a document was asked for.
// TERSE_GATE=off in the environment disables the check.
const fs = require('fs');

function readStdin() {
  try { return fs.readFileSync(0, 'utf8'); } catch (e) { return ''; }
}

// Keep the even-numbered pieces between a delimiter: text outside code fences, inline code or quotes.
function outside(text, delimiter) {
  const parts = text.split(delimiter);
  const kept = [];
  for (let i = 0; i < parts.length; i += 2) kept.push(parts[i]);
  return kept.join(' ');
}

function splitWords(text) {
  const words = [];
  let cur = '';
  for (const ch of text) {
    if (ch === ' ' || ch === '\n' || ch === '\t' || ch === '\r') {
      if (cur) words.push(cur);
      cur = '';
    } else {
      cur += ch;
    }
  }
  if (cur) words.push(cur);
  return words;
}

const PUNCT = '.,;:!?()[]{}\'*_‘’|>#-';
function trimPunct(word) {
  let s = word.split('’').join("'");
  while (s && PUNCT.includes(s[0])) s = s.slice(1);
  while (s && PUNCT.includes(s[s.length - 1])) s = s.slice(0, -1);
  return s;
}

function isCapitalised(word) {
  const c = word[0] || '';
  return c !== c.toLowerCase() && c === c.toUpperCase();
}

// "I" counts only in upper case, so Swedish "i" (in) does not. "my" followed by a capitalised word is a product name.
const FIRST_PERSON = ["i'd", "i'm", "i've", "i'll", 'me', 'my', 'mine', 'myself'];
function firstPerson(words) {
  const hits = [];
  for (let i = 0; i < words.length; i++) {
    const w = trimPunct(words[i]);
    if (!w) continue;
    if (w === 'I') { hits.push(w); continue; }
    const low = w.toLowerCase();
    if (!FIRST_PERSON.includes(low)) continue;
    const next = trimPunct(words[i + 1] || '');
    if (low === 'my' && next && isCapitalised(next)) continue;
    hits.push(w);
  }
  return hits;
}

const CLOSERS = ['let me know', 'feel free', 'happy to', 'hope this helps', 'in summary', 'to summarize', 'to recap',
  'want me to', 'shall i', 'would you like me', "if you'd like", 'if you would like', 'just say', 'if useful'];
const BANNED = ['significant', 'robust', 'comprehensive', 'leverage', 'precisely', 'buildable', 'to be honest', 'honestly', 'let me be direct'];

function unique(list) { return list.filter((x, i) => list.indexOf(x) === i); }

function problems(text) {
  const found = [];
  const dashes = text.split('—').length - 1 + text.split('–').length - 1;
  if (dashes) found.push(dashes + (dashes === 1 ? ' em or en dash' : ' em or en dashes') + ' (rule 5)');
  let body = outside(text, '```');
  body = outside(body, '`');
  body = outside(body.split('“').join('"').split('”').join('"'), '"');
  const fp = firstPerson(splitWords(body));
  if (fp.length) found.push(fp.length + (fp.length === 1 ? ' first-person word (' : ' first-person words (') + unique(fp).slice(0, 5).join(', ') + ') (rule 19)');
  const low = body.toLowerCase();
  const closers = CLOSERS.filter((c) => low.includes(c));
  if (closers.length) found.push('closing offer (' + closers.join(', ') + ') (rule 9)');
  const banned = BANNED.filter((b) => low.includes(b));
  if (banned.length) found.push('banned word (' + banned.join(', ') + ') (rule 12)');
  return found;
}

function main() {
  if (process.env.TERSE_GATE === 'off') return;
  let input = {};
  try { input = JSON.parse(readStdin()); } catch (e) { return; }
  if (input.stop_hook_active) return;
  const text = String(input.last_assistant_message || '');
  if (!text.trim()) return;
  const found = problems(text);
  if (!found.length) return;
  const reason = 'terse: rewrite the previous reply and send only the rewrite. Violations: ' + found.join('; ') +
    '. Every sentence has the topic as its subject. Your own next step is an instruction ("Next: run the suite, paste the count."). Same facts, fewer words. Do not mention this check.';
  process.stdout.write(JSON.stringify({ decision: 'block', reason: reason }));
}

if (require.main === module) main();
module.exports = { problems, firstPerson, splitWords };
