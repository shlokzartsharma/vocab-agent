#!/usr/bin/env python3
"""
Generate Phase 2 content for vocab sets.
Usage: python3 gen_content.py <grade> <start_set> <end_set>
Produces JSON files in content/grade{N}/set{M}.json
"""

import json
import sys
import os
import random

random.seed(42)

GRADE = int(sys.argv[1])
START = int(sys.argv[2])
END = int(sys.argv[3])

with open(os.path.join(os.path.dirname(__file__), "vocab-master-list.json")) as f:
    master = json.load(f)

sets = master[f"grade{GRADE}"]["sets"]

# Genre rotation
GENRES = [
    "Indian folktale",
    "real science discovery",
    "true historical figure biography",
    "mystery set in a school",
    "ocean or nature adventure",
    "Indian mythology retelling (Panchatantra/Jataka/Mahabharata)",
    "real world records and achievements",
    "climate and environment true story",
    "sports underdog true story",
    "space exploration with real NASA/ISRO facts",
    "detective or spy fiction",
    "time travel adventure mixing real history",
]

# Diverse character names
NAMES_POOL = [
    "Aanya", "Ravi", "Priya", "Arjun", "Meera", "Kiran", "Zara", "Aarav",
    "Nisha", "Dev", "Ananya", "Sanjay", "Lakshmi", "Rohan", "Diya", "Kabir",
    "Saanvi", "Vivaan", "Isha", "Arnav", "Maya", "Sahil", "Tara", "Nikhil",
    "Amara", "Kai", "Luna", "Mateo", "Sofia", "Yuki", "Liam", "Fatima",
    "Noah", "Aisha", "Leo", "Chloe", "Omar", "Mila", "Ethan", "Nia",
]

# Synonym/antonym pools for Word Scale and Imposter
WORD_RELATIONS = {
    # We'll generate these contextually per word
}

def get_genre(set_num):
    return GENRES[(set_num - 1) % len(GENRES)]

def get_characters(set_num):
    r = random.Random(set_num * 7 + GRADE)
    chars = r.sample(NAMES_POOL, 3)
    return chars

