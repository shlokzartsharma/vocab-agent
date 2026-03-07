#!/usr/bin/env python3
"""Apply 1,034 extra word definitions to all content JSON files."""
import json, glob, os

# Load the definitions
with open('extra_defs.json') as f:
    DEFS = json.load(f)

print(f"Loaded {len(DEFS)} definitions from extra_defs.json")

total_updated = 0
total_skipped = 0
total_already = 0

for fpath in sorted(glob.glob('content/grade*/set*.json')):
    with open(fpath) as f:
        data = json.load(f)

    changed = False
    for defn in data.get('definitions', []):
        word = defn['word'].lower()

        # Skip if already has a real definition
        if not defn['meaning1'].startswith('Definition of '):
            total_already += 1
            continue

        if word not in DEFS:
            total_skipped += 1
            continue

        d = DEFS[word]
        defn['partOfSpeech'] = d['pos']
        defn['meaning1'] = d['m1']
        defn['meaning2'] = d.get('m2', '')
        defn['studentChallenge'] = d['ch']
        changed = True
        total_updated += 1

    if changed:
        with open(fpath, 'w') as f:
            json.dump(data, f, indent=2)

print(f"Updated: {total_updated}")
print(f"Already defined: {total_already}")
print(f"Skipped (no def found): {total_skipped}")
print(f"Total processed: {total_updated + total_already + total_skipped}")
