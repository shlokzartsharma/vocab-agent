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
