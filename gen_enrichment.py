#!/usr/bin/env python3
"""
Enrich all content files with:
1. Proper double-take quiz sentences (extracted from definitions)
2. Real secret passages (generated from templates)
3. Real word scales (intensity gradients)
4. Real imposter hunts (synonyms + antonym imposter)
"""

import json
import os
import random
import re

random.seed(42)

# ============================================================
# SYNONYMS & ANTONYMS DATABASE
# Load from extra_word_data.json + inline fallbacks
# ============================================================

# Load the compiled word data from JSON
_EXTRA_DATA_PATH = os.path.join(os.path.dirname(__file__), "extra_word_data.json")
if os.path.exists(_EXTRA_DATA_PATH):
    with open(_EXTRA_DATA_PATH) as _f:
        WORD_DATA = json.load(_f)
else:
    WORD_DATA = {}

# Also keep inline data as fallback/supplement
_INLINE_DATA = {
    "abandon": {"syns": ["desert", "leave", "forsake"], "ant": "keep", "scale": ["leave", "abandon", "forsake", "desert"]},
    "ability": {"syns": ["skill", "talent", "capability"], "ant": "inability", "scale": ["knack", "ability", "talent", "mastery"]},
    "abolish": {"syns": ["eliminate", "end", "remove"], "ant": "establish", "scale": ["reduce", "abolish", "eradicate", "annihilate"]},
    "abroad": {"syns": ["overseas", "away", "foreign"], "ant": "home", "scale": ["away", "abroad", "overseas", "distant"]},
    "absorb": {"syns": ["soak", "take in", "engross"], "ant": "release", "scale": ["dampen", "absorb", "soak up", "engulf"]},
    "abstract": {"syns": ["theoretical", "conceptual", "intangible"], "ant": "concrete", "scale": ["vague", "abstract", "conceptual", "incomprehensible"]},
    "abundance": {"syns": ["plenty", "wealth", "surplus"], "ant": "scarcity", "scale": ["enough", "abundance", "surplus", "overflow"]},
    "abundant": {"syns": ["plentiful", "ample", "rich"], "ant": "scarce", "scale": ["sufficient", "abundant", "plentiful", "overflowing"]},
    "abuse": {"syns": ["mistreat", "harm", "exploit"], "ant": "respect", "scale": ["misuse", "abuse", "exploit", "torment"]},
    "accelerate": {"syns": ["speed up", "quicken", "hasten"], "ant": "slow down", "scale": ["increase", "accelerate", "rush", "rocket"]},
    "access": {"syns": ["entry", "admission", "approach"], "ant": "restriction", "scale": ["approach", "access", "entry", "freedom"]},
    "accident": {"syns": ["mishap", "incident", "misfortune"], "ant": "intention", "scale": ["slip", "accident", "mishap", "catastrophe"]},
    "accommodate": {"syns": ["house", "fit", "adjust"], "ant": "reject", "scale": ["fit", "accommodate", "house", "shelter"]},
    "accompany": {"syns": ["escort", "join", "follow"], "ant": "abandon", "scale": ["follow", "accompany", "escort", "guide"]},
    "accomplish": {"syns": ["achieve", "complete", "finish"], "ant": "fail", "scale": ["attempt", "accomplish", "achieve", "triumph"]},
    "accurate": {"syns": ["correct", "exact", "precise"], "ant": "inaccurate", "scale": ["close", "accurate", "exact", "precise"]},
    "accuse": {"syns": ["blame", "charge", "allege"], "ant": "defend", "scale": ["suspect", "accuse", "charge", "condemn"]},
    "achieve": {"syns": ["accomplish", "attain", "reach"], "ant": "fail", "scale": ["try", "achieve", "accomplish", "conquer"]},
    "achievement": {"syns": ["accomplishment", "success", "feat"], "ant": "failure", "scale": ["effort", "achievement", "feat", "triumph"]},
    "acknowledge": {"syns": ["admit", "accept", "recognize"], "ant": "deny", "scale": ["notice", "acknowledge", "accept", "embrace"]},
    "acquire": {"syns": ["obtain", "gain", "get"], "ant": "lose", "scale": ["find", "acquire", "obtain", "amass"]},
    "active": {"syns": ["energetic", "lively", "busy"], "ant": "inactive", "scale": ["moving", "active", "energetic", "tireless"]},
    "actual": {"syns": ["real", "true", "genuine"], "ant": "imaginary", "scale": ["possible", "actual", "real", "undeniable"]},
    "adapt": {"syns": ["adjust", "change", "modify"], "ant": "resist", "scale": ["cope", "adapt", "adjust", "transform"]},
    "adaptation": {"syns": ["adjustment", "change", "modification"], "ant": "rigidity", "scale": ["change", "adaptation", "transformation", "evolution"]},
    "adequate": {"syns": ["enough", "sufficient", "acceptable"], "ant": "inadequate", "scale": ["minimal", "adequate", "sufficient", "ample"]},
    "adhesive": {"syns": ["glue", "paste", "sticker"], "ant": "separator", "scale": ["tape", "adhesive", "glue", "cement"]},
    "adjust": {"syns": ["change", "modify", "adapt"], "ant": "fix", "scale": ["tweak", "adjust", "modify", "overhaul"]},
    "admire": {"syns": ["respect", "appreciate", "look up to"], "ant": "despise", "scale": ["like", "admire", "revere", "worship"]},
    "adopt": {"syns": ["embrace", "take on", "accept"], "ant": "reject", "scale": ["consider", "adopt", "embrace", "champion"]},
    "advantage": {"syns": ["benefit", "edge", "gain"], "ant": "disadvantage", "scale": ["help", "advantage", "edge", "dominance"]},
    "adventure": {"syns": ["journey", "quest", "expedition"], "ant": "routine", "scale": ["trip", "adventure", "expedition", "odyssey"]},
    "adversary": {"syns": ["opponent", "rival", "enemy"], "ant": "ally", "scale": ["rival", "adversary", "enemy", "nemesis"]},
    "advice": {"syns": ["guidance", "suggestion", "counsel"], "ant": "silence", "scale": ["hint", "advice", "guidance", "counsel"]},
    "affect": {"syns": ["influence", "change", "impact"], "ant": "ignore", "scale": ["touch", "affect", "influence", "transform"]},
    "afford": {"syns": ["manage", "provide", "spare"], "ant": "lack", "scale": ["manage", "afford", "provide", "lavish"]},
    "aggressive": {"syns": ["hostile", "forceful", "fierce"], "ant": "gentle", "scale": ["assertive", "aggressive", "hostile", "violent"]},
    "aggravate": {"syns": ["worsen", "irritate", "annoy"], "ant": "soothe", "scale": ["bother", "aggravate", "infuriate", "enrage"]},
    "ail": {"syns": ["trouble", "bother", "afflict"], "ant": "heal", "scale": ["bother", "ail", "afflict", "torment"]},
    "aim": {"syns": ["goal", "target", "purpose"], "ant": "miss", "scale": ["try", "aim", "target", "zero in"]},
    "aimless": {"syns": ["directionless", "purposeless", "wandering"], "ant": "purposeful", "scale": ["casual", "aimless", "lost", "hopeless"]},
    "alarmed": {"syns": ["frightened", "worried", "startled"], "ant": "calm", "scale": ["concerned", "alarmed", "frightened", "terrified"]},
    "alert": {"syns": ["watchful", "attentive", "aware"], "ant": "unaware", "scale": ["awake", "alert", "vigilant", "hyperaware"]},
    "alleviate": {"syns": ["ease", "relieve", "reduce"], "ant": "worsen", "scale": ["ease", "alleviate", "relieve", "eliminate"]},
    "allot": {"syns": ["assign", "distribute", "allocate"], "ant": "withhold", "scale": ["give", "allot", "distribute", "allocate"]},
    "allow": {"syns": ["permit", "let", "approve"], "ant": "forbid", "scale": ["tolerate", "allow", "permit", "encourage"]},
    "alter": {"syns": ["change", "modify", "adjust"], "ant": "preserve", "scale": ["tweak", "alter", "transform", "revolutionize"]},
    "alternate": {"syns": ["switch", "rotate", "take turns"], "ant": "remain", "scale": ["switch", "alternate", "rotate", "cycle"]},
    "alternative": {"syns": ["option", "choice", "substitute"], "ant": "original", "scale": ["option", "alternative", "substitute", "replacement"]},
    "altitude": {"syns": ["height", "elevation", "level"], "ant": "depth", "scale": ["height", "altitude", "elevation", "summit"]},
    "amateur": {"syns": ["beginner", "novice", "hobbyist"], "ant": "professional", "scale": ["beginner", "amateur", "intermediate", "expert"]},
    "ambiguous": {"syns": ["unclear", "vague", "confusing"], "ant": "clear", "scale": ["unclear", "ambiguous", "confusing", "incomprehensible"]},
    "ambition": {"syns": ["drive", "goal", "determination"], "ant": "laziness", "scale": ["wish", "ambition", "drive", "obsession"]},
    "ambulance": {"syns": ["rescue vehicle", "emergency van", "paramedic unit"], "ant": "hearse", "scale": ["car", "ambulance", "rescue vehicle", "emergency unit"]},
    "amendment": {"syns": ["change", "revision", "correction"], "ant": "original", "scale": ["tweak", "amendment", "revision", "overhaul"]},
    "amount": {"syns": ["quantity", "total", "sum"], "ant": "none", "scale": ["bit", "amount", "quantity", "abundance"]},
    "ample": {"syns": ["plenty", "enough", "sufficient"], "ant": "insufficient", "scale": ["enough", "ample", "abundant", "overflowing"]},
    "analyze": {"syns": ["examine", "study", "investigate"], "ant": "ignore", "scale": ["look at", "analyze", "examine", "dissect"]},
    "ancestor": {"syns": ["forefather", "predecessor", "forebear"], "ant": "descendant", "scale": ["parent", "ancestor", "forefather", "origin"]},
    "ancient": {"syns": ["old", "historic", "antique"], "ant": "modern", "scale": ["old", "ancient", "prehistoric", "primordial"]},
    "anchor": {"syns": ["secure", "fasten", "hold"], "ant": "release", "scale": ["hold", "anchor", "secure", "cement"]},
    "anecdote": {"syns": ["story", "tale", "account"], "ant": "report", "scale": ["remark", "anecdote", "tale", "saga"]},
    "animate": {"syns": ["enliven", "energize", "inspire"], "ant": "deaden", "scale": ["stir", "animate", "enliven", "electrify"]},
    "announce": {"syns": ["declare", "proclaim", "reveal"], "ant": "conceal", "scale": ["mention", "announce", "declare", "proclaim"]},
    "annual": {"syns": ["yearly", "regular", "seasonal"], "ant": "rare", "scale": ["occasional", "annual", "regular", "constant"]},
    "anonymous": {"syns": ["unnamed", "unknown", "nameless"], "ant": "identified", "scale": ["unnamed", "anonymous", "mysterious", "invisible"]},
    "anthem": {"syns": ["song", "hymn", "chant"], "ant": "silence", "scale": ["tune", "anthem", "hymn", "symphony"]},
    "anticipate": {"syns": ["expect", "predict", "foresee"], "ant": "doubt", "scale": ["guess", "anticipate", "expect", "foresee"]},
    "anxious": {"syns": ["worried", "nervous", "uneasy"], "ant": "calm", "scale": ["uneasy", "anxious", "worried", "panicked"]},
    "apparent": {"syns": ["obvious", "clear", "evident"], "ant": "hidden", "scale": ["noticeable", "apparent", "obvious", "unmistakable"]},
    "apparatus": {"syns": ["equipment", "device", "tool"], "ant": "nothing", "scale": ["tool", "apparatus", "equipment", "machinery"]},
    "appeal": {"syns": ["request", "attract", "plead"], "ant": "repel", "scale": ["ask", "appeal", "plead", "beg"]},
    "appear": {"syns": ["show", "emerge", "surface"], "ant": "disappear", "scale": ["peek", "appear", "emerge", "materialize"]},
    "appreciate": {"syns": ["value", "enjoy", "be grateful"], "ant": "disregard", "scale": ["notice", "appreciate", "value", "cherish"]},
    "apprehensive": {"syns": ["nervous", "worried", "fearful"], "ant": "confident", "scale": ["uneasy", "apprehensive", "fearful", "terrified"]},
    "approach": {"syns": ["near", "advance", "come close"], "ant": "retreat", "scale": ["move", "approach", "advance", "converge"]},
    "approached": {"syns": ["neared", "advanced", "came close"], "ant": "retreated", "scale": ["moved", "approached", "advanced", "arrived"]},
    "appropriate": {"syns": ["suitable", "proper", "fitting"], "ant": "inappropriate", "scale": ["acceptable", "appropriate", "ideal", "perfect"]},
    "approval": {"syns": ["consent", "agreement", "permission"], "ant": "rejection", "scale": ["acceptance", "approval", "endorsement", "praise"]},
    "approve": {"syns": ["accept", "agree", "support"], "ant": "reject", "scale": ["accept", "approve", "endorse", "champion"]},
    "approximate": {"syns": ["close", "rough", "estimated"], "ant": "exact", "scale": ["rough", "approximate", "close", "nearly exact"]},
    "arctic": {"syns": ["frozen", "icy", "frigid"], "ant": "tropical", "scale": ["cold", "arctic", "frigid", "glacial"]},
    "arena": {"syns": ["stadium", "field", "ring"], "ant": "sideline", "scale": ["court", "arena", "stadium", "colosseum"]},
    "argue": {"syns": ["debate", "disagree", "dispute"], "ant": "agree", "scale": ["disagree", "argue", "dispute", "fight"]},
    "argued": {"syns": ["debated", "disputed", "disagreed"], "ant": "agreed", "scale": ["disagreed", "argued", "disputed", "fought"]},
    "argument": {"syns": ["disagreement", "debate", "dispute"], "ant": "agreement", "scale": ["discussion", "argument", "quarrel", "fight"]},
    "aroma": {"syns": ["smell", "scent", "fragrance"], "ant": "stench", "scale": ["smell", "aroma", "fragrance", "perfume"]},
    "arrange": {"syns": ["organize", "sort", "order"], "ant": "scatter", "scale": ["sort", "arrange", "organize", "systematize"]},
    "arrest": {"syns": ["capture", "detain", "seize"], "ant": "release", "scale": ["stop", "arrest", "detain", "imprison"]},
    "arrive": {"syns": ["reach", "come", "appear"], "ant": "depart", "scale": ["come", "arrive", "reach", "land"]},
    "ascend": {"syns": ["climb", "rise", "go up"], "ant": "descend", "scale": ["step up", "ascend", "climb", "soar"]},
    "assembly": {"syns": ["gathering", "meeting", "group"], "ant": "dispersal", "scale": ["group", "assembly", "gathering", "convention"]},
    "assist": {"syns": ["help", "aid", "support"], "ant": "hinder", "scale": ["help", "assist", "aid", "rescue"]},
    "associate": {"syns": ["connect", "link", "relate"], "ant": "separate", "scale": ["link", "associate", "connect", "unite"]},
    "assume": {"syns": ["suppose", "guess", "presume"], "ant": "know", "scale": ["guess", "assume", "presume", "conclude"]},
    "assure": {"syns": ["promise", "guarantee", "confirm"], "ant": "doubt", "scale": ["tell", "assure", "promise", "guarantee"]},
    "astounding": {"syns": ["amazing", "shocking", "incredible"], "ant": "ordinary", "scale": ["surprising", "astounding", "astonishing", "mind-blowing"]},
    "astronomer": {"syns": ["stargazer", "scientist", "observer"], "ant": "amateur", "scale": ["observer", "astronomer", "scientist", "astrophysicist"]},
    "atmosphere": {"syns": ["air", "mood", "feeling"], "ant": "vacuum", "scale": ["air", "atmosphere", "environment", "ambiance"]},
    "attach": {"syns": ["fasten", "connect", "join"], "ant": "detach", "scale": ["stick", "attach", "fasten", "weld"]},
    "attached": {"syns": ["connected", "joined", "fastened"], "ant": "detached", "scale": ["linked", "attached", "bonded", "fused"]},
    "attentive": {"syns": ["alert", "focused", "watchful"], "ant": "distracted", "scale": ["aware", "attentive", "focused", "absorbed"]},
    "attitude": {"syns": ["outlook", "manner", "approach"], "ant": "indifference", "scale": ["feeling", "attitude", "mindset", "philosophy"]},
    "attract": {"syns": ["draw", "lure", "pull"], "ant": "repel", "scale": ["interest", "attract", "lure", "captivate"]},
    "attractive": {"syns": ["appealing", "pretty", "charming"], "ant": "unattractive", "scale": ["nice", "attractive", "beautiful", "stunning"]},
    "auction": {"syns": ["sale", "bidding", "selling"], "ant": "purchase", "scale": ["sale", "auction", "bidding war", "selloff"]},
    "authority": {"syns": ["power", "control", "leadership"], "ant": "weakness", "scale": ["influence", "authority", "power", "command"]},
    "automatically": {"syns": ["naturally", "mechanically", "instantly"], "ant": "manually", "scale": ["easily", "automatically", "instantly", "immediately"]},
    "available": {"syns": ["ready", "free", "obtainable"], "ant": "unavailable", "scale": ["possible", "available", "ready", "abundant"]},
    "average": {"syns": ["typical", "ordinary", "normal"], "ant": "exceptional", "scale": ["mediocre", "average", "typical", "standard"]},
    "avoid": {"syns": ["dodge", "escape", "evade"], "ant": "confront", "scale": ["skip", "avoid", "evade", "flee"]},
    "aware": {"syns": ["conscious", "informed", "mindful"], "ant": "unaware", "scale": ["noticing", "aware", "alert", "vigilant"]},
    "awe": {"syns": ["wonder", "amazement", "reverence"], "ant": "boredom", "scale": ["surprise", "awe", "wonder", "reverence"]},
    "awkward": {"syns": ["clumsy", "uncomfortable", "ungainly"], "ant": "graceful", "scale": ["uneasy", "awkward", "clumsy", "mortifying"]},
    # --- B ---
    "babble": {"syns": ["chatter", "prattle", "ramble"], "ant": "silence", "scale": ["murmur", "babble", "chatter", "rant"]},
    "baggage": {"syns": ["luggage", "bags", "suitcases"], "ant": "emptiness", "scale": ["bag", "baggage", "luggage", "cargo"]},
    "balcony": {"syns": ["terrace", "deck", "porch"], "ant": "basement", "scale": ["ledge", "balcony", "terrace", "rooftop"]},
    "ballads": {"syns": ["songs", "tunes", "poems"], "ant": "silence", "scale": ["ditty", "ballad", "song", "epic"]},
    "ballot": {"syns": ["vote", "election", "poll"], "ant": "abstention", "scale": ["vote", "ballot", "election", "referendum"]},
    "banter": {"syns": ["teasing", "joking", "chat"], "ant": "silence", "scale": ["chat", "banter", "teasing", "ribbing"]},
    "barber": {"syns": ["hairdresser", "stylist", "cutter"], "ant": "customer", "scale": ["trimmer", "barber", "stylist", "groomer"]},
    "bargain": {"syns": ["deal", "agreement", "discount"], "ant": "ripoff", "scale": ["deal", "bargain", "steal", "giveaway"]},
    "barrier": {"syns": ["obstacle", "wall", "blockade"], "ant": "opening", "scale": ["hurdle", "barrier", "wall", "fortress"]},
    "base": {"syns": ["bottom", "foundation", "support"], "ant": "top", "scale": ["floor", "base", "foundation", "bedrock"]},
    "bashful": {"syns": ["shy", "timid", "modest"], "ant": "bold", "scale": ["quiet", "bashful", "shy", "withdrawn"]},
    "behalf": {"syns": ["interest", "sake", "benefit"], "ant": "opposition", "scale": ["interest", "behalf", "benefit", "cause"]},
    "belligerent": {"syns": ["aggressive", "hostile", "combative"], "ant": "peaceful", "scale": ["rude", "belligerent", "hostile", "violent"]},
    "benefit": {"syns": ["advantage", "gain", "help"], "ant": "harm", "scale": ["help", "benefit", "advantage", "blessing"]},
    "benevolent": {"syns": ["kind", "generous", "charitable"], "ant": "cruel", "scale": ["nice", "benevolent", "generous", "saintly"]},
    "beverage": {"syns": ["drink", "liquid", "refreshment"], "ant": "food", "scale": ["sip", "beverage", "drink", "refreshment"]},
    "bicycle": {"syns": ["bike", "cycle", "two-wheeler"], "ant": "car", "scale": ["scooter", "bicycle", "motorcycle", "vehicle"]},
    "bitter": {"syns": ["harsh", "sour", "resentful"], "ant": "sweet", "scale": ["tart", "bitter", "sour", "acrid"]},
    "bland": {"syns": ["plain", "dull", "tasteless"], "ant": "flavorful", "scale": ["mild", "bland", "tasteless", "flavorless"]},
    "blanket": {"syns": ["cover", "quilt", "throw"], "ant": "sheet", "scale": ["sheet", "blanket", "quilt", "comforter"]},
    "blend": {"syns": ["mix", "combine", "merge"], "ant": "separate", "scale": ["stir", "blend", "mix", "fuse"]},
    "blizzard": {"syns": ["snowstorm", "whiteout", "gale"], "ant": "calm", "scale": ["flurry", "blizzard", "snowstorm", "whiteout"]},
    "blossom": {"syns": ["bloom", "flower", "flourish"], "ant": "wilt", "scale": ["bud", "blossom", "bloom", "flourish"]},
    "blunder": {"syns": ["mistake", "error", "goof"], "ant": "success", "scale": ["slip", "blunder", "mistake", "disaster"]},
    "blunt": {"syns": ["dull", "frank", "direct"], "ant": "sharp", "scale": ["rounded", "blunt", "dull", "flat"]},
    "boast": {"syns": ["brag", "show off", "flaunt"], "ant": "humble", "scale": ["mention", "boast", "brag", "flaunt"]},
    "boisterous": {"syns": ["loud", "rowdy", "noisy"], "ant": "quiet", "scale": ["lively", "boisterous", "rowdy", "unruly"]},
    "bold": {"syns": ["brave", "daring", "fearless"], "ant": "timid", "scale": ["confident", "bold", "daring", "fearless"]},
    "bond": {"syns": ["connection", "tie", "link"], "ant": "separation", "scale": ["link", "bond", "connection", "attachment"]},
    "border": {"syns": ["edge", "boundary", "limit"], "ant": "center", "scale": ["edge", "border", "boundary", "frontier"]},
    "boycott": {"syns": ["ban", "refuse", "shun"], "ant": "support", "scale": ["avoid", "boycott", "ban", "embargo"]},
    "bracelet": {"syns": ["bangle", "wristband", "armband"], "ant": "necklace", "scale": ["ring", "bracelet", "bangle", "cuff"]},
    "brawling": {"syns": ["fighting", "quarreling", "scuffling"], "ant": "peaceful", "scale": ["arguing", "brawling", "fighting", "battling"]},
    "brazen": {"syns": ["bold", "shameless", "audacious"], "ant": "shy", "scale": ["confident", "brazen", "shameless", "outrageous"]},
    "breach": {"syns": ["break", "violation", "gap"], "ant": "repair", "scale": ["crack", "breach", "break", "rupture"]},
    "breath": {"syns": ["air", "gasp", "exhale"], "ant": "suffocation", "scale": ["whisper", "breath", "gasp", "pant"]},
    "breathe": {"syns": ["inhale", "exhale", "respire"], "ant": "suffocate", "scale": ["sigh", "breathe", "inhale", "gasp"]},
    "brief": {"syns": ["short", "quick", "concise"], "ant": "lengthy", "scale": ["quick", "brief", "short", "fleeting"]},
    "brilliant": {"syns": ["bright", "clever", "outstanding"], "ant": "dull", "scale": ["smart", "brilliant", "genius", "extraordinary"]},
    "brink": {"syns": ["edge", "verge", "threshold"], "ant": "center", "scale": ["edge", "brink", "verge", "precipice"]},
    "briskly": {"syns": ["quickly", "rapidly", "energetically"], "ant": "slowly", "scale": ["steadily", "briskly", "rapidly", "swiftly"]},
    "bristle": {"syns": ["prickle", "spike", "stiffen"], "ant": "smooth", "scale": ["tingle", "bristle", "prickle", "spike"]},
    "brook": {"syns": ["stream", "creek", "rivulet"], "ant": "ocean", "scale": ["trickle", "brook", "stream", "river"]},
    "bruise": {"syns": ["mark", "injury", "bump"], "ant": "heal", "scale": ["scratch", "bruise", "wound", "gash"]},
    "bungle": {"syns": ["botch", "fumble", "mess up"], "ant": "succeed", "scale": ["slip", "bungle", "botch", "wreck"]},
    "burden": {"syns": ["load", "weight", "responsibility"], "ant": "relief", "scale": ["task", "burden", "load", "weight"]},
    "burrow": {"syns": ["tunnel", "dig", "hole"], "ant": "surface", "scale": ["hole", "burrow", "tunnel", "den"]},
    "business": {"syns": ["company", "trade", "commerce"], "ant": "leisure", "scale": ["shop", "business", "company", "corporation"]},
    "busy": {"syns": ["occupied", "active", "engaged"], "ant": "idle", "scale": ["working", "busy", "occupied", "swamped"]},
    "bystander": {"syns": ["onlooker", "witness", "spectator"], "ant": "participant", "scale": ["observer", "bystander", "witness", "spectator"]},
    # --- C ---
    "cable": {"syns": ["wire", "cord", "rope"], "ant": "wireless", "scale": ["thread", "cable", "wire", "chain"]},
    "calamity": {"syns": ["disaster", "catastrophe", "tragedy"], "ant": "blessing", "scale": ["problem", "calamity", "disaster", "catastrophe"]},
    "calculate": {"syns": ["compute", "figure", "determine"], "ant": "guess", "scale": ["count", "calculate", "compute", "analyze"]},
    "calendar": {"syns": ["schedule", "planner", "timetable"], "ant": "chaos", "scale": ["list", "calendar", "planner", "agenda"]},
    "campaign": {"syns": ["movement", "drive", "effort"], "ant": "surrender", "scale": ["effort", "campaign", "movement", "crusade"]},
    "candid": {"syns": ["honest", "frank", "open"], "ant": "deceptive", "scale": ["truthful", "candid", "frank", "blunt"]},
    "candidate": {"syns": ["applicant", "contender", "nominee"], "ant": "winner", "scale": ["applicant", "candidate", "nominee", "frontrunner"]},
    "canvas": {"syns": ["cloth", "fabric", "material"], "ant": "paper", "scale": ["fabric", "canvas", "cloth", "tapestry"]},
    "capable": {"syns": ["able", "skilled", "competent"], "ant": "incapable", "scale": ["able", "capable", "skilled", "expert"]},
    "capacity": {"syns": ["ability", "volume", "space"], "ant": "inability", "scale": ["room", "capacity", "volume", "maximum"]},
    "captives": {"syns": ["prisoners", "hostages", "detainees"], "ant": "free people", "scale": ["detainees", "captives", "prisoners", "slaves"]},
    "captivity": {"syns": ["imprisonment", "confinement", "bondage"], "ant": "freedom", "scale": ["detention", "captivity", "imprisonment", "slavery"]},
    "capture": {"syns": ["catch", "seize", "trap"], "ant": "release", "scale": ["catch", "capture", "seize", "imprison"]},
    "carefree": {"syns": ["relaxed", "easygoing", "lighthearted"], "ant": "worried", "scale": ["relaxed", "carefree", "lighthearted", "blissful"]},
    "cargo": {"syns": ["freight", "goods", "load"], "ant": "emptiness", "scale": ["package", "cargo", "freight", "shipment"]},
    "carpet": {"syns": ["rug", "mat", "covering"], "ant": "bare floor", "scale": ["mat", "carpet", "rug", "tapestry"]},
    "cascade": {"syns": ["waterfall", "flow", "pour"], "ant": "trickle", "scale": ["drip", "cascade", "waterfall", "torrent"]},
    "cask": {"syns": ["barrel", "keg", "container"], "ant": "cup", "scale": ["jug", "cask", "barrel", "vat"]},
    "castaway": {"syns": ["shipwrecked", "stranded", "marooned"], "ant": "rescued", "scale": ["lost", "castaway", "stranded", "marooned"]},
    "castle": {"syns": ["fortress", "palace", "stronghold"], "ant": "hut", "scale": ["house", "castle", "fortress", "citadel"]},
    "catalog": {"syns": ["list", "directory", "index"], "ant": "disarray", "scale": ["list", "catalog", "directory", "database"]},
    "catastrophe": {"syns": ["disaster", "calamity", "tragedy"], "ant": "miracle", "scale": ["problem", "catastrophe", "disaster", "apocalypse"]},
    "category": {"syns": ["group", "class", "type"], "ant": "whole", "scale": ["type", "category", "class", "division"]},
    "cathedral": {"syns": ["church", "temple", "chapel"], "ant": "shack", "scale": ["chapel", "cathedral", "basilica", "temple"]},
    "cause": {"syns": ["reason", "source", "origin"], "ant": "effect", "scale": ["factor", "cause", "reason", "root"]},
    "cautious": {"syns": ["careful", "wary", "guarded"], "ant": "reckless", "scale": ["careful", "cautious", "wary", "guarded"]},
    "cease": {"syns": ["stop", "end", "halt"], "ant": "continue", "scale": ["pause", "cease", "stop", "terminate"]},
    "cemetery": {"syns": ["graveyard", "burial ground", "memorial park"], "ant": "playground", "scale": ["grave", "cemetery", "graveyard", "memorial"]},
    "centre": {"syns": ["middle", "core", "heart"], "ant": "edge", "scale": ["middle", "centre", "core", "heart"]},
    "century": {"syns": ["hundred years", "era", "age"], "ant": "moment", "scale": ["decade", "century", "millennium", "era"]},
    "certain": {"syns": ["sure", "confident", "positive"], "ant": "uncertain", "scale": ["likely", "certain", "sure", "absolute"]},
    "challenge": {"syns": ["test", "trial", "dare"], "ant": "ease", "scale": ["task", "challenge", "trial", "ordeal"]},
    "chamber": {"syns": ["room", "hall", "vault"], "ant": "outdoors", "scale": ["room", "chamber", "hall", "vault"]},
    "champion": {"syns": ["winner", "hero", "defender"], "ant": "loser", "scale": ["winner", "champion", "hero", "legend"]},
    "chapter": {"syns": ["section", "part", "segment"], "ant": "whole", "scale": ["page", "chapter", "section", "volume"]},
    "character": {"syns": ["personality", "nature", "figure"], "ant": "nobody", "scale": ["person", "character", "personality", "icon"]},
    "characteristic": {"syns": ["trait", "feature", "quality"], "ant": "flaw", "scale": ["quality", "characteristic", "trait", "hallmark"]},
    "chatter": {"syns": ["talk", "gossip", "babble"], "ant": "silence", "scale": ["whisper", "chatter", "gossip", "ramble"]},
    "chill": {"syns": ["cold", "frost", "coolness"], "ant": "warmth", "scale": ["cool", "chill", "cold", "freeze"]},
    "chirp": {"syns": ["tweet", "peep", "sing"], "ant": "silence", "scale": ["peep", "chirp", "tweet", "sing"]},
    "circle": {"syns": ["ring", "loop", "round"], "ant": "line", "scale": ["curve", "circle", "ring", "sphere"]},
    "circular": {"syns": ["round", "ring-shaped", "curved"], "ant": "straight", "scale": ["curved", "circular", "round", "spherical"]},
    "circumstance": {"syns": ["situation", "condition", "event"], "ant": "choice", "scale": ["fact", "circumstance", "situation", "crisis"]},
    "civic": {"syns": ["public", "community", "municipal"], "ant": "private", "scale": ["local", "civic", "public", "governmental"]},
    "civilian": {"syns": ["citizen", "resident", "noncombatant"], "ant": "soldier", "scale": ["person", "civilian", "citizen", "resident"]},
    "claim": {"syns": ["assert", "state", "declare"], "ant": "deny", "scale": ["suggest", "claim", "assert", "insist"]},
    "clarify": {"syns": ["explain", "clear up", "simplify"], "ant": "confuse", "scale": ["hint", "clarify", "explain", "illuminate"]},
    "clasp": {"syns": ["grip", "hold", "clutch"], "ant": "release", "scale": ["touch", "clasp", "grip", "clutch"]},
    "classic": {"syns": ["timeless", "traditional", "legendary"], "ant": "modern", "scale": ["good", "classic", "timeless", "legendary"]},
    "classify": {"syns": ["sort", "group", "categorize"], "ant": "mix", "scale": ["sort", "classify", "categorize", "organize"]},
    "clever": {"syns": ["smart", "witty", "ingenious"], "ant": "foolish", "scale": ["smart", "clever", "brilliant", "genius"]},
    "climate": {"syns": ["weather", "conditions", "environment"], "ant": "shelter", "scale": ["weather", "climate", "conditions", "atmosphere"]},
    "cling": {"syns": ["hold on", "stick", "grasp"], "ant": "release", "scale": ["touch", "cling", "grip", "clutch"]},
    "coach": {"syns": ["trainer", "instructor", "mentor"], "ant": "student", "scale": ["helper", "coach", "trainer", "mentor"]},
    "coast": {"syns": ["shore", "beach", "seaside"], "ant": "inland", "scale": ["shore", "coast", "seaside", "waterfront"]},
    "coax": {"syns": ["persuade", "urge", "encourage"], "ant": "force", "scale": ["ask", "coax", "persuade", "convince"]},
    "coaxing": {"syns": ["persuading", "urging", "encouraging"], "ant": "forcing", "scale": ["asking", "coaxing", "persuading", "begging"]},
    "cobbler": {"syns": ["shoemaker", "shoe repairer", "craftsman"], "ant": "customer", "scale": ["worker", "cobbler", "shoemaker", "craftsman"]},
    "collaborate": {"syns": ["cooperate", "work together", "team up"], "ant": "compete", "scale": ["help", "collaborate", "cooperate", "unite"]},
    "collapse": {"syns": ["fall", "crumble", "break down"], "ant": "stand", "scale": ["sag", "collapse", "crumble", "shatter"]},
    "colossal": {"syns": ["huge", "enormous", "massive"], "ant": "tiny", "scale": ["big", "colossal", "enormous", "gigantic"]},
    "colony": {"syns": ["settlement", "community", "outpost"], "ant": "homeland", "scale": ["camp", "colony", "settlement", "territory"]},
    "column": {"syns": ["pillar", "post", "tower"], "ant": "row", "scale": ["post", "column", "pillar", "tower"]},
    "combine": {"syns": ["mix", "merge", "unite"], "ant": "separate", "scale": ["join", "combine", "merge", "fuse"]},
    "comment": {"syns": ["remark", "statement", "note"], "ant": "silence", "scale": ["remark", "comment", "statement", "declaration"]},
    "commit": {"syns": ["dedicate", "pledge", "promise"], "ant": "abandon", "scale": ["try", "commit", "dedicate", "devote"]},
    "committee": {"syns": ["group", "board", "panel"], "ant": "individual", "scale": ["team", "committee", "board", "council"]},
    "common": {"syns": ["ordinary", "usual", "frequent"], "ant": "rare", "scale": ["normal", "common", "frequent", "universal"]},
    "communicate": {"syns": ["talk", "share", "express"], "ant": "withhold", "scale": ["speak", "communicate", "express", "broadcast"]},
    "communication": {"syns": ["contact", "exchange", "dialogue"], "ant": "silence", "scale": ["message", "communication", "dialogue", "broadcast"]},
    "community": {"syns": ["neighborhood", "society", "group"], "ant": "isolation", "scale": ["group", "community", "society", "nation"]},
    "companion": {"syns": ["friend", "partner", "buddy"], "ant": "stranger", "scale": ["acquaintance", "companion", "friend", "soulmate"]},
    "compare": {"syns": ["contrast", "match", "relate"], "ant": "ignore", "scale": ["notice", "compare", "contrast", "analyze"]},
    "comparison": {"syns": ["contrast", "match", "analogy"], "ant": "difference", "scale": ["likeness", "comparison", "contrast", "analysis"]},
    "compassion": {"syns": ["sympathy", "kindness", "caring"], "ant": "cruelty", "scale": ["pity", "compassion", "empathy", "devotion"]},
    "compassionate": {"syns": ["caring", "kind", "sympathetic"], "ant": "cruel", "scale": ["kind", "compassionate", "caring", "devoted"]},
    "compel": {"syns": ["force", "require", "drive"], "ant": "discourage", "scale": ["urge", "compel", "force", "demand"]},
    "compete": {"syns": ["contest", "rival", "challenge"], "ant": "cooperate", "scale": ["try", "compete", "rival", "battle"]},
    "competition": {"syns": ["contest", "rivalry", "tournament"], "ant": "cooperation", "scale": ["game", "competition", "contest", "championship"]},
    "compile": {"syns": ["gather", "collect", "assemble"], "ant": "scatter", "scale": ["collect", "compile", "gather", "assemble"]},
    "complex": {"syns": ["complicated", "intricate", "involved"], "ant": "simple", "scale": ["tricky", "complex", "complicated", "bewildering"]},
    "composition": {"syns": ["essay", "piece", "creation"], "ant": "destruction", "scale": ["draft", "composition", "essay", "masterpiece"]},
    "compost": {"syns": ["fertilizer", "mulch", "humus"], "ant": "waste", "scale": ["scraps", "compost", "fertilizer", "soil"]},
    "comprehend": {"syns": ["understand", "grasp", "realize"], "ant": "misunderstand", "scale": ["notice", "comprehend", "understand", "master"]},
    "conceal": {"syns": ["hide", "cover", "disguise"], "ant": "reveal", "scale": ["cover", "conceal", "hide", "bury"]},
    "concentrate": {"syns": ["focus", "think hard", "pay attention"], "ant": "daydream", "scale": ["notice", "concentrate", "focus", "absorb"]},
    "concept": {"syns": ["idea", "notion", "thought"], "ant": "reality", "scale": ["idea", "concept", "theory", "philosophy"]},
    "concern": {"syns": ["worry", "care", "interest"], "ant": "indifference", "scale": ["interest", "concern", "worry", "anxiety"]},
    "concert": {"syns": ["show", "performance", "recital"], "ant": "silence", "scale": ["recital", "concert", "show", "festival"]},
    "conclude": {"syns": ["finish", "end", "decide"], "ant": "begin", "scale": ["pause", "conclude", "finish", "complete"]},
    "concluding": {"syns": ["final", "last", "closing"], "ant": "opening", "scale": ["late", "concluding", "final", "ultimate"]},
    "conduct": {"syns": ["behavior", "manage", "lead"], "ant": "misbehavior", "scale": ["act", "conduct", "manage", "direct"]},
    "confess": {"syns": ["admit", "reveal", "acknowledge"], "ant": "deny", "scale": ["hint", "confess", "admit", "declare"]},
    "confident": {"syns": ["sure", "bold", "certain"], "ant": "unsure", "scale": ["hopeful", "confident", "sure", "fearless"]},
    "confirm": {"syns": ["verify", "prove", "validate"], "ant": "deny", "scale": ["check", "confirm", "verify", "prove"]},
    "conflict": {"syns": ["fight", "disagreement", "clash"], "ant": "peace", "scale": ["disagreement", "conflict", "clash", "war"]},
    "confront": {"syns": ["face", "challenge", "oppose"], "ant": "avoid", "scale": ["meet", "confront", "challenge", "defy"]},
    "confuse": {"syns": ["puzzle", "bewilder", "mix up"], "ant": "clarify", "scale": ["puzzle", "confuse", "bewilder", "baffle"]},
    "congregation": {"syns": ["assembly", "gathering", "crowd"], "ant": "individual", "scale": ["group", "congregation", "assembly", "multitude"]},
    "connect": {"syns": ["join", "link", "attach"], "ant": "disconnect", "scale": ["touch", "connect", "link", "bond"]},
    "conquer": {"syns": ["defeat", "overcome", "win"], "ant": "surrender", "scale": ["beat", "conquer", "overcome", "dominate"]},
    "conscience": {"syns": ["morals", "ethics", "inner voice"], "ant": "apathy", "scale": ["feeling", "conscience", "morals", "principles"]},
    "conscious": {"syns": ["aware", "awake", "alert"], "ant": "unconscious", "scale": ["awake", "conscious", "aware", "alert"]},
    "consequence": {"syns": ["result", "outcome", "effect"], "ant": "cause", "scale": ["result", "consequence", "outcome", "impact"]},
    "consider": {"syns": ["think about", "ponder", "reflect"], "ant": "ignore", "scale": ["notice", "consider", "ponder", "deliberate"]},
    "considerable": {"syns": ["significant", "large", "substantial"], "ant": "small", "scale": ["some", "considerable", "substantial", "enormous"]},
    "consist": {"syns": ["include", "contain", "comprise"], "ant": "exclude", "scale": ["have", "consist", "include", "comprise"]},
    "consistent": {"syns": ["steady", "reliable", "uniform"], "ant": "inconsistent", "scale": ["regular", "consistent", "steady", "unwavering"]},
    "constant": {"syns": ["continuous", "steady", "unchanging"], "ant": "changing", "scale": ["regular", "constant", "continuous", "permanent"]},
    "construct": {"syns": ["build", "create", "make"], "ant": "destroy", "scale": ["make", "construct", "build", "engineer"]},
    "consult": {"syns": ["ask", "discuss", "confer"], "ant": "ignore", "scale": ["ask", "consult", "discuss", "confer"]},
    "consume": {"syns": ["eat", "use up", "devour"], "ant": "produce", "scale": ["taste", "consume", "devour", "gorge"]},
    "consumer": {"syns": ["buyer", "customer", "shopper"], "ant": "producer", "scale": ["shopper", "consumer", "buyer", "customer"]},
    "contact": {"syns": ["touch", "reach", "connect"], "ant": "avoid", "scale": ["reach", "contact", "connect", "meet"]},
    "contain": {"syns": ["hold", "include", "store"], "ant": "release", "scale": ["hold", "contain", "store", "enclose"]},
    "context": {"syns": ["setting", "background", "situation"], "ant": "isolation", "scale": ["setting", "context", "background", "framework"]},
    "continue": {"syns": ["proceed", "carry on", "persist"], "ant": "stop", "scale": ["go on", "continue", "persist", "endure"]},
    "contradiction": {"syns": ["conflict", "opposite", "inconsistency"], "ant": "agreement", "scale": ["difference", "contradiction", "conflict", "paradox"]},
    "contrast": {"syns": ["difference", "comparison", "distinction"], "ant": "similarity", "scale": ["difference", "contrast", "distinction", "opposition"]},
    "contribute": {"syns": ["give", "donate", "help"], "ant": "withhold", "scale": ["give", "contribute", "donate", "sacrifice"]},
    "contribution": {"syns": ["donation", "gift", "offering"], "ant": "withdrawal", "scale": ["gift", "contribution", "donation", "sacrifice"]},
    "control": {"syns": ["manage", "direct", "regulate"], "ant": "chaos", "scale": ["guide", "control", "command", "dominate"]},
    "controversy": {"syns": ["debate", "argument", "dispute"], "ant": "agreement", "scale": ["discussion", "controversy", "debate", "scandal"]},
    "convenient": {"syns": ["handy", "easy", "accessible"], "ant": "inconvenient", "scale": ["useful", "convenient", "handy", "ideal"]},
    "convert": {"syns": ["change", "transform", "switch"], "ant": "maintain", "scale": ["change", "convert", "transform", "revolutionize"]},
    "convince": {"syns": ["persuade", "influence", "sway"], "ant": "discourage", "scale": ["suggest", "convince", "persuade", "compel"]},
    "convinced": {"syns": ["persuaded", "certain", "sure"], "ant": "doubtful", "scale": ["hopeful", "convinced", "certain", "positive"]},
    "cooperate": {"syns": ["work together", "collaborate", "help"], "ant": "compete", "scale": ["help", "cooperate", "collaborate", "unite"]},
    "cooperation": {"syns": ["teamwork", "collaboration", "partnership"], "ant": "competition", "scale": ["help", "cooperation", "teamwork", "partnership"]},
    "cope": {"syns": ["manage", "handle", "deal with"], "ant": "surrender", "scale": ["survive", "cope", "manage", "thrive"]},
    "coral": {"syns": ["reef", "marine life", "organism"], "ant": "sand", "scale": ["shell", "coral", "reef", "atoll"]},
    "core": {"syns": ["center", "heart", "middle"], "ant": "surface", "scale": ["middle", "core", "heart", "nucleus"]},
    "correspond": {"syns": ["match", "relate", "communicate"], "ant": "differ", "scale": ["relate", "correspond", "match", "align"]},
    "courage": {"syns": ["bravery", "valor", "nerve"], "ant": "cowardice", "scale": ["nerve", "courage", "bravery", "heroism"]},
    "courageous": {"syns": ["brave", "fearless", "bold"], "ant": "cowardly", "scale": ["brave", "courageous", "fearless", "heroic"]},
    "coward": {"syns": ["weakling", "scaredy-cat", "chicken"], "ant": "hero", "scale": ["nervous", "coward", "weakling", "chicken"]},
    "cozy": {"syns": ["comfortable", "warm", "snug"], "ant": "uncomfortable", "scale": ["warm", "cozy", "snug", "toasty"]},
    "crater": {"syns": ["hole", "pit", "cavity"], "ant": "mound", "scale": ["dent", "crater", "pit", "chasm"]},
    "craving": {"syns": ["desire", "longing", "hunger"], "ant": "disgust", "scale": ["wish", "craving", "longing", "obsession"]},
    "create": {"syns": ["make", "build", "produce"], "ant": "destroy", "scale": ["make", "create", "build", "invent"]},
    "creativity": {"syns": ["imagination", "originality", "invention"], "ant": "imitation", "scale": ["skill", "creativity", "imagination", "genius"]},
    "crew": {"syns": ["team", "group", "staff"], "ant": "individual", "scale": ["pair", "crew", "team", "army"]},
    "critical": {"syns": ["important", "vital", "crucial"], "ant": "unimportant", "scale": ["important", "critical", "vital", "essential"]},
    "criticise": {"syns": ["judge", "review", "fault"], "ant": "praise", "scale": ["comment", "criticise", "judge", "condemn"]},
    "croak": {"syns": ["squawk", "rasp", "grunt"], "ant": "sing", "scale": ["murmur", "croak", "squawk", "screech"]},
    "culture": {"syns": ["tradition", "heritage", "civilization"], "ant": "ignorance", "scale": ["custom", "culture", "tradition", "civilization"]},
    "cure": {"syns": ["remedy", "treatment", "heal"], "ant": "disease", "scale": ["treatment", "cure", "remedy", "miracle"]},
    "curiosity": {"syns": ["interest", "wonder", "inquisitiveness"], "ant": "boredom", "scale": ["interest", "curiosity", "wonder", "fascination"]},
    "curious": {"syns": ["interested", "nosy", "inquisitive"], "ant": "bored", "scale": ["interested", "curious", "eager", "fascinated"]},
    "currency": {"syns": ["money", "cash", "funds"], "ant": "debt", "scale": ["coins", "currency", "money", "wealth"]},
    "current": {"syns": ["present", "existing", "modern"], "ant": "past", "scale": ["recent", "current", "present", "latest"]},
    "curtain": {"syns": ["drape", "blind", "screen"], "ant": "window", "scale": ["shade", "curtain", "drape", "screen"]},
    "cushion": {"syns": ["pillow", "pad", "buffer"], "ant": "rock", "scale": ["pad", "cushion", "pillow", "mattress"]},
    "custom": {"syns": ["tradition", "habit", "practice"], "ant": "novelty", "scale": ["habit", "custom", "tradition", "ritual"]},
    "customary": {"syns": ["usual", "traditional", "typical"], "ant": "unusual", "scale": ["normal", "customary", "traditional", "established"]},
    "customs": {"syns": ["traditions", "practices", "habits"], "ant": "innovations", "scale": ["habits", "customs", "traditions", "rituals"]},
    "cycle": {"syns": ["rotation", "sequence", "loop"], "ant": "end", "scale": ["loop", "cycle", "rotation", "revolution"]},
    "cylinder": {"syns": ["tube", "column", "barrel"], "ant": "cube", "scale": ["tube", "cylinder", "column", "drum"]},
    # --- D ---
    "damage": {"syns": ["harm", "injury", "destruction"], "ant": "repair", "scale": ["scratch", "damage", "wreck", "destroy"]},
    "daunting": {"syns": ["intimidating", "scary", "challenging"], "ant": "easy", "scale": ["challenging", "daunting", "intimidating", "terrifying"]},
    "dazzling": {"syns": ["brilliant", "stunning", "blinding"], "ant": "dull", "scale": ["bright", "dazzling", "brilliant", "blinding"]},
    "debate": {"syns": ["discuss", "argue", "dispute"], "ant": "agree", "scale": ["discuss", "debate", "argue", "clash"]},
    "debris": {"syns": ["rubble", "wreckage", "remains"], "ant": "order", "scale": ["scraps", "debris", "rubble", "wreckage"]},
    "decade": {"syns": ["ten years", "period", "era"], "ant": "instant", "scale": ["year", "decade", "century", "millennium"]},
    "decay": {"syns": ["rot", "decompose", "crumble"], "ant": "grow", "scale": ["age", "decay", "rot", "crumble"]},
    "deceive": {"syns": ["trick", "fool", "mislead"], "ant": "inform", "scale": ["fib", "deceive", "trick", "betray"]},
    "decide": {"syns": ["choose", "determine", "resolve"], "ant": "hesitate", "scale": ["consider", "decide", "determine", "commit"]},
    "declaration": {"syns": ["announcement", "statement", "proclamation"], "ant": "secret", "scale": ["statement", "declaration", "announcement", "proclamation"]},
    "declare": {"syns": ["announce", "state", "proclaim"], "ant": "conceal", "scale": ["say", "declare", "announce", "proclaim"]},
    "decline": {"syns": ["refuse", "decrease", "drop"], "ant": "accept", "scale": ["dip", "decline", "drop", "plummet"]},
    "decrease": {"syns": ["reduce", "lower", "shrink"], "ant": "increase", "scale": ["dip", "decrease", "reduce", "plummet"]},
    "decree": {"syns": ["order", "command", "law"], "ant": "suggestion", "scale": ["rule", "decree", "command", "mandate"]},
    "decrepit": {"syns": ["worn out", "crumbling", "broken down"], "ant": "new", "scale": ["old", "decrepit", "crumbling", "ruined"]},
    "dedicate": {"syns": ["devote", "commit", "pledge"], "ant": "neglect", "scale": ["give", "dedicate", "devote", "sacrifice"]},
    "defeat": {"syns": ["beat", "conquer", "overcome"], "ant": "lose", "scale": ["beat", "defeat", "conquer", "crush"]},
    "defend": {"syns": ["protect", "guard", "shield"], "ant": "attack", "scale": ["protect", "defend", "guard", "fortify"]},
    "defiance": {"syns": ["rebellion", "resistance", "disobedience"], "ant": "obedience", "scale": ["resistance", "defiance", "rebellion", "revolt"]},
    "defiant": {"syns": ["rebellious", "bold", "stubborn"], "ant": "obedient", "scale": ["stubborn", "defiant", "rebellious", "mutinous"]},
    "define": {"syns": ["explain", "describe", "clarify"], "ant": "confuse", "scale": ["describe", "define", "explain", "specify"]},
    "definite": {"syns": ["certain", "clear", "specific"], "ant": "vague", "scale": ["likely", "definite", "certain", "absolute"]},
    "deft": {"syns": ["skillful", "nimble", "clever"], "ant": "clumsy", "scale": ["handy", "deft", "skillful", "masterful"]},
    "delicate": {"syns": ["fragile", "gentle", "fine"], "ant": "sturdy", "scale": ["thin", "delicate", "fragile", "breakable"]},
    "deliberate": {"syns": ["intentional", "planned", "careful"], "ant": "accidental", "scale": ["careful", "deliberate", "intentional", "calculated"]},
    "delightful": {"syns": ["lovely", "pleasant", "charming"], "ant": "awful", "scale": ["nice", "delightful", "wonderful", "enchanting"]},
    "democracy": {"syns": ["republic", "freedom", "self-government"], "ant": "dictatorship", "scale": ["voting", "democracy", "republic", "freedom"]},
    "demonstrate": {"syns": ["show", "display", "prove"], "ant": "hide", "scale": ["show", "demonstrate", "display", "prove"]},
    "dense": {"syns": ["thick", "packed", "heavy"], "ant": "thin", "scale": ["thick", "dense", "packed", "solid"]},
    "deny": {"syns": ["refuse", "reject", "contradict"], "ant": "admit", "scale": ["doubt", "deny", "refuse", "reject"]},
    "depart": {"syns": ["leave", "go", "exit"], "ant": "arrive", "scale": ["go", "depart", "leave", "flee"]},
    "depend": {"syns": ["rely", "count on", "trust"], "ant": "distrust", "scale": ["need", "depend", "rely", "count on"]},
    "deprive": {"syns": ["strip", "take away", "deny"], "ant": "provide", "scale": ["limit", "deprive", "strip", "rob"]},
    "descend": {"syns": ["go down", "drop", "fall"], "ant": "ascend", "scale": ["step down", "descend", "drop", "plummet"]},
    "describe": {"syns": ["explain", "tell", "portray"], "ant": "conceal", "scale": ["mention", "describe", "explain", "illustrate"]},
    "description": {"syns": ["account", "explanation", "portrayal"], "ant": "mystery", "scale": ["mention", "description", "account", "portrait"]},
    "desert": {"syns": ["wasteland", "abandon", "barren land"], "ant": "oasis", "scale": ["dry land", "desert", "wasteland", "wilderness"]},
    "design": {"syns": ["plan", "create", "pattern"], "ant": "destroy", "scale": ["sketch", "design", "plan", "blueprint"]},
    "desperate": {"syns": ["hopeless", "frantic", "urgent"], "ant": "calm", "scale": ["worried", "desperate", "frantic", "hopeless"]},
    "despite": {"syns": ["regardless", "in spite of", "notwithstanding"], "ant": "because of", "scale": ["although", "despite", "regardless", "notwithstanding"]},
    "detail": {"syns": ["fact", "particular", "feature"], "ant": "overview", "scale": ["fact", "detail", "particular", "specifics"]},
    "detect": {"syns": ["find", "discover", "notice"], "ant": "miss", "scale": ["sense", "detect", "discover", "uncover"]},
    "detective": {"syns": ["investigator", "inspector", "sleuth"], "ant": "criminal", "scale": ["officer", "detective", "investigator", "sleuth"]},
    "determine": {"syns": ["decide", "figure out", "establish"], "ant": "wonder", "scale": ["guess", "determine", "establish", "prove"]},
    "determined": {"syns": ["resolute", "focused", "persistent"], "ant": "uncertain", "scale": ["motivated", "determined", "resolute", "unstoppable"]},
    "detriment": {"syns": ["harm", "damage", "disadvantage"], "ant": "benefit", "scale": ["risk", "detriment", "harm", "ruin"]},
    "detrimental": {"syns": ["harmful", "damaging", "negative"], "ant": "beneficial", "scale": ["risky", "detrimental", "harmful", "destructive"]},
    "develop": {"syns": ["grow", "create", "improve"], "ant": "decline", "scale": ["start", "develop", "grow", "flourish"]},
    "device": {"syns": ["gadget", "tool", "instrument"], "ant": "nothing", "scale": ["tool", "device", "gadget", "machine"]},
    "devote": {"syns": ["dedicate", "commit", "give"], "ant": "neglect", "scale": ["give", "devote", "dedicate", "sacrifice"]},
    "diagram": {"syns": ["chart", "drawing", "illustration"], "ant": "text", "scale": ["sketch", "diagram", "chart", "blueprint"]},
    "dictate": {"syns": ["command", "order", "direct"], "ant": "follow", "scale": ["suggest", "dictate", "command", "demand"]},
    "dictionary": {"syns": ["lexicon", "glossary", "wordbook"], "ant": "novel", "scale": ["glossary", "dictionary", "encyclopedia", "reference"]},
    "difference": {"syns": ["contrast", "distinction", "variation"], "ant": "similarity", "scale": ["change", "difference", "contrast", "opposite"]},
    "dignified": {"syns": ["noble", "stately", "respectable"], "ant": "shameful", "scale": ["polite", "dignified", "noble", "majestic"]},
    "dilemma": {"syns": ["problem", "predicament", "choice"], "ant": "solution", "scale": ["problem", "dilemma", "predicament", "crisis"]},
    "diligent": {"syns": ["hardworking", "careful", "thorough"], "ant": "lazy", "scale": ["careful", "diligent", "thorough", "tireless"]},
    "dimension": {"syns": ["size", "measurement", "aspect"], "ant": "point", "scale": ["size", "dimension", "measurement", "scope"]},
    "diminutive": {"syns": ["tiny", "small", "miniature"], "ant": "enormous", "scale": ["small", "diminutive", "tiny", "microscopic"]},
    "disappear": {"syns": ["vanish", "fade", "go away"], "ant": "appear", "scale": ["fade", "disappear", "vanish", "evaporate"]},
    "disappointed": {"syns": ["let down", "upset", "unhappy"], "ant": "pleased", "scale": ["sad", "disappointed", "upset", "heartbroken"]},
    "disaster": {"syns": ["catastrophe", "calamity", "tragedy"], "ant": "blessing", "scale": ["problem", "disaster", "catastrophe", "apocalypse"]},
    "disastrous": {"syns": ["terrible", "catastrophic", "devastating"], "ant": "wonderful", "scale": ["bad", "disastrous", "catastrophic", "ruinous"]},
    "discipline": {"syns": ["control", "training", "order"], "ant": "chaos", "scale": ["rules", "discipline", "control", "strictness"]},
    "discover": {"syns": ["find", "uncover", "detect"], "ant": "hide", "scale": ["notice", "discover", "uncover", "reveal"]},
    "discuss": {"syns": ["talk about", "debate", "review"], "ant": "ignore", "scale": ["mention", "discuss", "debate", "analyze"]},
    "disguise": {"syns": ["costume", "mask", "cover"], "ant": "reveal", "scale": ["mask", "disguise", "costume", "camouflage"]},
    "display": {"syns": ["show", "exhibit", "present"], "ant": "hide", "scale": ["show", "display", "exhibit", "showcase"]},
    "dispute": {"syns": ["argument", "disagreement", "debate"], "ant": "agreement", "scale": ["disagreement", "dispute", "argument", "conflict"]},
    "dissatisfied": {"syns": ["unhappy", "displeased", "disappointed"], "ant": "satisfied", "scale": ["unhappy", "dissatisfied", "frustrated", "furious"]},
    "distinct": {"syns": ["different", "unique", "clear"], "ant": "similar", "scale": ["noticeable", "distinct", "unique", "unmistakable"]},
    "distinguish": {"syns": ["differentiate", "identify", "recognize"], "ant": "confuse", "scale": ["notice", "distinguish", "identify", "pinpoint"]},
    "distract": {"syns": ["divert", "sidetrack", "disturb"], "ant": "focus", "scale": ["bother", "distract", "divert", "confuse"]},
    "distress": {"syns": ["suffering", "pain", "worry"], "ant": "comfort", "scale": ["worry", "distress", "suffering", "agony"]},
    "distribute": {"syns": ["hand out", "share", "deliver"], "ant": "collect", "scale": ["give", "distribute", "share", "spread"]},
    "disturb": {"syns": ["bother", "interrupt", "upset"], "ant": "calm", "scale": ["bother", "disturb", "upset", "alarm"]},
    "diverse": {"syns": ["varied", "different", "assorted"], "ant": "uniform", "scale": ["mixed", "diverse", "varied", "eclectic"]},
    "diversity": {"syns": ["variety", "range", "mixture"], "ant": "sameness", "scale": ["variety", "diversity", "range", "richness"]},
    "divert": {"syns": ["redirect", "distract", "reroute"], "ant": "focus", "scale": ["shift", "divert", "redirect", "reroute"]},
    "document": {"syns": ["record", "file", "paper"], "ant": "fiction", "scale": ["note", "document", "record", "archive"]},
    "documentary": {"syns": ["film", "report", "feature"], "ant": "fiction", "scale": ["report", "documentary", "film", "exposé"]},
    "domain": {"syns": ["area", "territory", "field"], "ant": "nothing", "scale": ["area", "domain", "territory", "realm"]},
    "domestic": {"syns": ["household", "local", "home"], "ant": "foreign", "scale": ["local", "domestic", "national", "internal"]},
    "dominate": {"syns": ["control", "rule", "overpower"], "ant": "submit", "scale": ["lead", "dominate", "control", "overpower"]},
    "drama": {"syns": ["play", "excitement", "conflict"], "ant": "comedy", "scale": ["act", "drama", "tragedy", "spectacle"]},
    "drift": {"syns": ["float", "wander", "glide"], "ant": "anchor", "scale": ["float", "drift", "wander", "roam"]},
    "drought": {"syns": ["dry spell", "dryness", "shortage"], "ant": "flood", "scale": ["dryness", "drought", "famine", "desolation"]},
    "drowsy": {"syns": ["sleepy", "tired", "groggy"], "ant": "alert", "scale": ["tired", "drowsy", "sleepy", "unconscious"]},
    "durable": {"syns": ["sturdy", "long-lasting", "tough"], "ant": "fragile", "scale": ["strong", "durable", "sturdy", "indestructible"]},
    "dwell": {"syns": ["live", "reside", "inhabit"], "ant": "leave", "scale": ["stay", "dwell", "reside", "settle"]},
    "dynamic": {"syns": ["energetic", "active", "lively"], "ant": "static", "scale": ["active", "dynamic", "energetic", "explosive"]},
    # --- E-Z continued in _INLINE_DATA_2 ---
}

