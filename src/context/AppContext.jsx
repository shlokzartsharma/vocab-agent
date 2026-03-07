import React, { createContext, useContext, useState, useCallback } from 'react';
import { getContent, getSetList, getGrades, getGradeInfo } from '../data/content';
import { getSetProgress, updateSetProgress, getGradeProgress } from '../data/progress';

const AppContext = createContext();

// Screens: home, grade, set, story, definitions, quiz, passage, wordscale, imposter
export function AppProvider({ children }) {
  const [screen, setScreen] = useState('home');
  const [selectedGrade, setSelectedGrade] = useState(null);
  const [selectedSet, setSelectedSet] = useState(null);
  const [content, setContent] = useState(null);
  const [progress, setProgress] = useState(null);

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
