import React from 'react';
import { useApp } from '../context/AppContext';

import { getTotals } from '../data/content';

// Card colours cycle through the brand palette so any grade that has content gets a card.
const PALETTE = ['var(--teal)', 'var(--magenta)', 'var(--gold)'];
const gradeColors = (grade, i) => ({ bg: i % 2 ? 'var(--cream)' : 'var(--cream-2)', border: PALETTE[i % PALETTE.length], text: 'var(--ink)', label: `Grade ${grade}` });

export default function HomeScreen() {
  const { selectGrade, getGradeInfo, getGradeProgress, getGrades } = useApp();
  const totals = getTotals();

  return (
    <div className="va-home">
      <div className="va-home-hero">
        <h1 className="va-home-title">Vocab Agent</h1>
        <p className="va-home-subtitle">
          Master {totals.words.toLocaleString()} vocabulary words across {totals.range} with stories, quizzes, and interactive activities.
        </p>
      </div>

      <div className="va-grade-cards">
        {getGrades().map((grade, i) => {
          const info = getGradeInfo(grade);
          const prog = getGradeProgress(grade, info.totalSets);
          const colors = gradeColors(grade, i);
          return (
            <button
              key={grade}
              className="va-grade-card"
              style={{
                '--card-bg': colors.bg,
                '--card-border': colors.border,
                '--card-text': colors.text,
              }}
              onClick={() => selectGrade(grade)}
            >
              <div className="va-grade-card-label">{colors.label}</div>
              <div className="va-grade-card-stats">
                <span>{info.totalSets} sets</span>
                <span className="va-dot">·</span>
                <span>{info.totalWords} words</span>
              </div>
              {prog.started > 0 && (
                <div className="va-grade-card-progress">
                  <div className="va-progress-bar">
                    <div
                      className="va-progress-fill"
                      style={{
                        width: `${(prog.completed / prog.total) * 100}%`,
                        backgroundColor: colors.border,
                      }}
                    />
                  </div>
                  <span className="va-progress-text">
                    {prog.completed}/{prog.total} complete
                  </span>
                </div>
              )}
            </button>
          );
        })}
      </div>

      <div className="va-home-footer">
        <p>Part of <strong>FlyingMinds.org</strong> · Powered by 25+ curriculum sources worldwide</p>
      </div>
    </div>
  );
}
