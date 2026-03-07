import React, { useState } from 'react';
import { useApp } from '../context/AppContext';

export default function StoryReader() {
  const { content, markProgress, goToSet } = useApp();
  const [partIndex, setPartIndex] = useState(0);

  if (!content?.story) return null;

  const parts = content.story.parts;
  const part = parts[partIndex];
  const isLast = partIndex === parts.length - 1;

  const renderText = (text) => {
    // Split on **word** and render bold spans
    const segments = text.split(/\*\*(.+?)\*\*/g);
    return segments.map((seg, i) =>
      i % 2 === 1 ? (
        <span key={i} className="va-vocab-highlight">{seg}</span>
      ) : (
        <span key={i}>{seg}</span>
      )
    );
  };

  const handleNext = () => {
    if (isLast) {
      markProgress({ storyRead: true });
      goToSet();
    } else {
      setPartIndex((p) => p + 1);
    }
  };

  return (
    <div className="va-story">
      <button className="va-back-btn" onClick={goToSet}>← Back to Set</button>

      <div className="va-story-progress">
        {parts.map((_, i) => (
          <div
            key={i}
            className={`va-story-dot ${i === partIndex ? 'active' : ''} ${i < partIndex ? 'done' : ''}`}
          />
        ))}
      </div>

      <div className="va-story-card">
        <h3 className="va-story-part-title">
          Part {partIndex + 1}: {part.title}
        </h3>
        <div className="va-story-text">{renderText(part.text)}</div>
      </div>

      <div className="va-story-nav">
        {partIndex > 0 && (
          <button className="va-btn va-btn--secondary" onClick={() => setPartIndex((p) => p - 1)}>
            ← Previous
          </button>
        )}
        <button className="va-btn va-btn--primary" onClick={handleNext}>
          {isLast ? 'Finish Reading ✓' : 'Next →'}
        </button>
      </div>
    </div>
  );
}
