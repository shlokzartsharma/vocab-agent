import json

with open("/Users/suchitrasharma/vocab-agent/vocab-master-list.json") as f:
    data = json.load(f)

lines = []
lines.append("# Vocab Agent — Master Word List")
lines.append("")
lines.append(f"**Total unique words: {data['totalUniqueWords']}**")
lines.append("")

for grade in [3, 4, 5]:
    g = data[f"grade{grade}"]
    lines.append(f"## Grade {grade} — {g['totalWords']} words in {g['totalSets']} sets")
    lines.append("")
    for s in g["sets"]:
        words = ", ".join(s["words"])
        sources = ", ".join(s["sources"])
        lines.append(f"### Set {s['setNumber']}")
        lines.append(f"**Words:** {words}")
        lines.append(f"**Sources:** {sources}")
        lines.append("")

with open("/Users/suchitrasharma/vocab-agent/vocab-master-list.md", "w") as f:
    f.write("\n".join(lines))

print("Markdown file written successfully")
print(f"Grade 3: {data['grade3']['totalWords']} words, {data['grade3']['totalSets']} sets")
print(f"Grade 4: {data['grade4']['totalWords']} words, {data['grade4']['totalSets']} sets")
print(f"Grade 5: {data['grade5']['totalWords']} words, {data['grade5']['totalSets']} sets")
print(f"Total: {data['totalUniqueWords']} words")