# Split into a second dict to keep the file manageable
_INLINE_DATA_2 = {
    # --- E ---
    "eager": {"syns": ["excited", "enthusiastic", "keen"], "ant": "reluctant", "scale": ["willing", "eager", "enthusiastic", "desperate"]},
    "earth": {"syns": ["ground", "soil", "world"], "ant": "sky", "scale": ["dirt", "earth", "ground", "terrain"]},
    "economy": {"syns": ["finances", "market", "trade"], "ant": "waste", "scale": ["trade", "economy", "market", "prosperity"]},
    "ecosystem": {"syns": ["habitat", "environment", "biome"], "ant": "wasteland", "scale": ["habitat", "ecosystem", "biome", "biosphere"]},
    "edible": {"syns": ["eatable", "safe to eat", "consumable"], "ant": "poisonous", "scale": ["safe", "edible", "delicious", "nutritious"]},
    "effect": {"syns": ["result", "impact", "outcome"], "ant": "cause", "scale": ["change", "effect", "impact", "transformation"]},
    "effective": {"syns": ["successful", "useful", "productive"], "ant": "useless", "scale": ["helpful", "effective", "powerful", "unstoppable"]},
    "effortless": {"syns": ["easy", "simple", "smooth"], "ant": "difficult", "scale": ["easy", "effortless", "smooth", "natural"]},
    "elaborate": {"syns": ["detailed", "complex", "fancy"], "ant": "simple", "scale": ["detailed", "elaborate", "complex", "ornate"]},
    "elated": {"syns": ["thrilled", "overjoyed", "delighted"], "ant": "depressed", "scale": ["happy", "elated", "thrilled", "ecstatic"]},
    "elect": {"syns": ["choose", "vote for", "select"], "ant": "reject", "scale": ["pick", "elect", "choose", "appoint"]},
    "elegant": {"syns": ["graceful", "stylish", "refined"], "ant": "crude", "scale": ["nice", "elegant", "graceful", "exquisite"]},
    "element": {"syns": ["part", "component", "factor"], "ant": "whole", "scale": ["part", "element", "component", "ingredient"]},
    "eliminate": {"syns": ["remove", "get rid of", "destroy"], "ant": "include", "scale": ["reduce", "eliminate", "remove", "eradicate"]},
    "eloquent": {"syns": ["articulate", "expressive", "fluent"], "ant": "inarticulate", "scale": ["clear", "eloquent", "articulate", "poetic"]},
    "embarrass": {"syns": ["shame", "humiliate", "fluster"], "ant": "comfort", "scale": ["fluster", "embarrass", "humiliate", "mortify"]},
    "embrace": {"syns": ["hug", "accept", "welcome"], "ant": "reject", "scale": ["hold", "embrace", "hug", "cling to"]},
    "emerge": {"syns": ["appear", "come out", "surface"], "ant": "hide", "scale": ["peek", "emerge", "appear", "burst out"]},
    "emission": {"syns": ["release", "discharge", "output"], "ant": "absorption", "scale": ["leak", "emission", "discharge", "pollution"]},
    "emotion": {"syns": ["feeling", "sentiment", "mood"], "ant": "apathy", "scale": ["feeling", "emotion", "passion", "intensity"]},
    "empathy": {"syns": ["understanding", "compassion", "sympathy"], "ant": "indifference", "scale": ["sympathy", "empathy", "compassion", "devotion"]},
    "emphasis": {"syns": ["stress", "importance", "focus"], "ant": "neglect", "scale": ["attention", "emphasis", "stress", "spotlight"]},
    "emphasize": {"syns": ["stress", "highlight", "underline"], "ant": "ignore", "scale": ["mention", "emphasize", "stress", "insist"]},
    "enable": {"syns": ["allow", "permit", "empower"], "ant": "prevent", "scale": ["help", "enable", "empower", "unleash"]},
    "encounter": {"syns": ["meet", "face", "come across"], "ant": "avoid", "scale": ["see", "encounter", "meet", "confront"]},
    "encore": {"syns": ["repeat", "extra performance", "bonus"], "ant": "finale", "scale": ["repeat", "encore", "bonus", "extension"]},
    "encourage": {"syns": ["support", "inspire", "motivate"], "ant": "discourage", "scale": ["support", "encourage", "inspire", "empower"]},
    "endeavor": {"syns": ["attempt", "effort", "try"], "ant": "quit", "scale": ["try", "endeavor", "strive", "pursue"]},
    "endure": {"syns": ["survive", "bear", "withstand"], "ant": "surrender", "scale": ["bear", "endure", "withstand", "survive"]},
    "engineer": {"syns": ["designer", "builder", "inventor"], "ant": "destroyer", "scale": ["worker", "engineer", "designer", "inventor"]},
    "engraving": {"syns": ["carving", "etching", "inscription"], "ant": "blank", "scale": ["scratch", "engraving", "carving", "sculpture"]},
    "enhance": {"syns": ["improve", "boost", "strengthen"], "ant": "diminish", "scale": ["help", "enhance", "boost", "maximize"]},
    "enigmatic": {"syns": ["mysterious", "puzzling", "cryptic"], "ant": "obvious", "scale": ["curious", "enigmatic", "mysterious", "baffling"]},
    "enormous": {"syns": ["huge", "massive", "immense"], "ant": "tiny", "scale": ["big", "enormous", "massive", "colossal"]},
    "ensure": {"syns": ["guarantee", "confirm", "secure"], "ant": "risk", "scale": ["check", "ensure", "guarantee", "secure"]},
    "enterprise": {"syns": ["business", "venture", "project"], "ant": "laziness", "scale": ["project", "enterprise", "venture", "empire"]},
    "enthusiasm": {"syns": ["excitement", "eagerness", "passion"], "ant": "apathy", "scale": ["interest", "enthusiasm", "passion", "obsession"]},
    "entirety": {"syns": ["whole", "totality", "completeness"], "ant": "part", "scale": ["piece", "majority", "entirety", "totality"]},
    "envelope": {"syns": ["cover", "wrapper", "case"], "ant": "contents", "scale": ["wrapper", "envelope", "package", "parcel"]},
    "environment": {"syns": ["surroundings", "nature", "habitat"], "ant": "void", "scale": ["setting", "environment", "habitat", "ecosystem"]},
    "envy": {"syns": ["jealousy", "desire", "longing"], "ant": "contentment", "scale": ["wish", "envy", "jealousy", "resentment"]},
    "episode": {"syns": ["event", "incident", "chapter"], "ant": "whole", "scale": ["moment", "episode", "event", "saga"]},
    "equip": {"syns": ["supply", "provide", "prepare"], "ant": "strip", "scale": ["give", "equip", "supply", "arm"]},
    "equivalent": {"syns": ["equal", "same", "matching"], "ant": "different", "scale": ["similar", "equivalent", "equal", "identical"]},
    "erode": {"syns": ["wear away", "corrode", "decay"], "ant": "build", "scale": ["weaken", "erode", "corrode", "crumble"]},
    "error": {"syns": ["mistake", "blunder", "fault"], "ant": "correctness", "scale": ["slip", "error", "mistake", "blunder"]},
    "escalate": {"syns": ["increase", "intensify", "worsen"], "ant": "decrease", "scale": ["grow", "escalate", "intensify", "explode"]},
    "especially": {"syns": ["particularly", "mainly", "notably"], "ant": "generally", "scale": ["somewhat", "especially", "particularly", "extremely"]},
    "essential": {"syns": ["necessary", "vital", "crucial"], "ant": "unnecessary", "scale": ["useful", "essential", "vital", "critical"]},
    "establish": {"syns": ["create", "found", "set up"], "ant": "destroy", "scale": ["start", "establish", "found", "build"]},
    "estimate": {"syns": ["guess", "calculate", "approximate"], "ant": "measure", "scale": ["guess", "estimate", "calculate", "determine"]},
    "evacuate": {"syns": ["leave", "clear out", "flee"], "ant": "enter", "scale": ["leave", "evacuate", "flee", "escape"]},
    "evaluate": {"syns": ["assess", "judge", "review"], "ant": "ignore", "scale": ["check", "evaluate", "assess", "analyze"]},
    "eventually": {"syns": ["finally", "ultimately", "in time"], "ant": "immediately", "scale": ["soon", "eventually", "finally", "ultimately"]},
    "evidence": {"syns": ["proof", "clue", "sign"], "ant": "doubt", "scale": ["hint", "evidence", "proof", "confirmation"]},
    "evident": {"syns": ["obvious", "clear", "apparent"], "ant": "hidden", "scale": ["noticeable", "evident", "obvious", "undeniable"]},
    "evolve": {"syns": ["develop", "change", "grow"], "ant": "stay the same", "scale": ["change", "evolve", "develop", "transform"]},
    "exaggerate": {"syns": ["overstate", "stretch", "inflate"], "ant": "understate", "scale": ["stretch", "exaggerate", "overstate", "fabricate"]},
    "examine": {"syns": ["inspect", "study", "analyze"], "ant": "ignore", "scale": ["look at", "examine", "inspect", "scrutinize"]},
    "example": {"syns": ["instance", "sample", "model"], "ant": "exception", "scale": ["case", "example", "instance", "illustration"]},
    "exceed": {"syns": ["surpass", "outdo", "go beyond"], "ant": "fall short", "scale": ["meet", "exceed", "surpass", "shatter"]},
    "excel": {"syns": ["shine", "thrive", "outperform"], "ant": "fail", "scale": ["succeed", "excel", "shine", "dominate"]},
    "excellent": {"syns": ["outstanding", "superb", "wonderful"], "ant": "terrible", "scale": ["good", "excellent", "superb", "outstanding"]},
    "except": {"syns": ["excluding", "but", "besides"], "ant": "including", "scale": ["besides", "except", "excluding", "apart from"]},
    "excerpt": {"syns": ["passage", "extract", "section"], "ant": "whole", "scale": ["quote", "excerpt", "passage", "extract"]},
    "exchange": {"syns": ["swap", "trade", "switch"], "ant": "keep", "scale": ["trade", "exchange", "swap", "barter"]},
    "exclaim": {"syns": ["shout", "cry out", "blurt"], "ant": "whisper", "scale": ["say", "exclaim", "shout", "scream"]},
    "exclaimed": {"syns": ["shouted", "cried out", "declared"], "ant": "whispered", "scale": ["said", "exclaimed", "shouted", "screamed"]},
    "exclude": {"syns": ["leave out", "ban", "reject"], "ant": "include", "scale": ["skip", "exclude", "ban", "prohibit"]},
    "execute": {"syns": ["carry out", "perform", "accomplish"], "ant": "abandon", "scale": ["do", "execute", "perform", "accomplish"]},
    "exercise": {"syns": ["workout", "activity", "training"], "ant": "rest", "scale": ["movement", "exercise", "workout", "training"]},
    "exert": {"syns": ["apply", "use", "put forth"], "ant": "relax", "scale": ["try", "exert", "strain", "push"]},
    "exhaust": {"syns": ["tire", "drain", "wear out"], "ant": "energize", "scale": ["tire", "exhaust", "drain", "deplete"]},
    "exhilarated": {"syns": ["thrilled", "excited", "elated"], "ant": "bored", "scale": ["happy", "exhilarated", "thrilled", "ecstatic"]},
    "exhilarating": {"syns": ["thrilling", "exciting", "stimulating"], "ant": "boring", "scale": ["fun", "exhilarating", "thrilling", "electrifying"]},
    "existence": {"syns": ["life", "being", "reality"], "ant": "nonexistence", "scale": ["presence", "existence", "life", "reality"]},
    "exotic": {"syns": ["unusual", "foreign", "rare"], "ant": "common", "scale": ["unusual", "exotic", "rare", "extraordinary"]},
    "expand": {"syns": ["grow", "enlarge", "spread"], "ant": "shrink", "scale": ["grow", "expand", "enlarge", "explode"]},
    "expansion": {"syns": ["growth", "increase", "spread"], "ant": "reduction", "scale": ["growth", "expansion", "increase", "explosion"]},
    "expect": {"syns": ["anticipate", "predict", "hope"], "ant": "doubt", "scale": ["hope", "expect", "anticipate", "demand"]},
    "expectation": {"syns": ["hope", "anticipation", "prediction"], "ant": "surprise", "scale": ["hope", "expectation", "anticipation", "demand"]},
    "expedition": {"syns": ["journey", "voyage", "mission"], "ant": "stay", "scale": ["trip", "expedition", "voyage", "odyssey"]},
    "experience": {"syns": ["knowledge", "event", "encounter"], "ant": "inexperience", "scale": ["event", "experience", "adventure", "ordeal"]},
    "experiment": {"syns": ["test", "trial", "study"], "ant": "theory", "scale": ["try", "experiment", "test", "investigation"]},
    "expert": {"syns": ["specialist", "master", "professional"], "ant": "beginner", "scale": ["skilled", "expert", "master", "authority"]},
    "explain": {"syns": ["clarify", "describe", "illustrate"], "ant": "confuse", "scale": ["tell", "explain", "clarify", "illuminate"]},
    "explanation": {"syns": ["reason", "clarification", "description"], "ant": "mystery", "scale": ["hint", "explanation", "clarification", "revelation"]},
    "exploit": {"syns": ["use", "take advantage of", "achievement"], "ant": "ignore", "scale": ["use", "exploit", "manipulate", "abuse"]},
    "explore": {"syns": ["investigate", "search", "discover"], "ant": "ignore", "scale": ["look", "explore", "investigate", "discover"]},
    "export": {"syns": ["send abroad", "ship out", "sell overseas"], "ant": "import", "scale": ["sell", "export", "ship", "distribute"]},
    "expose": {"syns": ["reveal", "uncover", "show"], "ant": "hide", "scale": ["show", "expose", "reveal", "uncover"]},
    "express": {"syns": ["state", "communicate", "convey"], "ant": "suppress", "scale": ["say", "express", "communicate", "proclaim"]},
    "extend": {"syns": ["stretch", "expand", "lengthen"], "ant": "shorten", "scale": ["stretch", "extend", "expand", "prolong"]},
    "extensive": {"syns": ["wide", "broad", "thorough"], "ant": "limited", "scale": ["wide", "extensive", "broad", "comprehensive"]},
    "external": {"syns": ["outer", "outside", "surface"], "ant": "internal", "scale": ["outer", "external", "outside", "surface"]},
    "extract": {"syns": ["remove", "pull out", "take out"], "ant": "insert", "scale": ["pull", "extract", "remove", "uproot"]},
    "extraordinary": {"syns": ["amazing", "remarkable", "exceptional"], "ant": "ordinary", "scale": ["unusual", "extraordinary", "remarkable", "phenomenal"]},
    "extreme": {"syns": ["intense", "severe", "drastic"], "ant": "moderate", "scale": ["strong", "extreme", "severe", "radical"]},
    "exuberant": {"syns": ["lively", "enthusiastic", "vibrant"], "ant": "subdued", "scale": ["cheerful", "exuberant", "lively", "ecstatic"]},
}

