// Content loader — imports all JSON content files
// Grades and set counts come from the files themselves (content/gradeG/setN.json).

const contentModules = import.meta.glob('../../content/grade*/set*.json', { eager: true });

const CONTENT = {};

for (const [path, mod] of Object.entries(contentModules)) {
  const match = path.match(/grade(\d+)\/set(\d+)\.json$/);
  if (match) {
    const grade = parseInt(match[1]);
    const set = parseInt(match[2]);
    const key = `g${grade}s${set}`;
    CONTENT[key] = mod.default || mod;
  }
}

export function getContent(grade, setNumber) {
  return CONTENT[`g${grade}s${setNumber}`] || null;
}

export function getSetList(grade) {
  const sets = [];
  for (const [key, data] of Object.entries(CONTENT)) {
    if (data.grade === grade) {
      sets.push({
        setNumber: data.setNumber,
        words: data.words,
        genre: data.genre,
        sources: data.sources,
      });
    }
  }
  return sets.sort((a, b) => a.setNumber - b.setNumber);
}

export function getGrades() {
  return [...new Set(Object.values(CONTENT).map((d) => d.grade))].sort((a, b) => a - b);
}

export function getTotals() {
  const all = Object.values(CONTENT);
  const grades = getGrades();
  return {
    words: all.reduce((n, d) => n + (d.words || []).length, 0),
    sets: all.length,
    range: grades.length ? (grades.length === 1 ? `Grade ${grades[0]}` : `Grades ${grades[0]}–${grades[grades.length - 1]}`) : '',
  };
}

export function getGradeInfo(grade) {
  const sets = getSetList(grade);
  return {
    grade,
    totalSets: sets.length,
    totalWords: sets.reduce((sum, s) => sum + s.words.length, 0),
  };
}

export default CONTENT;
