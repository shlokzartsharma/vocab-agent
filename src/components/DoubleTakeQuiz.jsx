import React, { useState } from 'react';
import { useApp } from '../context/AppContext';

export default function DoubleTakeQuiz() {
  const { content, markProgress, goToSet } = useApp();
  const [qIndex, setQIndex] = useState(0);
  const [selected, setSelected] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [finished, setFinished] = useState(false);

  if (!content?.doubleTakeQuiz) return null;

  const questions = content.doubleTakeQuiz;
  const q = questions[qIndex];
  const isLast = qIndex === questions.length - 1;

  const handleSelect = (optionIndex) => {
    if (showResult) return;
    setSelected(optionIndex);
    setShowResult(true);
    if (optionIndex === q.correctIndex) {
      setScore((s) => s + 1);
    }
  };

  const handleNext = () => {
    if (isLast) {
      const finalScore = score + (selected === q.correctIndex ? 0 : 0); // already counted
      markProgress({ quizScore: score, quizTotal: questions.length });
      setFinished(true);
    } else {
      setSelected(null);
      setShowResult(false);
      setQIndex((i) => i + 1);
    }
  };

  if (finished) {
    const pct = Math.round((score / questions.length) * 100);
    return (
      <div className="va-quiz-complete">
        <button className="va-back-btn" onClick={goToSet}>← Back to Set</button>
        <div className="va-complete-card">
          <div className="va-complete-icon">{pct >= 80 ? '🌟' : pct >= 60 ? '👍' : '📚'}</div>
          <h2>Quiz Complete!</h2>
          <div className="va-complete-score">{score} / {questions.length}</div>
          <p className="va-complete-pct">{pct}% correct</p>
          <div className="va-complete-actions">
            <button className="va-btn va-btn--secondary" onClick={() => {
              setQIndex(0); setSelected(null); setShowResult(false);
              setScore(0); setFinished(false);
            }}>
              Try Again
            </button>
            <button className="va-btn va-btn--primary" onClick={goToSet}>
              Back to Set
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="va-quiz">
      <button className="va-back-btn" onClick={goToSet}>← Back to Set</button>

      <div className="va-quiz-progress">
        <span>Question {qIndex + 1} of {questions.length}</span>
        <span className="va-quiz-score">Score: {score}</span>
      </div>

      <div className="va-quiz-card">
        <div className="va-quiz-sentences">
          <div className="va-quiz-sentence">
            <span className="va-quiz-label">Sentence 1:</span>
            <p>{q.sentence1}</p>
          </div>
          <div className="va-quiz-sentence">
            <span className="va-quiz-label">Sentence 2:</span>
            <p>{q.sentence2}</p>
          </div>
        </div>

        <div className="va-quiz-options">
          {q.options.map((opt, i) => {
            let cls = 'va-quiz-option';
            if (showResult) {
              if (i === q.correctIndex) cls += ' correct';
              else if (i === selected) cls += ' incorrect';
            } else if (i === selected) {
              cls += ' selected';
            }
            return (
              <button key={i} className={cls} onClick={() => handleSelect(i)}>
                {opt}
              </button>
            );
          })}
        </div>

        {showResult && (
          <div className={`va-quiz-feedback ${selected === q.correctIndex ? 'correct' : 'incorrect'}`}>
            {selected === q.correctIndex
              ? 'Correct! Great job!'
              : `Not quite. The answer is "${q.correctAnswer}".`}
          </div>
        )}
      </div>

      {showResult && (
        <button className="va-btn va-btn--primary" onClick={handleNext}>
          {isLast ? 'See Results' : 'Next Question →'}
        </button>
      )}
    </div>
  );
}
