// Run: node hooks/check-reply.test.js
const assert = require('assert');
const { problems } = require('./check-reply.js');

const cases = [
  ['I would look at pg_stat_activity first \u2014 my guess is locks. "my pipeline" is quoted. Let me know if useful. `my var`',
    ['1 em or en dash (rule 5)', '3 first-person words (I, my, me) (rule 19)', 'closing offer (let me know, if useful) (rule 9)']],
  ['Rubriken blir Integrationer och AI i din produkt. Vi bygger det i tre steg.', []],
  ['| location | her My Drive | shared drive |\nHer folder was in My Drive.', []],
  ['Next: run the suite, paste the count. Delete the 22 docs?', []],
  ['Say so and I\u2019ll flip it next time.', ['1 first-person word (I\'ll) (rule 19)']],
  ['```\nI = 1\n```\nDone.', []],
  ['The design is robust and comprehensive.', ['banned word (robust, comprehensive) (rule 12)']],
  ['Ranges run 10\u201315 seconds.', ['1 em or en dash (rule 5)']],
  ['', []],
];
for (const [text, expected] of cases) assert.deepStrictEqual(problems(text), expected, text);
console.log(cases.length + ' cases pass');