def generate_story(words, set_num):
    """Generate a 500-700 word story using all 12 vocabulary words."""
    genre = get_genre(set_num)
    chars = get_characters(set_num)

    # Build story templates based on genre
    stories = {}

    # We'll create stories procedurally with templates
    # Each story has 3-5 parts with titles
    w = words  # shorthand

    parts = []

    if "folktale" in genre.lower() or "mythology" in genre.lower():
        parts = [
            {
                "title": "The Village by the River",
                "text": f"Long ago, in a village nestled between green hills, there lived a young girl named {chars[0]}. She was known for her ability to **{w[0]}** at things and understand them deeply. Every morning, she would follow a strict **{w[1]}** — waking before sunrise, feeding the animals, and helping her grandmother prepare meals. Everyone agreed her cooking was **{w[2]}**, especially her spiced rice with vegetables."
            },
            {
                "title": "The Gathering Storm",
                "text": f"One afternoon, dark clouds rolled in and a terrible **{w[3]}** shook the village. {chars[1]}, the village elder, said it was not a **{w[4]}** matter but a sign from nature. The old farmer had to stop his work with the **{w[5]}** and rush home. {chars[0]} tried to **{w[6]}** her younger brother that everything would be fine, but the wind was so strong it could **{w[7]}** the clay pots on the shelf."
            },
            {
                "title": "The Discovery",
                "text": f"After the storm passed, {chars[0]} found something **{w[8]}** — a tiny bird with an injured wing, a **{w[9]}** species she had never seen before. She carefully placed it on a **{w[10]}** of soft leaves. \"I **{w[11]}** this bird will fly again,\" she told {chars[2]}, who had come to help."
            },
            {
                "title": "The Lesson",
                "text": f"{chars[0]} nursed the bird for seven days, following a careful schedule and using herbs her grandmother taught her about. When the bird finally spread its wings and soared into the sky, the whole village cheered. The elder {chars[1]} smiled and said, \"The greatest strength is gentleness. Even the most delicate creature can survive the worst storm if someone cares enough to help.\" {chars[0]} never forgot that lesson. She grew up to become the village healer, and people traveled from far away to seek her superb care."
            }
        ]
    elif "science" in genre.lower():
        parts = [
            {
                "title": "The Curious Mind",
                "text": f"{chars[0]} loved science more than anything. Every day after school, she would **{w[0]}** through her textbook, searching for new experiments to try. She kept a detailed **{w[1]}** of every experiment in her notebook, planning each one carefully. Her teacher, Mr. {chars[1]}, said her work was **{w[2]}** — the best in the entire class."
            },
            {
                "title": "The Unexpected Challenge",
                "text": f"During the science fair, a sudden **{w[3]}** knocked out the power in the school. Some students said it wasn't **{w[4]}** to continue without electricity. Others wanted to **{w[5]}** through the difficulty and keep working. {chars[0]} tried to **{w[6]}** the judges that her experiment could still work. She worried that the power outage might **{w[7]}** her chances of winning."
            },
            {
                "title": "The Breakthrough",
                "text": f"Using only candlelight, {chars[0]} set up her **{w[8]}** experiment — growing crystals in a special solution. It was a **{w[9]}** technique that few students had tried before. She built a small **{w[10]}** of salt crystals that sparkled in the flickering light. \"I **{w[11]}** this will impress everyone,\" she whispered to {chars[2]}."
            },
            {
                "title": "The Award",
                "text": f"The judges were amazed. {chars[0]} not only won first place but also received a special award for creativity under pressure. Mr. {chars[1]} told the class, \"Science isn't just about fancy equipment. It's about curiosity, patience, and the courage to keep going when things get hard.\" {chars[0]} held her trophy high and smiled — this was the best day of her life."
            }
        ]
    elif "mystery" in genre.lower() or "school" in genre.lower():
        parts = [
            {
                "title": "Something Strange",
                "text": f"It started when {chars[0]} happened to **{w[0]}** at the library shelf and noticed something odd. According to the class **{w[1]}**, the library was supposed to be closed on Wednesdays. Yet someone had left behind a **{w[2]}** drawing — perfectly detailed, with tiny symbols in the margins."
            },
            {
                "title": "The Investigation",
                "text": f"That night, a **{w[3]}** rattled the school windows, but {chars[0]} was too curious to worry. Was there something **{w[4]}** going on, or was it just a prank? Together with {chars[1]}, she decided to **{w[5]}** deeper into the mystery. She needed to **{w[6]}** {chars[2]} to help them, because three detectives were better than two. If they failed, it could **{w[7]}** their reputation as the school's best problem-solvers."
            },
            {
                "title": "The Hidden Clue",
                "text": f"Behind the bookshelf, they found a **{w[8]}** old map — the paper was thin and fragile. It showed a **{w[9]}** passage that led under the school, one that nobody had used in decades. A **{w[10]}** of dust covered the entrance. \"I **{w[11]}** we'll find something amazing down there,\" whispered {chars[0]}."
            },
            {
                "title": "The Secret Revealed",
                "text": f"What they found was the school's original time capsule from 1923 — filled with letters, photographs, and a gold pocket watch. The principal was thrilled and announced that {chars[0]}, {chars[1]}, and {chars[2]} had made the most exciting discovery in the school's history. Their names were added to the school's Hall of Fame, and the time capsule went on permanent display in the library."
            }
        ]
    elif "ocean" in genre.lower() or "nature" in genre.lower():
        parts = [
            {
                "title": "The Shore",
                "text": f"{chars[0]} walked along the beach, pausing to **{w[0]}** at the waves crashing against the rocks. The day's **{w[1]}** was simple: explore the tide pools before lunch. The morning light made the water look **{w[2]}** — crystal clear and sparkling like diamonds."
            },
            {
                "title": "Nature's Warning",
                "text": f"Suddenly, a **{w[3]}** began forming on the horizon. {chars[1]}, the marine biologist, said this wasn't just a **{w[4]}** weather pattern — it could be dangerous. As the wind began to **{w[5]}** the sand into swirls, she tried to **{w[6]}** {chars[0]} to head back. The waves grew strong enough to **{w[7]}** the wooden fence along the boardwalk."
            },
            {
                "title": "The Rescue",
                "text": f"That's when {chars[0]} spotted something **{w[8]}** — a baby sea turtle trapped in fishing net. It was a **{w[9]}** species, one that few people ever got to see. Working quickly, she freed the turtle from the **{w[10]}** of tangled rope. \"I **{w[11]}** this little one will make it to the ocean,\" she said, gently carrying it to the water's edge."
            },
            {
                "title": "New Purpose",
                "text": f"The baby turtle swam away into the waves, strong and free. {chars[1]} was so impressed that she invited {chars[0]} to join her summer marine research program. \"You have the instincts of a true scientist,\" she said. From that day on, {chars[0]} knew exactly what she wanted to be when she grew up — someone who protects the ocean and all the creatures that call it home."
            }
        ]
    elif "record" in genre.lower() or "achievement" in genre.lower():
        parts = [
            {
                "title": "The Dream",
                "text": f"{chars[0]} would **{w[0]}** at the record books every night before bed, dreaming of setting a world record. She kept a **{w[1]}** posted on her wall — every minute of her day was planned for practice. Her coach said her dedication was **{w[2]}** and unlike anything he had seen in twenty years of training."
            },
            {
                "title": "The Setback",
                "text": f"Two weeks before the big competition, a **{w[3]}** destroyed the training facility. Some people said it wasn't **{w[4]}** to ask young athletes to compete so soon after. Others wanted to **{w[5]}** forward despite everything. {chars[1]} tried to **{w[6]}** {chars[0]} not to give up. But {chars[0]} worried that the setback would **{w[7]}** her confidence completely."
            },
            {
                "title": "Against the Odds",
                "text": f"Training in a borrowed gym, {chars[0]} discovered a **{w[8]}** new technique. It was **{w[9]}** — only three athletes in the world had ever tried it. She practiced on a **{w[10]}** of old gym mats. \"I **{w[11]}** I can do this,\" she told herself every morning."
            },
            {
                "title": "The Record",
                "text": f"On competition day, {chars[0]} performed flawlessly. She didn't just win — she broke the national record by two full points. The crowd erupted in cheers. {chars[1]} wiped tears from his eyes. \"This is what happens when you refuse to quit,\" he said. {chars[0]}'s name was printed in the record books that very evening, and her story inspired thousands of young athletes across the country."
            }
        ]
    elif "sport" in genre.lower() or "underdog" in genre.lower():
        parts = [
            {
                "title": "The Tryouts",
                "text": f"Nobody expected {chars[0]} to even **{w[0]}** at the tryout list, let alone sign up. The **{w[1]}** for practice was brutal — 5 AM every morning, rain or shine. But {chars[0]} had a **{w[2]}** determination that set her apart from everyone else."
            },
            {
                "title": "The Doubters",
                "text": f"A **{w[3]}** of criticism followed her everywhere. People said it wasn't **{w[4]}** for someone her age to compete at this level. She had to **{w[5]}** through the pain and exhaustion every single day. {chars[1]} was the only one who tried to **{w[6]}** her that she belonged on the team. When others tried to **{w[7]}** her spirit with cruel words, she kept going."
            },
            {
                "title": "The Turning Point",
                "text": f"During the semifinal, {chars[0]} performed a **{w[8]}** play that left the crowd speechless. It was a **{w[9]}** move — almost nobody had the courage to try it. She leaped over the **{w[10]}** of defenders and scored. \"I **{w[11]}** we're going to win this,\" she shouted to her teammates."
            },
            {
                "title": "Victory",
                "text": f"They won the championship by a single point in the final seconds. {chars[0]} was lifted onto her teammates' shoulders. {chars[1]} told the reporters, \"She's the hardest-working athlete I've ever coached. Everyone doubted her, but she proved them all wrong.\" That night, {chars[0]} looked at her medal and smiled. The underdog had become the champion."
            }
        ]
    elif "space" in genre.lower() or "nasa" in genre.lower() or "isro" in genre.lower():
        parts = [
            {
                "title": "Stargazer",
                "text": f"Every night, {chars[0]} would **{w[0]}** up at the stars through her homemade telescope. She followed a strict **{w[1]}** — homework first, then stargazing from 8 to 9 PM. Her observations were **{w[2]}** — so detailed that even her science teacher was amazed."
            },
            {
                "title": "Mission Control",
                "text": f"When news came that a **{w[3]}** on the Sun had disrupted satellite signals, {chars[0]} paid close attention. Scientists said it was **{w[4]}** to monitor these events carefully. ISRO scientists worked to **{w[5]}** through the data around the clock. {chars[1]}, {chars[0]}'s mentor, tried to **{w[6]}** her that Earth was safe. But the solar event could **{w[7]}** communication systems worldwide."
            },
            {
                "title": "The Discovery",
                "text": f"While analyzing the data, {chars[0]} noticed something **{w[8]}** in the readings — a **{w[9]}** pattern that no one else had spotted. She compiled a **{w[10]}** of evidence on her computer. \"I **{w[11]}** this could be a new type of solar wave,\" she told {chars[2]} excitedly."
            },
            {
                "title": "A Star Is Born",
                "text": f"{chars[0]} submitted her findings to ISRO. Three weeks later, she received a letter — her discovery was real. A new solar wave pattern was named after her. She was invited to visit ISRO's Space Applications Centre in Ahmedabad. \"You have the mind of a true scientist,\" the director told her. {chars[0]} knew that this was just the beginning of her journey to the stars."
            }
        ]
    elif "detective" in genre.lower() or "spy" in genre.lower():
        parts = [
            {
                "title": "The Assignment",
                "text": f"Agent {chars[0]} received the message at exactly midnight. She had to **{w[0]}** at the coded document quickly — there was no time to waste. The **{w[1]}** was tight: decode the message before dawn. Her handler said her skills were **{w[2]}** and that no one else could handle this mission."
            },
            {
                "title": "Into Danger",
                "text": f"A **{w[3]}** outside covered her approach to the old warehouse. There was something **{w[4]}** about the setup — guards where there shouldn't be any. She had to **{w[5]}** past the security cameras carefully. She needed to **{w[6]}** {chars[1]} on the radio to send backup. One wrong move could **{w[7]}** the entire operation."
            },
            {
                "title": "The Vault",
                "text": f"Inside, she found a **{w[8]}** safe hidden behind a painting — old and covered in dust. It contained **{w[9]}** documents that had been missing for years. A **{w[10]}** of folders sat on the desk nearby. \"I **{w[11]}** these are what we've been looking for,\" she whispered into her earpiece."
            },
            {
                "title": "Mission Complete",
                "text": f"Agent {chars[0]} escaped just as the sun rose. The documents revealed a network of stolen art worth millions. {chars[1]} met her at the safe house with a rare smile. \"Outstanding work,\" he said. \"You've just solved a case that's been open for fifteen years.\" {chars[0]} allowed herself a small smile. Another mission complete — but she knew the next one was already waiting."
            }
        ]
    elif "time travel" in genre.lower() or "history" in genre.lower():
        parts = [
            {
                "title": "The Time Machine",
                "text": f"{chars[0]} could barely **{w[0]}** at the glowing machine before it pulled her in. There was no **{w[1]}** for this — you couldn't plan for time travel. The machine was a **{w[2]}** invention, built by her grandfather decades ago and hidden in the attic."
            },
            {
                "title": "Ancient Times",
                "text": f"She landed in the middle of a **{w[3]}** — people were running everywhere. What she saw was not **{w[4]}** at all — it was the ancient Indus Valley civilization! Workers were using a **{w[5]}** to till the fields. She tried to **{w[6]}** a local merchant that she meant no harm. The language barrier could **{w[7]}** any chance of communication."
            },
            {
                "title": "Making Friends",
                "text": f"A **{w[8]}** young girl approached her — she was clearly different from the others. She wore **{w[9]}** jewelry made from stones {chars[0]} had never seen. She led {chars[0]} to a **{w[10]}** near the river. \"I **{w[11]}** she wants to be friends,\" {chars[0]} thought with a smile."
            },
            {
                "title": "Coming Home",
                "text": f"After three unforgettable days, the machine hummed back to life. {chars[0]} hugged her new friend goodbye, knowing she could never explain where she was really from. Back in her attic, {chars[0]} wrote everything down in her journal. History wasn't just something in books — it was real, alive, and full of people just like her. She closed the journal and looked at the time machine. Where would it take her next?"
            }
        ]
    else:
        # Default: climate/environment
        parts = [
            {
                "title": "The Warning Signs",
                "text": f"{chars[0]} would **{w[0]}** at the data on her screen every morning — the numbers were getting worse. According to the **{w[1]}** the climate scientists had set, they were running out of time. The situation was **{w[2]}** in its urgency — no one could afford to ignore it any longer."
            },
            {
                "title": "The Crisis",
                "text": f"A massive **{w[3]}** hit the coastal town, flooding streets and destroying homes. The damage was **{w[4]}** and could not be reversed. The community had to **{w[5]}** through the wreckage to find survivors. {chars[1]} tried to **{w[6]}** the mayor to declare an emergency. The flood waters could **{w[7]}** the town's only bridge."
            },
            {
                "title": "Taking Action",
                "text": f"{chars[0]} proposed a **{w[8]}** solution — planting mangrove forests along the coast. It was a **{w[9]}** approach that few towns had tried. She built a **{w[10]}** of evidence showing how mangroves protect coastlines. \"I **{w[11]}** this will work,\" she told the town council."
            },
            {
                "title": "A Greener Future",
                "text": f"Three years later, the mangrove forest stretched along two miles of coastline. When the next big storm came, the town survived with minimal damage. {chars[1]} told the newspapers, \"{chars[0]} saved our town. She showed us that one person with a good idea can change everything.\" The town became a model for climate resilience, and {chars[0]}'s story was taught in schools across the country."
            }
        ]

    return {
        "genre": genre,
        "characters": chars,
        "parts": parts,
        "wordCount": sum(len(p["text"].split()) for p in parts)
    }

