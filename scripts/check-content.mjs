// Validates every content/gradeG/setN.json against the set format the app renders.
// Usage: node scripts/check-content.mjs [grade ...]   (no args = every grade)
// Exits 1 if any set has an error.
import fs from 'fs';
import path from 'path';

const ROOT = path.join(path.dirname(new URL(import.meta.url).pathname), '..', 'content');
const STORY_WORDS = { 1: [110, 165], 2: [140, 205], 3: [200, 270], 4: [200, 270], 5: [210, 275], 6: [220, 290], 7: [230, 300], 8: [240, 320] };
// Reference products we study must never reach students (sources field included).
const BANNED = /sadlier|wordly\s*wise|flocabulary|vocabulary\s*workshop|membean|\bixl\b|testing\s*mom|scholastic|mcgraw|wit\s*&\s*wisdom|\bckla\b/i;
const NEW_GRADES = new Set([1, 2, 6, 7, 8]);

const grades = process.argv.slice(2).map(Number).filter(Boolean);
const dirs = fs.readdirSync(ROOT).filter((d) => /^grade\d+$/.test(d)).filter((d) => !grades.length || grades.includes(Number(d.slice(5))));
let errors = 0, sets = 0;
const seenWords = new Map();

for (const dir of dirs) {
  const grade = Number(dir.slice(5));
  for (const file of fs.readdirSync(path.join(ROOT, dir)).filter((f) => /^set\d+\.json$/.test(f))) {
    sets++;
    const where = `${dir}/${file}`;
    const bad = (msg) => { errors++; console.log(`✗ ${where}: ${msg}`); };
    let d;
    try { d = JSON.parse(fs.readFileSync(path.join(ROOT, dir, file), 'utf8')); } catch (e) { bad('invalid JSON: ' + e.message); continue; }
    const W = d.words || [];
    if (d.grade !== grade) bad(`grade ${d.grade} ≠ folder ${grade}`);
    if (d.setNumber !== Number(file.match(/\d+/)[0])) bad('setNumber does not match file name');
    if (W.length !== 12 || new Set(W).size !== 12) bad('need 12 distinct words');
    for (const w of W) {
      if (w !== w.toLowerCase()) bad(`word not lowercase: ${w}`);
      if (seenWords.has(w)) bad(`"${w}" also in ${seenWords.get(w)}`); else seenWords.set(w, where);
    }
    // story
    const parts = (d.story && d.story.parts) || [];
    if (parts.length !== 4) bad('story needs 4 parts');
    const allText = parts.map((p) => p.text || '').join(' ');
    for (const w of W) {
      const n = (allText.match(new RegExp('\\*\\*' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\*\\*', 'gi')) || []).length;
      if (n !== 1) bad(`story bolds "${w}" ${n} times (need exactly 1)`);
    }
    if (parts[3] && /\*\*/.test(parts[3].text || '')) bad('story part 4 must have no bolded words');
    const wc = allText.replace(/\*\*/g, '').split(/\s+/).filter(Boolean).length;
    const [lo, hi] = STORY_WORDS[grade] || [100, 400];
    if (NEW_GRADES.has(grade) && (wc < lo || wc > hi)) bad(`story is ${wc} words (want ${lo}-${hi} for grade ${grade})`);
    // definitions
    const defs = d.definitions || [];
    if (defs.length !== 12) bad('need 12 definitions');
    defs.forEach((x, i) => {
      if (x.word !== W[i]) bad(`definition ${i + 1} is "${x.word}", expected "${W[i]}"`);
      if (!x.meaning1 || !/Example:/.test(x.meaning1)) bad(`definition "${x.word}": meaning1 needs "Example:"`);
      if (!/___/.test(x.studentChallenge || '')) bad(`definition "${x.word}": studentChallenge needs ___`);
      if (new RegExp('\\b' + x.word + '\\b', 'i').test(x.studentChallenge || '')) bad(`definition "${x.word}": studentChallenge gives away the word`);
    });
    // double-take quiz
    const q = d.doubleTakeQuiz || [];
    if (q.length !== 12) bad('need 12 doubleTakeQuiz questions');
    const keys = q.map((x) => x.correctAnswer);
    for (const w of W) if (keys.filter((k) => k === w).length !== 1) bad(`doubleTakeQuiz: "${w}" must be the answer exactly once`);
    q.forEach((x, i) => {
      if (!Array.isArray(x.options) || x.options.length !== 4 || new Set(x.options).size !== 4) bad(`doubleTake ${i + 1}: need 4 distinct options`);
      else if (x.options[x.correctIndex] !== x.correctAnswer) bad(`doubleTake ${i + 1}: correctIndex does not point at correctAnswer`);
      if ((x.options || []).some((o) => !W.includes(o))) bad(`doubleTake ${i + 1}: an option is not in the set`);
      for (const s of [x.sentence1, x.sentence2]) {
        if (!/_{3,}/.test(s || '')) bad(`doubleTake ${i + 1}: sentence missing blank`);
        if (new RegExp('\\b' + x.correctAnswer + '\\b', 'i').test(s || '')) bad(`doubleTake ${i + 1}: sentence contains the answer`);
      }
    });
    // secret passage
    const sp = d.secretPassage || {};
    if (JSON.stringify(sp.wordBank) !== JSON.stringify(W)) bad('secretPassage wordBank must equal words in order');
    for (let n = 1; n <= 12; n++) if (((sp.passage || '').match(new RegExp('_\\(' + n + '\\)_', 'g')) || []).length !== 1) bad(`secretPassage: blank _(${n})_ must appear once`);
    const bl = sp.blanks || [];
    if (bl.length !== 12) bad('secretPassage needs 12 blanks');
    for (const w of W) if (bl.filter((b) => b.correctAnswer === w).length !== 1) bad(`secretPassage: "${w}" must fill exactly one blank`);
    bl.forEach((b, i) => {
      if (b.blankNumber !== i + 1) bad(`secretPassage blank ${i + 1}: wrong blankNumber`);
      if (!Array.isArray(b.options) || b.options.length !== 4 || !b.options.includes(b.correctAnswer)) bad(`secretPassage blank ${i + 1}: need 4 options including the answer`);
    });
    // word scales and imposter hunt
    const wsi = d.wordScaleImposter || {};
    const sc = wsi.wordScales || [], ih = wsi.imposterHunt || [];
    if (sc.length !== 4) bad('need 4 wordScales');
    sc.forEach((s, i) => {
      if (!W.includes(s.vocabWord)) bad(`wordScale ${i + 1}: vocabWord not in set`);
      if (!Array.isArray(s.scale) || s.scale.length !== 3) bad(`wordScale ${i + 1}: need 3 steps`);
      else if ((s.scale[s.vocabPosition] || '').toLowerCase() !== s.vocabWord) bad(`wordScale ${i + 1}: vocabPosition does not point at the word`);
    });
    if (ih.length !== 8) bad('need 8 imposterHunt rows');
    ih.forEach((h, i) => {
      if (!Array.isArray(h.words) || h.words.length !== 4) bad(`imposter ${i + 1}: need 4 words`);
      else if (h.words[h.imposterIndex] !== h.imposterWord) bad(`imposter ${i + 1}: imposterIndex does not point at imposterWord`);
    });
    // no reference products anywhere a student could see (or in sources)
    const flat = JSON.stringify(d);
    if (BANNED.test(flat)) bad('names a reference product: ' + flat.match(BANNED)[0]);
  }
}
console.log(`${sets} sets checked, ${errors} error(s).`);
process.exit(errors ? 1 : 0);