# Merge inline data into WORD_DATA (JSON data takes priority)
for _d in [_INLINE_DATA, _INLINE_DATA_2]:
    for _k, _v in _d.items():
        if _k not in WORD_DATA:
            WORD_DATA[_k] = _v

# ============================================================
# PASSAGE TEMPLATES - 12 templates that cycle through sets
# Each uses {b1}..{b12} for blanks
# ============================================================

PASSAGE_TEMPLATES = [
    # Template 0: School adventure
    "Last Monday, Priya took a quick {b1} at the bulletin board and saw an exciting announcement. According to the {b2}, the school was hosting a {b3} science fair on Friday. A sudden {b4} of excitement swept through the hallway. The rules were {b5} — every student could participate. Teams would need to {b6} through piles of research to find good topics. The teacher tried to {b7} everyone to sign up early. If too many waited, the schedule might {b8} into chaos. The experiments required {b9} handling of materials. Finding a {b10} topic would earn bonus points. Students built a {b11} of supplies on the lab table. \"I {b12} this will be the best fair yet!\" said Priya.",

    # Template 1: Nature walk
    "During the field trip, our guide took a {b1} at the trail map before we set off. We followed a strict {b2} to make sure we saw everything. The view from the hilltop was {b3}. Dark clouds hinted that a {b4} might be coming. The park ranger explained the {b5} rules for protecting wildlife. We watched a farmer use an old {b6} to prepare the soil nearby. Our teacher tried to {b7} us that the creek was safe to cross. She warned that sharp rocks could {b8} if stepped on wrong. We saw a {b9} spider web sparkling with dew. A {b10} wildflower grew between the rocks. Ants carried food to a {b11} near the path. \"I {b12} we'll see deer before sunset,\" whispered Marco.",

    # Template 2: Market day
    "Arun took a quick {b1} around the bustling market. The vendors followed their daily {b2} of setting up stalls at dawn. The fruit display looked {b3}, with colors shining in the sun. A {b4} of customers rushed in when the doors opened. Every transaction had to be {b5} and above board. The baker would {b6} through dough to make fresh bread. She tried to {b7} shoppers to try her new recipe. One careless bump could {b8} the glass jars on the shelf. The pastries had {b9} decorations made of sugar. It was {b10} to find handmade items at such low prices. A {b11} of oranges sat on the counter. \"I {b12} today will be our best sales day,\" said the owner.",

    # Template 3: Space exploration
    "Commander Luna took a final {b1} at the control panel. The mission {b2} called for launch at exactly noon. The rocket's design was {b3} — a marvel of engineering. Outside, a {b4} of cosmic dust swirled past the window. Every step of the mission had to be {b5} and follow strict protocols. The astronauts would {b6} through mountains of data to find answers. Scientists worked hard to {b7} the public that space travel was safe. If anything went wrong, it could {b8} years of planning. The instruments were {b9} and needed careful handling. A {b10} mineral was discovered on the asteroid's surface. They built a {b11} of samples to bring home. \"I {b12} this mission will change history,\" said Luna.",

    # Template 4: Ocean adventure
    "Captain Meera took a {b1} through her telescope at the horizon. According to the sailing {b2}, they would reach the island by evening. The sunset over the water was {b3}. A {b4} was approaching from the west, bringing high waves. The crew made sure their route was {b5} and followed maritime rules. They would have to {b6} through the heavy sea to stay on course. The first mate tried to {b7} the nervous passengers that all was well. The powerful waves could {b8} a smaller boat into pieces. The coral reef below was {b9} and beautiful. They spotted a {b10} sea turtle swimming alongside. Seaweed formed a {b11} on the deck. \"I {b12} calm waters ahead,\" announced the captain.",

    # Template 5: Mystery story
    "Detective Ravi took a {b1} at the mysterious envelope on the desk. His case {b2} was packed with meetings that day. The handwriting on the letter was {b3} — perfectly formed. Outside, a {b4} rattled the windows of the old office. He checked if entering the building was {b5} without a warrant. He would {b6} through every file cabinet for clues. His partner tried to {b7} him the case was too dangerous. One false move could {b8} the entire investigation. The evidence was {b9} — it had to be handled with gloves. A {b10} fingerprint was found on the doorknob. Papers formed a {b11} on the detective's desk. \"I {b12} we'll solve this before midnight,\" Ravi said confidently.",

    # Template 6: Sports competition
    "The coach took a quick {b1} at the scoreboard and smiled. The team had followed the training {b2} perfectly for weeks. Their performance in the first half was {b3}. A {b4} of cheers erupted from the fans in the stands. Every move had to be {b5} according to the rulebook. The players would {b6} through every obstacle on the field. The captain tried to {b7} the younger players to stay focused. A hard tackle could {b8} the team's winning streak. The balance beam required {b9} footwork and timing. It was {b10} for a rookie to score three goals in one game. The team formed a {b11} in the center of the field. \"I {b12} victory is ours today!\" shouted the coach.",

    # Template 7: Cooking adventure
    "Chef Amira took a {b1} at the recipe card before starting. She followed a careful {b2} to prepare each course. The aroma filling the kitchen was {b3}. A {b4} of activity erupted as the dinner rush began. Every ingredient had to be {b5} — fresh and properly sourced. She would {b6} through the preparation with skill and speed. Her assistant tried to {b7} the new cook that the sauce would thicken. Too much heat could {b8} the delicate soufflé. The pastry layers were {b9} and paper-thin. She used a {b10} spice that was hard to find in stores. A {b11} of herbs sat ready on the counter. \"I {b12} the guests will love this dish,\" she said with a grin.",

    # Template 8: Historical journey
    "The historian took a {b1} at the ancient map spread across the table. A detailed {b2} of the expedition had been planned months ago. The craftsmanship of the old artifacts was {b3}. A great {b4} of change was sweeping through the kingdom. The king's decree was {b5} and binding on all citizens. Farmers would {b6} the fields from dawn until dusk. The advisor tried to {b7} the ruler to seek peace with neighbors. War could {b8} the fragile alliance between the kingdoms. The treaty documents were {b9} and written on thin parchment. A {b10} gemstone was offered as a gift of goodwill. A {b11} of earth marked the ancient burial site. Scholars could not {b12} what the future would hold.",

    # Template 9: Environmental story
    "Dr. Noor took a {b1} at the data on her screen with concern. Her research {b2} was full of field visits this month. The coral reef she studied was {b3} in its beauty. A {b4} had damaged the coastline last week. It was {b5} to dump waste into the ocean. Conservationists would {b6} through red tape to get new protections passed. They tried to {b7} lawmakers that funding was urgent. Pollution could {b8} the fragile marine ecosystem. The ecosystem was {b9} and needed protection. They found a {b10} species of fish near the reef. A {b11} of sand had shifted after the tide. \"I {b12} that with action, we can save this reef,\" she said hopefully.",

    # Template 10: Friendship story
    "Maya took a {b1} at her best friend and knew something was wrong. Their usual after-school {b2} of walking home together had been disrupted. Things between them used to be {b3} — they never argued. But a {b4} of misunderstandings had come between them. It wasn't {b5} to read someone else's diary, and that had started the problem. Maya decided to {b6} through her fear and apologize. She tried to {b7} her friend that it would never happen again. Lies could {b8} even the strongest friendship. Feelings were {b9} and easily hurt. Moments like these were {b10} — true friendship didn't come along every day. She sat on a {b11} of grass in the park and waited. \"I {b12} she'll forgive me,\" Maya whispered to herself.",

    # Template 11: Innovation story
    "The inventor took a {b1} at the blueprint one last time. The building {b2} called for testing to begin at nine o'clock. The design was {b3} — better than anything before it. A {b4} of questions came from the review committee. Every patent filed had to be {b5} and properly documented. Engineers would {b6} through calculations to check for errors. The team leader tried to {b7} investors that the product was ready. A single flaw could {b8} months of hard work. The wiring inside was {b9} and required steady hands. Using a {b10} metal alloy made the device lighter. A {b11} of prototypes sat in the workshop. \"I {b12} this invention will change everything,\" announced the inventor proudly.",
]