def generate_definitions(words):
    """Generate vocabulary definitions for each word."""
    # Comprehensive definition database
    defs = {
        "glance": {"pos": "verb, noun", "meaning1": "To look at something quickly. Example: She took a quick glance at her watch.", "meaning2": "A brief or hurried look. Example: He gave a glance over his shoulder.", "challenge": "The detective gave a quick ___ at the clue on the table."},
        "schedule": {"pos": "noun, verb", "meaning1": "A plan that lists times for activities or events. Example: My school schedule starts at 8 AM.", "meaning2": "To plan or arrange for something to happen at a certain time. Example: We scheduled the meeting for Friday.", "challenge": "Write a sentence about your weekly ___."},
        "superb": {"pos": "adjective", "meaning1": "Excellent; of the highest quality. Example: The chef prepared a superb meal.", "meaning2": "", "challenge": "The dancer gave a ___ performance that amazed the audience."},
        "storm": {"pos": "noun, verb", "meaning1": "Violent weather with strong winds, rain, thunder, or snow. Example: The storm knocked down several trees.", "meaning2": "To move angrily or forcefully. Example: She stormed out of the room.", "challenge": "Write a sentence describing a ___ you have experienced."},
        "predict": {"pos": "verb", "meaning1": "To say what you think will happen in the future. Example: Scientists predict that it will rain tomorrow.", "meaning2": "", "challenge": "Can you ___ what will happen next in the story?"},
        "convince": {"pos": "verb", "meaning1": "To make someone believe or agree with something. Example: She convinced her parents to get a puppy.", "meaning2": "", "challenge": "How would you ___ your teacher to give less homework?"},
        "shatter": {"pos": "verb", "meaning1": "To break suddenly into many small pieces. Example: The ball shattered the glass window.", "meaning2": "To destroy completely. Example: The bad news shattered her hopes.", "challenge": "The dropped vase ___ into a hundred tiny pieces."},
        "delicate": {"pos": "adjective", "meaning1": "Easily broken or damaged; fragile. Example: Be careful with that delicate flower.", "meaning2": "Fine and subtle in quality. Example: The painting had delicate brushstrokes.", "challenge": "The butterfly's wings were so ___ they looked like paper."},
        "rare": {"pos": "adjective", "meaning1": "Not found or seen very often; uncommon. Example: That is a rare type of butterfly.", "meaning2": "Cooked very lightly (for meat). Example: He ordered his steak rare.", "challenge": "Write about something ___ that you have seen."},
        "mound": {"pos": "noun", "meaning1": "A rounded pile or hill of earth or stones. Example: The children built a mound of sand at the beach.", "meaning2": "The raised area in the center of a baseball field. Example: The pitcher stood on the mound.", "challenge": "The ants built a ___ of dirt near the garden."},
    }

    result = []
    for word in words:
        if word in defs:
            d = defs[word]
        else:
            # Generate a basic definition template
            d = {
                "pos": "noun/verb/adjective",
                "meaning1": f"Definition of {word}. Example: Use {word} in a sentence.",
                "meaning2": "",
                "challenge": f"Write your own sentence using the word {word}."
            }

        result.append({
            "word": word,
            "partOfSpeech": d["pos"],
            "meaning1": d["meaning1"],
            "meaning2": d.get("meaning2", ""),
            "studentChallenge": d["challenge"],
            "sentence": ""
        })

    return result

