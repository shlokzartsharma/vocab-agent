import React, { useState } from 'react';
import { useApp } from '../context/AppContext';

function HuntItem({ data, onComplete }) {
  const [selected, setSelected] = useState(null);
  const [checked, setChecked] = useState(false);

  const handleSelect = (index) => {
    if (checked) return;
    setSelected(index);
    setChecked(true);
    if (index === data.imposterIndex) {
      onComplete();
    }
  };

  return (
    <div className={`va-hunt-item ${checked ? (selected === data.imposterIndex ? 'correct' : 'incorrect') : ''}`}>
      <h4>
        Which word does NOT belong with <span className="va-hunt-vocab">{data.vocabWord}</span>?
      </h4>
      <div className="va-hunt-options">
        {data.words.map((word, i) => {
          let cls = 'va-hunt-word';
          if (checked) {
            if (i === data.imposterIndex) cls += ' imposter';
            if (i === selected && i !== data.imposterIndex) cls += ' wrong';
          }
          return (
            <button key={i} className={cls} onClick={() => handleSelect(i)}>
              {word}
            </button>
          );
        })}
      </div>
      {checked && (
        <div className={`va-hunt-feedback ${selected === data.imposterIndex ? 'correct' : 'incorrect'}`}>
          {selected === data.imposterIndex
            ? `Correct! "${data.imposterWord}" is the opposite/imposter.`
            : `The imposter was "${data.imposterWord}" — it means the opposite of ${data.vocabWord}.`}
        </div>
      )}
    </div>
  );
}

export default function ImposterHunt() {
  const { content, markProgress, goToSet } = useApp();
  const [completed, setCompleted] = useState(0);

  if (!content?.wordScaleImposter?.imposterHunt) return null;

  const hunts = content.wordScaleImposter.imposterHunt;

  const handleComplete = () => {
    const newCount = completed + 1;
    setCompleted(newCount);
    if (newCount >= hunts.length) {
      markProgress({ imposterDone: true });
    }
  };

  return (
    <div className="va-imposter">
      <button className="va-back-btn" onClick={goToSet}>← Back to Set</button>

      <h2>Imposter Hunt</h2>
      <p className="va-imposter-instructions">
        Each group has synonyms and ONE imposter (opposite). Find the word that does NOT belong!
      </p>

      <div className="va-hunt-grid">
        {hunts.map((h) => (
          <HuntItem key={h.vocabWord} data={h} onComplete={handleComplete} />
        ))}
      </div>

      {completed >= hunts.length && (
        <button className="va-btn va-btn--primary" onClick={goToSet}>
          Done — Back to Set ✓
        </button>
      )}
    </div>
  );
}
