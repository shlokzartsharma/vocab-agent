import React from 'react';
import { useApp } from '../context/AppContext';

const ACTIVITIES = [
  {
    key: 'story',
    title: 'Read the Story',
    icon: '📖',
    description: 'Read a 4-part story using all 12 vocabulary words in context.',
    progressKey: 'storyRead',
    doneLabel: 'Read',
  },
  {
    key: 'definitions',
    title: 'Study Definitions',
    icon: '📝',
    description: 'Flip through flashcards with meanings, examples, and challenges.',
    progressKey: 'definitionsReviewed',
    doneLabel: 'Reviewed',
  },
  {
    key: 'quiz',
    title: 'Double-Take Quiz',
    icon: '🎯',
    description: 'Choose the right word for two different context sentences.',
    progressKey: 'quizScore',
    doneLabel: null,
  },
  {
    key: 'passage',
    title: 'Secret Passage',
    icon: '🔐',
    description: 'Fill in the blanks in a mystery passage using the word bank.',
    progressKey: 'passageScore',
    doneLabel: null,
  },
  {
    key: 'wordscale',
    title: 'Word Scale',
    icon: '📊',
    description: 'Order 4 related words from weakest to strongest intensity.',
    progressKey: 'wordScaleDone',
    doneLabel: 'Complete',
  },
  {
    key: 'imposter',
    title: 'Imposter Hunt',
    icon: '🕵️',
    description: 'Find the word that does NOT belong with the synonyms.',
    progressKey: 'imposterDone',
    doneLabel: 'Complete',
  },
];

export default function SetDashboard() {
  const { content, progress, goToActivity, goToGrade, goHome, selectedGrade, selectedSet } = useApp();

  if (!content) return null;

  const getStatus = (activity) => {
    if (!progress) return 'not-started';
    const val = progress[activity.progressKey];
    if (val === null || val === undefined || val === false) return 'not-started';
    return 'done';
  };

  const getScoreLabel = (activity) => {
    if (!progress) return null;
    if (activity.progressKey === 'quizScore' && progress.quizScore !== null) {
      return `${progress.quizScore}/${progress.quizTotal}`;
    }
    if (activity.progressKey === 'passageScore' && progress.passageScore !== null) {
      return `${progress.passageScore}/${progress.passageTotal}`;
    }
    if (activity.doneLabel && progress[activity.progressKey]) {
      return activity.doneLabel;
    }
    return null;
  };

  return (
    <div className="va-set-dashboard">
      <div className="va-breadcrumb">
        <button onClick={goHome} className="va-breadcrumb-link">Home</button>
        <span className="va-breadcrumb-sep">/</span>
        <button onClick={goToGrade} className="va-breadcrumb-link">Grade {selectedGrade}</button>
        <span className="va-breadcrumb-sep">/</span>
        <span className="va-breadcrumb-current">Set {selectedSet}</span>
      </div>

      <div className="va-set-header">
        <h2>Set {selectedSet}: {content.genre}</h2>
        <div className="va-set-word-list">
          {content.words.map((w) => (
            <span key={w} className="va-word-chip va-word-chip--large">{w}</span>
          ))}
        </div>
      </div>

      <div className="va-activity-grid">
        {ACTIVITIES.map((activity) => {
          const status = getStatus(activity);
          const score = getScoreLabel(activity);
          return (
            <button
              key={activity.key}
              className={`va-activity-card va-activity-card--${status}`}
              onClick={() => goToActivity(activity.key)}
            >
              <div className="va-activity-icon">{activity.icon}</div>
              <div className="va-activity-info">
                <h3>{activity.title}</h3>
                <p>{activity.description}</p>
              </div>
              {score && <div className="va-activity-badge">{score}</div>}
            </button>
          );
        })}
      </div>
    </div>
  );
}