def get_quiz_sentences(word, definitions):
    """Generate two context sentences for a double-take quiz from the word's definition."""
    meaning1 = definitions.get("meaning1", "")
    meaning2 = definitions.get("meaning2", "")
    challenge = definitions.get("studentChallenge", "")

    def replace_word_with_blank(sentence, w):
        """Replace a word (including inflected forms) with ___ in a sentence."""
        # Build regex that matches the word with optional suffixes (ed, ing, s, es, d, ly, er, est, ion, ment)
        pattern = re.compile(r'\b(' + re.escape(w) + r'(?:ed|ing|es|s|d|ly|er|est|tion|ment|ous|ive|al|ful)?)\b', re.IGNORECASE)
        match = pattern.search(sentence)
        if match:
            return sentence[:match.start()] + "___" + sentence[match.end():]
        return None

    # Extract example from meaning1
    s1 = ""
    if "Example:" in meaning1:
        example = meaning1.split("Example:")[1].strip()
        result = replace_word_with_blank(example, word)
        s1 = result if result else example

    # Use challenge as s2 if it has a blank
    s2 = challenge if "___" in challenge or "___ " in challenge or " ___" in challenge else ""

    # If s1 didn't work, try meaning2
    if not s1 and meaning2 and "Example:" in meaning2:
        example = meaning2.split("Example:")[1].strip()
        result = replace_word_with_blank(example, word)
        if result:
            s1 = result

    # Fallbacks
    if not s1:
        s1 = f"The ___ was important to everyone involved."
    if not s2:
        s2 = f"She needed to ___ before making her decision."

    return s1, s2


