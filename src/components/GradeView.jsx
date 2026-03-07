import React, { useState } from 'react';
import { useApp } from '../context/AppContext';

const GENRE_ICONS = {
  'Indian folktale': '📖',
  'real science discovery': '🔬',
  'true historical figure biography': '🏛️',
  'mystery set in a school': '🔍',
  'space exploration with real NASA/ISRO facts': '🚀',
  'detective or spy fiction': '🕵️',
  'time travel adventure mixing real history': '⏰',
  'ocean or nature adventure': '🌊',
  'Indian mythology retelling (Panchatantra/Jataka/Mahabharata)': '🐘',
  'real world records and achievements': '🏆',
  'climate and environment true story': '🌍',
  'sports underdog true story': '⚽',
};

export default function GradeView() {
  const { selectedGrade, selectSet, goHome, getSetList } = useApp();
  const [search, setSearch] = useState('');

  const sets = getSetList(selectedGrade);
  const filtered = search
    ? sets.filter(
        (s) =>
          s.words.some((w) => w.toLowerCase().includes(search.toLowerCase())) ||
          s.genre.toLowerCase().includes(search.toLowerCase())
      )
    : sets;

  return (
    <div className="va-grade-view">
      <div className="va-breadcrumb">
        <button onClick={goHome} className="va-breadcrumb-link">Home</button>
        <span className="va-breadcrumb-sep">/</span>
        <span className="va-breadcrumb-current">Grade {selectedGrade}</span>
      </div>

      <h2 className="va-grade-title">Grade {selectedGrade} Vocabulary</h2>
      <p className="va-grade-subtitle">{sets.length} sets · {sets.length * 12} words</p>

      <input
        type="text"
        className="va-search"
        placeholder="Search words or genres..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="va-set-grid">
        {filtered.map((s) => (
          <button
            key={s.setNumber}
            className="va-set-card"
            onClick={() => selectSet(selectedGrade, s.setNumber)}
          >
            <div className="va-set-card-header">
              <span className="va-set-number">Set {s.setNumber}</span>
              <span className="va-set-genre">{GENRE_ICONS[s.genre] || '📚'} {s.genre}</span>
            </div>
            <div className="va-set-words">
              {s.words.map((w) => (
                <span key={w} className="va-word-chip">{w}</span>
              ))}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
