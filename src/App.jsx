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
import { getTotals } from './data/content';
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
      <main className="va-main">
        <Screen />
      </main>
      <footer className="va-footer">
        <span>{getTotals().words.toLocaleString()} words · {getTotals().sets} sets · {getTotals().range}</span>
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
