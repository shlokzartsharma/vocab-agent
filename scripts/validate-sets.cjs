#!/usr/bin/env node
// Validates vocab set JSON files for correct structure and content
const fs = require('fs');
const path = require('path');

const grade = parseInt(process.argv[2] || '4');
const startSet = parseInt(process.argv[3] || '1');
const endSet = parseInt(process.argv[4] || '12');

let totalErrors = 0;
let totalWarnings = 0;

for (let s = startSet; s <= endSet; s++) {
  const filePath = path.join(__dirname, '..', 'content', `grade${grade}`, `set${s}.json`);
  if (!fs.existsSync(filePath)) {
    console.log(`\n❌ set${s}.json NOT FOUND`);
    totalErrors++;
    continue;
  }

  let data;
  try {
    data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    console.log(`\n❌ set${s}.json INVALID JSON: ${e.message}`);
    totalErrors++;
    continue;
  }

  const errors = [];
  const warnings = [];
  const words = data.words || [];

  // 1. Check doubleTakeQuiz
  const dt = data.doubleTakeQuiz;
  if (!dt || !Array.isArray(dt)) {
    errors.push('doubleTakeQuiz missing or not array');
  } else {
    if (dt.length !== 12) errors.push(`doubleTakeQuiz has ${dt.length} questions, expected 12`);
    dt.forEach((q, i) => {
      if (!q.options || q.options.length !== 4) {
        errors.push(`DT Q${i+1}: options not 4 items`);
      } else {
        const idx = q.options.indexOf(q.correctAnswer);
        if (idx === -1) errors.push(`DT Q${i+1}: correctAnswer "${q.correctAnswer}" not in options`);
        else if (idx !== q.correctIndex) errors.push(`DT Q${i+1}: correctIndex=${q.correctIndex} but answer at index ${idx}`);
      }
      if (!q.sentence1 || !q.sentence2) errors.push(`DT Q${i+1}: missing sentence1 or sentence2`);
    });
  }

  // 2. Check secretPassage
  const sp = data.secretPassage;
  if (!sp) {
    errors.push('secretPassage missing');
  } else {
    if (!sp.wordBank || sp.wordBank.length !== 12) errors.push(`SP wordBank has ${sp.wordBank?.length} words, expected 12`);
    if (!sp.passage) errors.push('SP passage missing');
    if (!sp.blanks || sp.blanks.length !== 12) {
      errors.push(`SP has ${sp.blanks?.length} blanks, expected 12`);
    } else {
      const usedWords = sp.blanks.map(b => b.correctAnswer.toLowerCase());
      const wordSet = new Set(usedWords);
      if (wordSet.size !== 12) {
        const dupes = usedWords.filter((w, i) => usedWords.indexOf(w) !== i);
        errors.push(`SP duplicate words: ${dupes.join(', ')}`);
      }
      // Check all set words are used
      const missing = words.filter(w => !wordSet.has(w.toLowerCase()));
      if (missing.length > 0) errors.push(`SP missing words: ${missing.join(', ')}`);

      sp.blanks.forEach((b, i) => {
        if (!b.options || b.options.length !== 4) {
          errors.push(`SP blank ${i+1}: options not 4 items`);
        } else {
          const found = b.options.some(o => o.toLowerCase() === b.correctAnswer.toLowerCase());
          if (!found) errors.push(`SP blank ${i+1}: correctAnswer "${b.correctAnswer}" not in options`);
        }
      });
    }
  }

  // 3. Check wordScaleImposter
  const wsi = data.wordScaleImposter;
  if (!wsi) {
    errors.push('wordScaleImposter missing');
  } else {
    // Word Scales
    if (!wsi.wordScales || wsi.wordScales.length !== 4) {
      errors.push(`wordScales has ${wsi.wordScales?.length} entries, expected 4`);
    } else {
      wsi.wordScales.forEach((ws, i) => {
        if (!ws.scale || ws.scale.length !== 3) errors.push(`WS ${i+1}: scale has ${ws.scale?.length} words, expected 3`);
        else {
          const pos = ws.vocabPosition;
          if (pos < 0 || pos > 2) errors.push(`WS ${i+1}: vocabPosition ${pos} out of range`);
          else {
            const atPos = ws.scale[pos].toLowerCase();
            const vocab = ws.vocabWord.toLowerCase();
            if (atPos !== vocab) warnings.push(`WS ${i+1}: vocabWord="${ws.vocabWord}" but scale[${pos}]="${ws.scale[pos]}"`);
          }
        }
      });
    }

    // Imposter Hunt
    if (!wsi.imposterHunt || wsi.imposterHunt.length !== 8) {
      errors.push(`imposterHunt has ${wsi.imposterHunt?.length} entries, expected 8`);
    } else {
      wsi.imposterHunt.forEach((ih, i) => {
        if (!ih.words || ih.words.length !== 4) errors.push(`IH ${i+1}: words has ${ih.words?.length} items, expected 4`);
        else {
          const idx = ih.imposterIndex;
          if (idx < 0 || idx > 3) errors.push(`IH ${i+1}: imposterIndex ${idx} out of range`);
          else if (ih.words[idx] !== ih.imposterWord) {
            errors.push(`IH ${i+1}: imposterWord="${ih.imposterWord}" but words[${idx}]="${ih.words[idx]}"`);
          }
        }
      });
    }
  }

  // Print results
  const status = errors.length === 0 ? '✅' : '❌';
  console.log(`\n${status} Grade ${grade} Set ${s}: ${errors.length} errors, ${warnings.length} warnings`);
  errors.forEach(e => console.log(`  ❌ ${e}`));
  warnings.forEach(w => console.log(`  ⚠️  ${w}`));
  totalErrors += errors.length;
  totalWarnings += warnings.length;
}

console.log(`\n${'='.repeat(50)}`);
console.log(`Total: ${totalErrors} errors, ${totalWarnings} warnings`);
if (totalErrors === 0) console.log('🎉 All sets passed validation!');
