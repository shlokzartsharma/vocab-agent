import React, { useState, useMemo } from 'react';
import { useApp } from '../context/AppContext';

export default function SecretPassage() {
  const { content, markProgress, goToSet } = useApp();
  const [answers, setAnswers] = useState({});
  const [checked, setChecked] = useState(false);
  const [score, setScore] = useState(null);

  if (!content?.secretPassage) return null;

  const { passage, blanks, wordBank } = content.secretPassage;

  // Split passage into segments around _(N)_ markers
  const segments = useMemo(() => {
    const parts = passage.split(/(_\(\d+\)_)/g);
    return parts.map((part) => {
      const match = part.match(/^_\((\d+)\)_$/);
      if (match) {
        return { type: 'blank', number: parseInt(match[1]) };
      }
      return { type: 'text', content: part };
    });
  }, [passage]);

  const handleSelect = (blankNum, word) => {
    if (checked) return;
    setAnswers((prev) => ({ ...prev, [blankNum]: word }));
  };

  const handleCheck = () => {
    let correct = 0;
    blanks.forEach((b) => {
      if (answers[b.blankNumber] === b.correctAnswer) correct++;
    });
    setScore(correct);
    markProgress({ passageScore: correct, passageTotal: blanks.length });
    setChecked(true);
  };

  const handleReset = () => {
    setAnswers({});
    setChecked(false);
    setScore(null);
  };

  const allFilled = blanks.every((b) => answers[b.blankNumber]);

  // Track which words are used
  const usedWords = new Set(Object.values(answers));

  return (
    <div className="va-passage">
      <button className="va-back-btn" onClick={goToSet}>← Back to Set</button>

      <h2 className="va-passage-title">Secret Passage</h2>
      <p className="va-passage-instructions">
        Fill in each blank with the correct vocabulary word from the word bank.
      </p>

      <div className="va-word-bank">
        {wordBank.map((word) => (
          <span
            key={word}
            className={`va-bank-word ${usedWords.has(word) ? 'used' : ''}`}
          >
            {word}
          </span>
        ))}
      </div>

      <div className="va-passage-text">
        {segments.map((seg, i) => {
          if (seg.type === 'text') {
            return <span key={i}>{seg.content}</span>;
          }
          const blank = blanks.find((b) => b.blankNumber === seg.number);
          const answer = answers[seg.number];
          const isCorrect = checked && answer === blank?.correctAnswer;
          const isWrong = checked && answer && answer !== blank?.correctAnswer;

          return (
            <span key={i} className="va-blank-wrapper">
              <select
                className={`va-blank-select ${isCorrect ? 'correct' : ''} ${isWrong ? 'incorrect' : ''}`}
                value={answer || ''}
                onChange={(e) => handleSelect(seg.number, e.target.value)}
                disabled={checked}
              >
                <option value="">({seg.number})</option>
                {blank?.options.map((opt) => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
              {isWrong && checked && (
                <span className="va-blank-correction">{blank.correctAnswer}</span>
              )}
            </span>
          );
        })}
      </div>

      <div className="va-passage-actions">
        {!checked ? (
          <button
            className="va-btn va-btn--primary"
            onClick={handleCheck}
            disabled={!allFilled}
          >
            Check Answers
          </button>
        ) : (
          <>
            <div className="va-passage-score">
              Score: {score} / {blanks.length} ({Math.round((score / blanks.length) * 100)}%)
            </div>
            <div className="va-passage-btn-row">
              <button className="va-btn va-btn--secondary" onClick={handleReset}>
                Try Again
              </button>
              <button className="va-btn va-btn--primary" onClick={goToSet}>
                Back to Set
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