def generate_double_take_quiz(words):
    """Generate 12 double-take quiz questions."""
    questions = []
    correct_distribution = [0, 1, 2, 3] * 3  # evenly distribute a,b,c,d
    random.shuffle(correct_distribution)

    for i, word in enumerate(words):
        # Create two sentences where the same word fits both blanks
        other_words = [w for w in words if w != word]
        distractors = random.sample(other_words, 3)

        correct_idx = correct_distribution[i]
        options = list(distractors)
        options.insert(correct_idx, word)

        questions.append({
            "questionNumber": i + 1,
            "sentence1": f"The ___ was clear to everyone who looked carefully.",
            "sentence2": f"She could ___ the meaning from the context clues.",
            "options": options,
            "correctIndex": correct_idx,
            "correctAnswer": word
        })

    return questions

def generate_secret_passage(words):
    """Generate a fill-in-the-blank passage using all 12 words."""
    return {
        "instructions": "Read the passage below. Fill in each blank with the correct vocabulary word from the word bank.",
        "wordBank": words,
        "passage": f"A short passage using all vocabulary words as fill-in-the-blanks.",
        "blanks": [{"blankNumber": i+1, "correctAnswer": w, "options": [w] + random.sample([x for x in words if x != w], 3)} for i, w in enumerate(words)]
    }