def build_secret_passage(words, set_number):
    """Build a secret passage using a template."""
    template_idx = (set_number - 1) % len(PASSAGE_TEMPLATES)
    template = PASSAGE_TEMPLATES[template_idx]

    # Create blank mapping
    blank_map = {}
    for i, word in enumerate(words):
        blank_map[f"b{i+1}"] = f"_({i+1})_"

    try:
        passage = template.format(**blank_map)
    except (KeyError, IndexError):
        # Fallback: simple passage
        parts = []
        for i, w in enumerate(words):
            parts.append(f"_({i+1})_")
        passage = " ".join(parts)

    return passage


def build_word_scale(word):
    """Build a word intensity scale using WORD_DATA."""
    if word in WORD_DATA and "scale" in WORD_DATA[word]:
        scale = WORD_DATA[word]["scale"]
        try:
            pos = scale.index(word)
        except ValueError:
            pos = 1
        return scale, pos
    # Fallback: generate a simple scale
    return [f"slightly {word}", word, f"very {word}", f"extremely {word}"], 1


def build_imposter_hunt(word):
    """Build an imposter hunt row using WORD_DATA."""
    if word in WORD_DATA:
        data = WORD_DATA[word]
        syns = data.get("syns", [f"similar to {word}", f"like {word}", f"related to {word}"])
        ant = data.get("ant", f"opposite of {word}")

        # Build the word list: vocab word + 3 synonyms + 1 antonym
        words_list = [word] + syns[:3]
        # Pad if needed
        while len(words_list) < 4:
            words_list.append(f"related to {word}")

        # Insert antonym at random position
        imposter_pos = random.randint(0, 4)
        words_list.insert(imposter_pos, ant)

        return words_list, imposter_pos, ant

    # Fallback
    words_list = [word, f"similar to {word}", f"like {word}", f"related to {word}", f"opposite of {word}"]
    return words_list, 4, f"opposite of {word}"


