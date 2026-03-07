import React from 'react';
import { AppProvider, useApp } from './context/AppContext';
import HomeScreen from './components/HomeScreen';
import GradeView from './components/GradeView';
import SetDashboard from './components/SetDashboard';
import StoryReader from './components/StoryReader';
import Definitions from './components/Definitions';
import DoubleTakeQuiz from './components/DoubleTakeQuiz';
import SecretPassage from './components/SecretPassage';
import WordScale from './components/WordScale';
import ImposterHunt from './components/ImposterHunt';
import './App.css';

function AppContent() {
  const { screen, goHome } = useApp();

  const screens = {
    home: HomeScreen,
    grade: GradeView,
    set: SetDashboard,
    story: StoryReader,
    definitions: Definitions,
    quiz: DoubleTakeQuiz,
    passage: SecretPassage,
    wordscale: WordScale,
    imposter: ImposterHunt,
  };

  const Screen = screens[screen] || HomeScreen;

  return (
    <div className="va-app">
      <header className="va-header">
        <div className="va-logo-group" onClick={goHome}>
          <svg className="va-logo-icon" width="28" height="28" viewBox="0 0 28 28" fill="none">
            <rect width="28" height="28" rx="6" fill="#6366F1"/>
            <text x="14" y="19" textAnchor="middle" fill="white" fontSize="16" fontWeight="700" fontFamily="Inter, sans-serif">V</text>
          </svg>
          <span className="va-logo">Vocab Agent</span>
        </div>
        <span className="va-header-sub">FlyingMinds.org</span>
      </header>
      <main className="va-main">
        <Screen />
      </main>
      <footer className="va-footer">
        <span>1,344 words · 112 sets · Grades 3–5</span>
        <span className="va-footer-sep">·</span>
        <span>FlyingMinds.org</span>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}
