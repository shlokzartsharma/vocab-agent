import React, { useState } from 'react';
import { useApp } from '../context/AppContext';

export default function Definitions() {
  const { content, markProgress, goToSet } = useApp();
  const [cardIndex, setCardIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);

  if (!content?.definitions) return null;

  const defs = content.definitions;
  const def = defs[cardIndex];
  const isLast = cardIndex === defs.length - 1;

  const handleNext = () => {
    if (isLast) {
      markProgress({ definitionsReviewed: true });
      goToSet();
    } else {
      setFlipped(false);
      setCardIndex((i) => i + 1);
    }
  };

  return (
    <div className="va-definitions">
      <button className="va-back-btn" onClick={goToSet}>← Back to Set</button>

      <div className="va-def-counter">
        {cardIndex + 1} / {defs.length}
      </div>

      <div
        className={`va-flashcard ${flipped ? 'flipped' : ''}`}
        onClick={() => setFlipped((f) => !f)}
      >
        <div className="va-flashcard-inner">
          <div className="va-flashcard-front">
            <div className="va-flashcard-word">{def.word}</div>
            <div className="va-flashcard-pos">{def.partOfSpeech}</div>
            <p className="va-flashcard-hint">Tap to see definition</p>
          </div>
          <div className="va-flashcard-back">
            <div className="va-flashcard-word-small">{def.word}</div>
            <div className="va-flashcard-meaning">
              <strong>1.</strong> {def.meaning1}
            </div>
            {def.meaning2 && (
              <div className="va-flashcard-meaning">
                <strong>2.</strong> {def.meaning2}
              </div>
            )}
            <div className="va-flashcard-challenge">
              <strong>Challenge:</strong> {def.studentChallenge}
            </div>
          </div>
        </div>
      </div>

      <div className="va-def-nav">
        {cardIndex > 0 && (
          <button
            className="va-btn va-btn--secondary"
            onClick={() => { setFlipped(false); setCardIndex((i) => i - 1); }}
          >
            ← Previous
          </button>
        )}
        <button className="va-btn va-btn--primary" onClick={handleNext}>
          {isLast ? 'Done Reviewing ✓' : 'Next →'}
        </button>
      </div>
    </div>
  );
}
