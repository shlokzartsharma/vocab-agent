// Content loader — imports all JSON content files
// Grade 3: 40 sets, Grade 4: 24 sets, Grade 5: 48 sets

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
  return [3, 4, 5];
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
