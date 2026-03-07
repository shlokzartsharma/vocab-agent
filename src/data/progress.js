// Progress tracking via localStorage

const STORAGE_KEY = 'vocab-agent-progress';

function loadProgress() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function saveProgress(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

export function getSetProgress(grade, setNumber) {
  const all = loadProgress();
  const key = `g${grade}s${setNumber}`;
  return all[key] || {
    storyRead: false,
    definitionsReviewed: false,
    quizScore: null,
    quizTotal: null,
    passageScore: null,
    passageTotal: null,
    wordScaleDone: false,
    imposterDone: false,
  };
}

export function updateSetProgress(grade, setNumber, updates) {
  const all = loadProgress();
  const key = `g${grade}s${setNumber}`;
  all[key] = { ...getSetProgress(grade, setNumber), ...updates };
  saveProgress(all);
  return all[key];
}

export function getGradeProgress(grade, totalSets) {
  const all = loadProgress();
  let completed = 0;
  let started = 0;
  for (let s = 1; s <= totalSets; s++) {
    const key = `g${grade}s${s}`;
    const p = all[key];
    if (p) {
      started++;
      if (p.storyRead && p.definitionsReviewed && p.quizScore !== null && p.passageScore !== null) {
        completed++;
      }
    }
  }
  return { completed, started, total: totalSets };
}

export function resetProgress() {
  localStorage.removeItem(STORAGE_KEY);
}