def enrich_file(fpath):
    """Enrich a single content JSON file."""
    with open(fpath) as f:
        data = json.load(f)

    words = data["words"]
    set_number = data["setNumber"]

    # --- Fix Double-Take Quiz ---
    definitions_map = {}
    for d in data.get("definitions", []):
        definitions_map[d["word"]] = d

    quiz = data.get("doubleTakeQuiz", [])
    for q in quiz:
        correct_word = q["correctAnswer"]
        if correct_word in definitions_map:
            s1, s2 = get_quiz_sentences(correct_word, definitions_map[correct_word])
            q["sentence1"] = s1
            q["sentence2"] = s2

    # --- Fix Secret Passage ---
    passage = build_secret_passage(words, set_number)
    data["secretPassage"]["passage"] = passage

    # --- Fix Word Scale & Imposter Hunt ---
    ws = data.get("wordScaleImposter", {})

    # Word Scales (first 4 words)
    scale_words = words[:4]
    new_scales = []
    for w in scale_words:
        scale, pos = build_word_scale(w)
        new_scales.append({
            "vocabWord": w,
            "scale": scale,
            "vocabPosition": pos
        })
    ws["wordScales"] = new_scales

    # Imposter Hunt (last 8 words)
    hunt_words = words[4:]
    new_hunts = []
    for w in hunt_words:
        word_list, imp_pos, imp_word = build_imposter_hunt(w)
        new_hunts.append({
            "vocabWord": w,
            "words": word_list,
            "imposterIndex": imp_pos,
            "imposterWord": imp_word
        })
    ws["imposterHunt"] = new_hunts

    data["wordScaleImposter"] = ws

    # Write back
    with open(fpath, "w") as f:
        json.dump(data, f, indent=2)

    return True


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    total_enriched = 0
    for grade in [3, 4, 5]:
        content_dir = f"content/grade{grade}"
        if not os.path.exists(content_dir):
            print(f"Skipping grade {grade} — directory not found")
            continue

        files = sorted([f for f in os.listdir(content_dir) if f.endswith(".json")])
        for fname in files:
            fpath = os.path.join(content_dir, fname)
            enrich_file(fpath)
            total_enriched += 1

        print(f"Grade {grade}: Enriched {len(files)} files")

    print(f"\nTotal enriched: {total_enriched} files")
    print("Done!")
