import React from 'react';
import { useApp } from '../context/AppContext';

const GRADE_COLORS = {
  3: { bg: '#ECFDF5', border: '#10B981', text: '#065F46', label: 'Grade 3' },
  4: { bg: '#EFF6FF', border: '#3B82F6', text: '#1E40AF', label: 'Grade 4' },
  5: { bg: '#F5F3FF', border: '#8B5CF6', text: '#5B21B6', label: 'Grade 5' },
};

export default function HomeScreen() {
  const { selectGrade, getGradeInfo, getGradeProgress } = useApp();

  return (
    <div className="va-home">
      <div className="va-home-hero">
        <h1 className="va-home-title">Vocab Agent</h1>
        <p className="va-home-subtitle">
          Master 1,344 vocabulary words across Grades 3–5 with stories, quizzes, and interactive activities.
        </p>
      </div>

      <div className="va-grade-cards">
        {[3, 4, 5].map((grade) => {
          const info = getGradeInfo(grade);
          const prog = getGradeProgress(grade, info.totalSets);
          const colors = GRADE_COLORS[grade];
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
