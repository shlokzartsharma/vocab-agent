import React, { createContext, useContext, useState, useCallback, useEffect, useRef } from 'react';
import { getContent, getSetList, getGrades, getGradeInfo } from '../data/content';
import { getSetProgress, updateSetProgress, getGradeProgress } from '../data/progress';

const AppContext = createContext();

// Screen <-> address. Activity names in the URL are the ones a parent would recognise.
const STEP = { story: 'story', definitions: 'words', quiz: 'double-take', passage: 'secret-passage', wordscale: 'word-scale', imposter: 'imposter-hunt' };
const SCREEN_OF = Object.fromEntries(Object.entries(STEP).map(([k, v]) => [v, k]));

export function buildUrl(screen, grade, set) {
  const base = window.location.pathname;
  if (screen === 'home' || !grade) return base;
  const q = new URLSearchParams({ grade: String(grade) });
  if (screen !== 'grade' && set) {
    q.set('set', String(set));
    if (STEP[screen]) q.set('step', STEP[screen]);
  }
  return base + '?' + q.toString();
}

function readUrl() {
  const none = { screen: 'home', grade: null, set: null, content: null };
  try {
    const q = new URLSearchParams(window.location.search);
    const g = Number(q.get('grade'));
    if (!getGrades().includes(g)) return none;
    const n = Number(q.get('set'));
    const data = n ? getContent(g, n) : null;
    if (!data) return { screen: 'grade', grade: g, set: null, content: null };
    const step = SCREEN_OF[q.get('step')];
    return { screen: step || 'set', grade: g, set: n, content: data };
  } catch (e) { return none; }
}


// Screens: home, grade, set, story, definitions, quiz, passage, wordscale, imposter
export function AppProvider({ children }) {
  // Every screen has its own address (owner, 2026-11-14): /vocab-agent?grade=1&set=3&step=story.
  // Opening that link lands on the same screen; Back and Forward move between screens.
  const start = readUrl();
  const [screen, setScreen] = useState(start.screen);
  const [selectedGrade, setSelectedGrade] = useState(start.grade);
  const [selectedSet, setSelectedSet] = useState(start.set);
  const [content, setContent] = useState(start.content);
  const [progress, setProgress] = useState(start.set ? getSetProgress(start.grade, start.set) : null);
  const fromHistory = useRef(true); // the first render matches the URL already

  // Keep the address bar in step with the screen.
  useEffect(() => {
    const url = buildUrl(screen, selectedGrade, selectedSet);
    if (fromHistory.current) {
      fromHistory.current = false;
      if (url !== window.location.pathname + window.location.search) window.history.replaceState(null, '', url);
      return;
    }
    if (url !== window.location.pathname + window.location.search) window.history.pushState(null, '', url);
    window.scrollTo(0, 0);
  }, [screen, selectedGrade, selectedSet]);

  // Back / Forward: show the screen the address names.
  useEffect(() => {
    const onPop = () => {
      const st = readUrl();
      fromHistory.current = true;
      setSelectedGrade(st.grade);
      setSelectedSet(st.set);
      setContent(st.content);
      setProgress(st.set ? getSetProgress(st.grade, st.set) : null);
      setScreen(st.screen);
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);

  const selectGrade = useCallback((grade) => {
    setSelectedGrade(grade);
    setScreen('grade');
  }, []);

  const selectSet = useCallback((grade, setNumber) => {
    const data = getContent(grade, setNumber);
    if (data) {
      setSelectedGrade(grade);
      setSelectedSet(setNumber);
      setContent(data);
      setProgress(getSetProgress(grade, setNumber));
      setScreen('set');
    }
  }, []);

  const goToActivity = useCallback((activityScreen) => {
    setScreen(activityScreen);
  }, []);

  const markProgress = useCallback((updates) => {
    if (selectedGrade && selectedSet) {
      const updated = updateSetProgress(selectedGrade, selectedSet, updates);
      setProgress(updated);
    }
  }, [selectedGrade, selectedSet]);

  const goHome = useCallback(() => {
    setScreen('home');
    setSelectedGrade(null);
    setSelectedSet(null);
    setContent(null);
    setProgress(null);
  }, []);

  const goToGrade = useCallback(() => {
    setScreen('grade');
  }, []);

  const goToSet = useCallback(() => {
    setScreen('set');
  }, []);

  const value = {
    screen,
    selectedGrade,
    selectedSet,
    content,
    progress,
    selectGrade,
    selectSet,
    goToActivity,
    markProgress,
    goHome,
    goToGrade,
    goToSet,
    getSetList,
    getGrades,
    getGradeInfo,
    getGradeProgress,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  return useContext(AppContext);
}