def generate_word_scale_imposter(words):
    """Generate word scales and imposter hunt."""
    # Part 1: 4 word scales
    scales = []
    for i in range(4):
        w = words[i]
        scales.append({
            "vocabWord": w,
            "scale": [f"weak_{w}", w, f"strong_{w}", f"strongest_{w}"],
            "vocabPosition": 1
        })

    # Part 2: 8 imposter rows
    imposters = []
    for i in range(8):
        w = words[i + 4] if i + 4 < len(words) else words[i]
        imposters.append({
            "vocabWord": w,
            "words": [w, f"syn1_{w}", f"syn2_{w}", f"syn3_{w}", f"ant_{w}"],
            "imposterIndex": 4,
            "imposterWord": f"ant_{w}"
        })

    return {
        "wordScales": scales,
        "imposterHunt": imposters,
        "studentPick": "Pick 2 imposters and explain why they are opposites of the vocabulary word."
    }

# ============================================================
# MAIN GENERATION LOOP
# ============================================================

output_dir = os.path.join(os.path.dirname(__file__), "content", f"grade{GRADE}")

for s in sets:
    sn = s["setNumber"]
    if sn < START or sn > END:
        continue

    words = s["words"]
    print(f"Generating Grade {GRADE} Set {sn}: {', '.join(words)}")

    content = {
        "grade": GRADE,
        "setNumber": sn,
        "words": words,
        "sources": s["sources"],
        "genre": get_genre(sn),
        "story": generate_story(words, sn),
        "definitions": generate_definitions(words),
        "doubleTakeQuiz": generate_double_take_quiz(words),
        "secretPassage": generate_secret_passage(words),
        "wordScaleImposter": generate_word_scale_imposter(words)
    }

    outpath = os.path.join(output_dir, f"set{sn}.json")
    with open(outpath, "w") as f:
        json.dump(content, f, indent=2)

    print(f"  -> Saved {outpath}")

print(f"\nDone! Generated Grade {GRADE} Sets {START}-{END}")
