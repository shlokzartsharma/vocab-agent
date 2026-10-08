# New-grade content generation (Grades 1, 2, 6, 7, 8)

Read content/grade3/set12.json FIRST to see the exact JSON structure, and follow it exactly.

Write each assigned set to content/gradeG/setN.json (G = grade, N = set number).

## Top-Level Fields
"grade" (number), "setNumber" (number), "words" (array of the 12 assigned words, in the assigned order),
"sources": ["Common Core Grade G", "Tier 2 Academic", "Custom (Existing)"] (internal only, never shown; never name a publisher or product),
"genre" (the assigned genre), "story", "definitions", "doubleTakeQuiz", "secretPassage", "wordScaleImposter".

## Age adjustments (these OVERRIDE the word counts and reading level below)
- Grade 1 (ages 6-7): story total 120-150 words, short sentences (mostly under 12 words), concrete everyday settings (home, school, park, animals). Definitions in very simple words a 6-year-old knows; examples about their world. Nothing scary.
- Grade 2 (ages 7-8): story total 150-190 words, simple sentences, familiar settings.
- Grade 6 (ages 11-12): story total 240-270 words; richer settings (history, science, adventure, school life).
- Grade 7 (ages 12-13): story total 250-280 words; mild suspense, debate or mystery are fine.
- Grade 8 (ages 13-14): story total 260-300 words; more mature themes (justice, courage, change), still school-appropriate.
- Every story, definition and quiz sentence must be ORIGINAL. Never copy text from any book, workbook or website.
- Character names: a diverse mix (e.g. Maya, Leo, Priya, Sam, Aisha, Ben, Nora, Jai, Ella, Omar, Zoe, Ravi, Lily, Max, Ana, Theo, Kofi, Mei, Diego, Sara). No real people.

## story
- genre: string (as assigned)
- characters: array of 3 character name strings (as assigned)
- parts: array of exactly 4 objects, each with "title" (string) and "text" (string)
- Every single vocab word MUST appear EXACTLY ONCE in the story text, bolded as **word**
- Total wordCount across all 4 parts: see Age adjustments
- Age-appropriate for the set's grade (see Age adjustments)
- The story should make vocab word meanings clear from context
- wordCount: integer (actual word count)
- Part 4 wraps up the story without any vocab words — it's a reflection/conclusion

## definitions (array of 12)
Each object:
- "word": lowercase string
- "partOfSpeech": e.g. "noun", "verb", "adjective", "noun, verb", "adjective, verb"
- "meaning1": "Clear definition for a student in this grade. Example: A natural-sounding example sentence." (ALWAYS filled)
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
