# Grade 5 Content Generation Instructions

Read /Users/suchitrasharma/vocab-agent/content/grade3/set12.json FIRST to see the exact JSON structure.

Generate a JSON file for each assigned set at: /Users/suchitrasharma/vocab-agent/content/grade5/setN.json

## Top-Level Fields
```json
{
  "grade": 5,
  "setNumber": N,
  "words": ["word1", ..., "word12"],
  "sources": ["Common Core Grade 5", "Sadlier Vocabulary Workshop", "Wordly Wise 3000", "Flocabulary Grade 5", "CKLA Grade 5", "Tier 2 Academic"],
  "genre": "assigned genre string",
  "story": { ... },
  "definitions": [ ... ],
  "doubleTakeQuiz": [ ... ],
  "secretPassage": { ... },
  "wordScaleImposter": { ... }
}
```

## story
- genre: string (as assigned)
- characters: array of 3 character name strings (as assigned)
- parts: array of exactly 4 objects, each with "title" (string) and "text" (string)
- Every single vocab word MUST appear EXACTLY ONCE in the story text, bolded as **word**
- Total wordCount across all 4 parts: 230-250 words
- Age-appropriate for Grade 5 (10-11 year olds) — these are harder words so the stories can be slightly more sophisticated than Grade 4
- The story should make vocab word meanings clear from context
- wordCount: integer (actual word count)
- Part 4 wraps up the story without any vocab words — it's a reflection/conclusion

## definitions (array of 12)
Each object:
- "word": lowercase string
- "partOfSpeech": e.g. "noun", "verb", "adjective", "noun, verb", "adjective, verb"
- "meaning1": "Clear definition for a 5th grader. Example: A natural-sounding example sentence." (ALWAYS filled)
- "meaning2": "Second meaning if the word has one. Example: Example sentence." (use "" if no clear second meaning)
- "studentChallenge": "Fill-in-the-blank sentence where ___ is the answer." (use three underscores)
- "sentence": "" (always empty string)

## doubleTakeQuiz (array of 12)
Each object:
- "questionNumber": 1 through 12
- "sentence1": sentence with _______ (7 underscores) as blank
- "sentence2": DIFFERENT sentence with _______ as blank (same answer)
- "options": array of 4 words from this set's 12 words
- "correctIndex": 0-based index of correct answer in options array
- "correctAnswer": the correct word string
- Two sentences should show word in slightly different contexts/meanings
- Each vocab word is the correct answer exactly once across the 12 questions
- Options should be plausible distractors (same part of speech when possible)

## secretPassage
- "instructions": "Read the passage below. Fill in each blank with the correct vocabulary word from the word bank."
- "wordBank": array of all 12 words in same order as the words array
- "passage": A cohesive narrative passage using _(1)_ through _(12)_ for blanks. Use \n for paragraph breaks. Must read as a coherent story.
- "blanks": array of 12 objects, each with:
  - "blankNumber": 1-12
  - "correctAnswer": the vocab word
  - "options": array of 4 words from the word bank (includes correct + 3 distractors)
- Each vocab word appears exactly once as a correctAnswer
- The passage should be different from (but can be thematically similar to) the story

## wordScaleImposter
- "wordScales": array of exactly 4 objects:
  - "vocabWord": one of the 12 vocab words
  - "scale": array of exactly 3 strings showing intensity gradient (weak → strong), first letter capitalized
  - "vocabPosition": 0, 1, or 2 (index of vocabWord in the scale)
- "imposterHunt": array of exactly 8 objects:
  - "vocabWord": one of the 12 vocab words
  - "words": array of exactly 4 strings (3 synonyms/related + 1 antonym/opposite), first letter capitalized
  - "imposterIndex": 0-based index of the imposter in the words array
  - "imposterWord": the imposter word string (capitalized)
- "studentPick": "Pick 2 imposters and explain why they are opposites of the vocabulary word."
- Choose 4 different words for scales and 8 different words for imposter hunt (can overlap with scale words)

## CRITICAL RULES
1. JSON must be valid — test by mentally parsing it
2. All arrays must have exactly the right number of elements
3. correctIndex must match the actual position of correctAnswer in options
4. Every vocab word used exactly once as correct answer in doubleTakeQuiz and secretPassage
5. No vocab word appears in its own studentChallenge sentence
6. Capitalize first letter of words in scale and imposterHunt word arrays
7. The story Part 4 should NOT contain any bolded vocab words — it's the reflection/wrap-up
