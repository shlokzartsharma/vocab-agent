import React, { useState, useMemo } from 'react';
import { useApp } from '../context/AppContext';

function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function ScaleItem({ scale, vocabWord, onComplete }) {
  const [order, setOrder] = useState(() => shuffleArray(scale));
  const [checked, setChecked] = useState(false);
  const [correct, setCorrect] = useState(false);

  const handleMove = (fromIndex, direction) => {
    if (checked) return;
    const toIndex = fromIndex + direction;
    if (toIndex < 0 || toIndex >= order.length) return;
    const newOrder = [...order];
    [newOrder[fromIndex], newOrder[toIndex]] = [newOrder[toIndex], newOrder[fromIndex]];
    setOrder(newOrder);
  };

  const handleCheck = () => {
    const isCorrect = order.every((word, i) => word === scale[i]);
    setCorrect(isCorrect);
    setChecked(true);
    if (isCorrect) onComplete();
  };

  const handleShowAnswer = () => {
    setOrder([...scale]);
    setChecked(true);
    setCorrect(true);
    onComplete();
  };

  return (
    <div className={`va-scale-item ${checked ? (correct ? 'correct' : 'incorrect') : ''}`}>
      <h4>Arrange from weakest → strongest:</h4>
      <div className="va-scale-words">
        {order.map((word, i) => (
          <div key={word} className={`va-scale-word ${word === vocabWord ? 'vocab' : ''}`}>
            <button
              className="va-scale-arrow"
              onClick={() => handleMove(i, -1)}
              disabled={i === 0 || checked}
            >↑</button>
            <span>{word}</span>
            <button
              className="va-scale-arrow"
              onClick={() => handleMove(i, 1)}
              disabled={i === order.length - 1 || checked}
            >↓</button>
          </div>
        ))}
      </div>
      <div className="va-scale-label-row">
        <span className="va-scale-label">weakest</span>
        <span className="va-scale-label">strongest</span>
      </div>
      {!checked ? (
        <div className="va-scale-actions">
          <button className="va-btn va-btn--primary va-btn--small" onClick={handleCheck}>
            Check
          </button>
          <button className="va-btn va-btn--secondary va-btn--small" onClick={handleShowAnswer}>
            Show Answer
          </button>
        </div>
      ) : (
        <div className={`va-scale-feedback ${correct ? 'correct' : 'incorrect'}`}>
          {correct ? 'Correct!' : `Correct order: ${scale.join(' → ')}`}
        </div>
      )}
    </div>
  );
}

export default function WordScale() {
  const { content, markProgress, goToSet } = useApp();
  const [completed, setCompleted] = useState(0);

  if (!content?.wordScaleImposter?.wordScales) return null;

  const scales = content.wordScaleImposter.wordScales;

  const handleComplete = () => {
    const newCount = completed + 1;
    setCompleted(newCount);
    if (newCount >= scales.length) {
      markProgress({ wordScaleDone: true });
    }
  };

  return (
    <div className="va-wordscale">
      <button className="va-back-btn" onClick={goToSet}>← Back to Set</button>

      <h2>Word Scale</h2>
      <p className="va-wordscale-instructions">
        Order each group of words from <strong>weakest</strong> to <strong>strongest</strong> intensity.
      </p>

      <div className="va-scale-grid">
        {scales.map((s) => (
          <ScaleItem
            key={s.vocabWord}
            scale={s.scale}
            vocabWord={s.vocabWord}
            onComplete={handleComplete}
          />
        ))}
      </div>

      {completed >= scales.length && (
        <button className="va-btn va-btn--primary" onClick={goToSet}>
          Done — Back to Set ✓
        </button>
      )}
    </div>
  );
}
