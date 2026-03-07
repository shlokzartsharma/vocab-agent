import json
import re

# ============================================================
# STEP 1: Collect ALL words from every source
# ============================================================

# Source tag constants
SRC_CUSTOM = "Custom (Existing)"
SRC_FLOCAB3 = "Flocabulary Grade 3"
SRC_FLOCAB4 = "Flocabulary Grade 4"
SRC_FLOCAB5 = "Flocabulary Grade 5"
SRC_CC3 = "Common Core Grade 3"
SRC_CC4 = "Common Core Grade 4"
SRC_CC5 = "Common Core Grade 5"
SRC_SADLIER = "Sadlier Vocab Workshop"
SRC_WORDLY3 = "Wordly Wise Book 3"
SRC_WORDLY4 = "Wordly Wise Book 4"
SRC_WORDLY5 = "Wordly Wise Book 5"
SRC_SSAT = "SSAT Elementary"
SRC_SINGAPORE = "Singapore MOE/PSLE"
SRC_CAMBRIDGE = "Cambridge Primary"
SRC_CBSE = "CBSE India"
SRC_AUSTRALIA = "Australian Curriculum"
SRC_UK_KS2 = "British KS2"
SRC_WIT3 = "Wit & Wisdom Grade 3"
SRC_WIT4 = "Wit & Wisdom Grade 4"
SRC_BENCHMARK = "Benchmark Advance"
SRC_PIACADEMY = "PiAcademy GCSE"
SRC_EDUKATE = "EduKate Singapore"
SRC_SCHOLASTIC = "Scholastic"
SRC_OXFORD = "Oxford Word Lists"
SRC_TIER2 = "Tier 2 Academic"

# Master dict: word -> set of source tags
word_sources = {}

def add_words(words, source):
    for w in words:
        w = w.strip().lower()
        w = re.sub(r'[^a-z\-]', '', w)
        if len(w) < 3:
            continue
        if w not in word_sources:
            word_sources[w] = set()
        word_sources[w].add(source)

# --- EXISTING GRADE 3 WORDS (144) ---
existing_g3 = [
    "allow","bitter","common","journey","observe","superb","fury","intent","pattern","boast","eloquent","glisten",
    "force","goal","patient","prefer","trace","accuse","clever","coast","delicate","explore","approach","approve",
    "glory","meek","magnificent","invest","locate","ripple","sufficient","uproar","aim","aware","defeat","drift",
    "mild","pause","refuse","route","ruin","solid","imitate","pierce","rare","symbol","triumph","prompt",
    "revive","tradition","watchful","wreckage","advantage","ambition","defiant","fearsome","imply","active","bargain","gasp",
    "loyal","resource","sensitive","struggle","value","vary","wander","capture","coward","exclaim","gloomy","insist",
    "passage","restless","shallow","shatter","talent","atmosphere","brilliant","convince","endure","glance","harsh","plunge",
    "precious","swift","unite","border","certain","clasp","depart","fierce","journey","observe","superb","treasure",
    "wisdom","accuse","clever","coast","delicate","explore","imitate","pierce","rare","symbol","triumph","ancient",
    "climate","cling","custom","decay","disturb","expose","perform","remote","timid","ability","avoid","bashful",
    "brief","compete","consider","delightful","honor","remark","reflex","actual","brink","chill","conquer","fortunate",
    "fury","intent","pattern","vibrant","wit","approach","approve","glory","meek","tradition","prompt","revive"
]
add_words(existing_g3, SRC_CUSTOM)

# --- FLOCABULARY GRADE 5 (140 words) ---
flocab5 = [
    "abolish","absurd","abuse","access","accomplish","achievement","aggressive","alternate","altitude","ambition",
    "analyze","anthem","appeal","appropriate","approximate","argue","aroma","assume","available","awkward",
    "barrier","benefit","beverage","bland","blunder","boast","bond","border","boycott","burden",
    "calculate","campaign","capable","capacity","character","chill","civic","classify","column","communicate",
    "compel","compile","comply","conflict","confront","conscious","consequence","consider","consistent","context",
    "continuous","contrast","convenient","convert","cope","correspond","debate","decade","decline","declaration",
    "demonstrate","deprive","descend","dictate","dispute","distinct","divert","domestic","dominate","drowsy",
    "elegant","eliminate","emphasize","endure","establish","evaluate","evident","exaggerate","excel","extract",
    "familiar","famine","fiction","focus","former","frontier","genuine","guarantee","harsh","heritage",
    "hostile","illuminate","illustrate","impact","impulse","indicate","influence","inhabitant","interpret","investigate",
    "irritate","jostle","keen","labor","landscape","legitimate","liberal","linger","literal","lofty",
    "luxurious","majority","massive","miniature","miserable","moral","mumble","negotiate","noble","numerous",
    "obstacle","overwhelm","pedestrian","persuade","plead","portable","potential","precise","precaution","predator",
    "preserve","prey","principle","proclamation","prosper","protest","provision","pursue","reassure","reform",
    "reliable","reluctant","resemble","resolve","restrict","reveal","rural","sacred","scarce","sole",
    "solemn","soothe","sophomore","source","splendid","stout","summit","supreme","symbolize","territory",
    "trait","tremendous","triumph","urban","vast","version","veteran","vow"
]
add_words(flocab5, SRC_FLOCAB5)

# --- FLOCABULARY GRADE 3 (140 words) ---
flocab3 = [
    "ability","absorb","accuse","act","active","actual","adapt","adequate","adopt","advantage",
    "advice","ambition","ancient","approach","arrange","arctic","attitude","attract","average","avoid",
    "bold","border","brief","brilliant","cable","capture","certain","chill","clever","climate",
    "cling","coast","confess","consider","contain","continent","convince","coward","crew","cure",
    "cycle","damage","decrease","defend","definite","demonstrate","depend","description","develop","device",
    "diagram","discover","discuss","drift","eager","elect","enable","entire","establish","examine",
    "except","exclaim","expand","experience","expert","explore","express","fact","fatal","feature",
    "flexible","focus","fortunate","frequent","frontier","furious","generous","giant","grace","grasp",
    "greed","grip","halt","harsh","hasty","hesitate","hollow","identify","illustrate","imagine",
    "incredible","indicate","inform","inspect","instant","intelligent","intend","investigate","island","issue",
    "journey","labor","landscape","layer","legend","limit","local","locate","lodge","luxury",
    "marvel","mature","meadow","mention","method","minimum","minor","miserable","moist","moral",
    "mound","narrow","nation","natural","necessary","negative","noble","normal","notice","numerous",
    "observe","obvious","occur","opinion","opposite","ordinary","organ","origin","passage","pastime",
    "peer","permanent","plead","plunge","popular","portion","positive","possess","predict","prepare",
    "preserve","previous","process","produce","progress","proper","provide","publish","purchase","purpose",
    "pursue","quality","quantity","rapid","rare","rate","recall","recognize","recover","reduce",
    "refer","reflect","region","relate","release","remain","remark","remove","repeat","replace",
    "represent","request","require","research","resident","resist","resources","respond","restore","result",
    "reveal","reverse","review","revolve","reward","rig","risk","route","scatter","scene",
    "schedule","select","separate","series","severe","signal","similar","simple","site","sketch",
    "soar","solve","source","specific","starve","steady","strain","structure","struggle","succeed",
    "suggest","summary","support","surface","surround","survive","swift","symbol","talent","task",
    "technique","temperature","tend","tense","texture","threat","thrill","topic","tough","tradition",
    "transfer","transform","transparent","treasure","tremendous","triumph","typical","unite","unusual","valuable",
    "variety","vast","version","visible","volunteer","weapon","wicked","wit","worthwhile"
]
add_words(flocab3, SRC_FLOCAB3)

# --- FLOCABULARY GRADE 4 (140 words) ---
flocab4 = [
    "accurate","address","afford","alert","analyze","ancestor","annual","apparent","appropriate","arena",
    "arrest","ascend","assist","attempt","attentive","attractive","awkward","baggage","basic","benefit",
    "blend","blossom","burrow","calculate","capable","captivity","carefree","century","chamber","circular",
    "coax","column","communicate","companion","comparison","compile","complete","conflict","congregation","connect",
    "consequence","considerable","constant","construct","contribute","control","convenient","convince","cooperate","cozy",
    "create","critical","current","customary","decay","declare","delicate","dense","desperate","determine",
    "develop","device","devote","diagram","disaster","discipline","distinguish","distract","document","drowsy",
    "dwell","eager","edible","effective","elegant","eliminate","embrace","emerge","encourage","endure",
    "enormous","episode","essential","estimate","evaluate","evidence","exaggerate","excel","exchange","exclaim",
    "expand","export","extend","extract","fascinate","flexible","focus","fortunate","fragile","frequent",
    "fume","function","furious","gaze","generous","genuine","gigantic","glare","gleam","glimpse",
    "grace","gradual","gust","harsh","haven","hazard","hesitate","horizontal","humble","humor",
    "identify","illustrate","image","immediate","incredible","indicate","influence","inhabit","inspect","instant",
    "investigate","jagged","junior","legend","linger","locate"
]
add_words(flocab4, SRC_FLOCAB4)

# --- COMMON CORE TIER II GRADE 3 ---
cc3 = [
    "ability","absorb","accuse","adapt","adequate","advantage","advice","ambition","ancient","approach",
    "arrange","attract","avoid","bold","border","brief","brilliant","cable","capture","certain",
    "chill","clever","climate","cling","coast","confess","consider","contain","continent","convince",
    "coward","crew","cure","cycle","damage","decrease","defend","definite","demonstrate","depend",
    "description","develop","device","diagram","discover","discuss","drift","eager","elect","enable",
    "entire","establish","examine","except","exclaim","expand","experience","expert","explore","express",
    "fact","fatal","feature","flexible","focus","fortunate","frequent","frontier","furious","generous",
    "giant","grace","grasp","greed","grip","halt","harsh","hasty","hesitate","hollow",
    "identify","illustrate","imagine","incredible","indicate","inform","inspect","instant","intelligent","intend",
    "investigate","island","issue","journey","labor","landscape","layer","legend","limit","local",
    "locate","lodge","luxury","marvel","mature","meadow","mention","method","minimum","minor",
    "miserable","moist","moral","mound","narrow","nation","natural","necessary","negative","noble",
    "normal","notice","numerous","observe","obvious","occur","opinion","opposite","ordinary","organ",
    "origin","passage","pastime","peer","permanent","plead","plunge","popular","portion","positive",
    "possess","predict","prepare","preserve","previous","process","produce","progress","proper","provide",
    "publish","purchase","purpose","pursue","quality","quantity","rapid","rare","rate","recall",
    "recognize","recover","reduce","refer","reflect","region","relate","release","remain","remark",
    "remove","repeat","replace","represent","request","require","research","resident","resist","resources",
    "respond","restore","result","reveal","reverse","review","revolve","reward","risk","route",
    "scatter","scene","schedule","select","separate","series","severe","signal","similar","simple",
    "site","sketch","soar","solve","source","specific","starve","steady","strain","structure",
    "struggle","succeed","suggest","summary","support","surface","surround","survive","swift","symbol",
    "talent","task","technique","temperature","tend","tense","texture","threat","thrill","topic",
    "tough","tradition","transfer","transform","transparent","treasure","tremendous","triumph","typical","unite",
    "unusual","valuable","variety","vast","version","visible","volunteer","weapon","wicked","wit","worthwhile"
]
add_words(cc3, SRC_CC3)

# --- COMMON CORE TIER II GRADE 4 ---
cc4 = [
    "accomplish","adaptation","approached","argued","automatically","avoid","border","calculate","cause","circular",
    "compare","concluding","confirm","contrast","convince","critical","decrease","defend","demonstrate","describe",
    "detail","develop","difference","disappointed","distribute","effective","eliminate","entirety","essential","estimate",
    "evidence","example","except","exclaimed","flexible","fortunate","frequent","furious","increasing","infer",
    "inform","insert","maximum","minimum","observe","organized","obvious","passage","persuade","predict",
    "prediction","prefer","previous","purpose","rarely","reason","recognize","recommend","represent","result",
    "scarce","select","separate","simplify","summarize","surround","support","temporary","threatens","tradition",
    "typical","usually"
]
add_words(cc4, SRC_CC4)

# --- COMMON CORE TIER II GRADE 5 ---
cc5 = [
    "abolish","accomplish","accurate","announce","anxious","approach","approval","approximate","argument","avoid",
    "briskly","cease","claim","conclude","conflict","consistent","context","convince","culture","decade",
    "dissatisfied","dominate","drowsy","edible","effortless","equivalent","escalate","establish","evaluate","evidence",
    "exhaust","expansion","expectation","explain","express","extend","familiar","frequent","gigantic","glare",
    "gist","harsh","heroic","hesitate","hilarious","historic","horizontal","hostile","huddle","identify",
    "illegible","immigrate","influence","investigate","navigate","opposed","ordinary","passage","persuade","primary",
    "recently","reference","review","revolt","scarce","significant","source","summarize","superior","tension",
    "tolerate","tremble","unexpected","unfamiliar","vertical"
]
add_words(cc5, SRC_CC5)

# --- SSAT ELEMENTARY ---
ssat = [
    "abandon","abolish","acknowledge","adhesive","admire","aggravate","ail","aimless","alarmed","alter",
    "approximate","blunt","burrow","capable","conceal","contradiction","debate","decline","detrimental","envy",
    "evacuate","fragile","furious","generous","guardian","hardship","hazard","idealism","illuminate","jagged",
    "jubilation","kin","liberate","luxurious","moral","myth","nonchalant","novel","obsolete","orchard",
    "petrify","plentiful","protagonist","queasy","restore","reveal","route","salvage","seldom","shabby",
    "taunt","tragedy","uproot","valiant","vivid","weary","withdraw","zany"
]
add_words(ssat, SRC_SSAT)

# --- SINGAPORE MOE/PSLE ---
singapore = [
    "abundance","accelerate","acquire","adequate","admire","adversary","aesthetic","alleviate","ambition","analyze",
    "anecdote","animate","anticipate","apparatus","appreciate","articulate","astounding","authenticate","benevolent",
    "biodiversity","boisterous","brilliant","capacity","collaborate","compassion","comprehend","consequence","contradict",
    "contribute","cooperation","creativity","cumulative","curiosity","dazzling","deceive","dedicate","deliberate",
    "demonstrate","dexterity","diligent","diversity","dynamic","eloquent","empathy","endeavor","enhance","enthusiasm",
    "environment","exemplary","exhilarating","expand","expedition","extraordinary","facilitate","fluctuate","formidable",
    "fruition","gratitude","harmonious","illuminate","improvise","innovative","integrity","jubilant",
    "abundant","adapt","ambiguous","appropriate","boast","buoyant","collaborate","comprehend","consequence","deplete",
    "distinguish","diverse","elaborate","emerge","evaluate","fathom","frustrate","grasp","hesitate","hypothesis",
    "immerse","industrious","integrate","juxtapose","lucid","magnify","momentum","navigate","nostalgic","observe",
    "opportune","paradox","persistent","quaint","replenish","resilient","scrutinize","simultaneously","spacious",
    "tangible","transform","unravel","versatile","warrant","yield","zealous",
    "bystander","witness","vast","extensive","amass","reluctant","compassionate","meticulous","mischievous",
    "ferocious","elaborate","apprehensive","petrified","mortified","elated","exhilarated","colossal","mammoth",
    "catastrophe","calamity"
]
add_words(singapore, SRC_SINGAPORE)

# --- EDUKATE SINGAPORE P5 ADVANCED ---
edukate = [
    "aberration","altruistic","benevolent","candid","conscientious","diligent","discerning","eloquent","empathetic",
    "fervent","fortitude","gregarious","harmonious","idyllic","impeccable","jubilant","kinetic","luminous",
    "meticulous","nimble","opulent","perseverance","quintessential","resilient","sagacious","tenacious","ubiquitous",
    "venerable","whimsical","xenial","yearning","zealous","aesthetic","astute","audacious","benign","capricious",
    "daunting","ebullient","fastidious","garrulous","hapless","incandescent","juxtapose","kaleidoscopic","labyrinthine",
    "magnanimous","nascent","oblivious","paradox","quandary","ravenous","scrupulous","tenuous","unprecedented",
    "vivacious","wistful","yielding","zephyr","acrimonious","beguile","congenial","dexterous","effervescent",
    "flamboyant","gratuitous","hypothetical","iconoclast","judicious","knack","lackadaisical","melancholy","nonchalant",
    "ostentatious","philanthropic","querulous","recalcitrant","sanguine","taciturn","unassailable","vindictive","wary",
    "exuberant","frivolous","gullible","harrowing","impervious","jeopardize","kudos","loquacious","munificent",
    "nebulous","ominous","penchant","reticent","spurious","trepidation","unwavering","voracious","whet"
]
add_words(edukate, SRC_EDUKATE)

# --- PIACADEMY GCSE ---
piacademy = [
    "aberration","accolade","amalgamate","ambiguous","belligerent","benevolent","brazen","candid","capitulate",
    "clandestine","cogent","complacent","conundrum","debilitate","decadent","deference","deft","deleterious",
    "didactic","disparage","ebullient","egregious","eloquent","emulate","enigmatic","ephemeral","erratic",
    "esoteric","exacerbate","exonerate","facetious","fastidious","flagrant","frivolous","garrulous","gratuitous",
    "hackneyed","harbinger","iconoclast","impetuous","incorrigible","insidious","intrepid","juxtapose","laconic",
    "lethargic","magnanimous","nefarious","obsequious","pernicious"
]
add_words(piacademy, SRC_PIACADEMY)

# --- UK KS2 STATUTORY YEARS 3-4 ---
uk_ks2_34 = [
    "accident","actual","address","answer","appear","arrive","believe","bicycle","breath","breathe",
    "build","busy","business","calendar","caught","centre","century","certain","circle","complete",
    "consider","continue","decide","describe","different","difficult","disappear","early","earth","eight",
    "eighth","enough","exercise","experience","experiment","extreme","famous","favourite","february","forward",
    "fruit","grammar","group","guard","guide","heard","heart","height","history","imagine",
    "increase","important","interest","island","knowledge","learn","length","library","material","medicine",
    "mention","minute","natural","naughty","notice","occasion","often","opposite","ordinary","particular",
    "peculiar","perhaps","popular","position","possess","possession","possible","potatoes","pressure","probably",
    "promise","purpose","quarter","question","recent","regular","reign","remember","sentence","separate",
    "special","straight","strange","strength","suppose","surprise","therefore","though","although","thought",
    "through","various","weight","woman","women"
]
add_words(uk_ks2_34, SRC_UK_KS2)

# --- UK KS2 STATUTORY YEARS 5-6 ---
uk_ks2_56 = [
    "accommodate","accompany","according","achieve","aggressive","amateur","ancient","apparent","appreciate","attached",
    "available","average","awkward","bargain","bruise","category","cemetery","committee","communicate","community",
    "competition","conscience","conscious","controversy","correspond","criticise","curiosity","definite","desperate",
    "determined","develop","dictionary","disastrous","embarrass","environment","equip","especially","exaggerate",
    "excellent","existence","explanation","familiar","foreign","forty","frequently","government","guarantee","harass",
    "hindrance","identity","immediate","individual","interfere","interrupt","language","leisure","lightning","marvellous",
    "mischievous","muscle","necessary","neighbour","nuisance","occupy","occur","opportunity","parliament","persuade",
    "physical","prejudice","privilege","profession","programme","pronunciation","queue","recognise","recommend",
    "relevant","restaurant","rhyme","rhythm","sacrifice","secretary","shoulder","signature","sincere","soldier",
    "stomach","sufficient","suggest","symbol","system","temperature","thorough","twelfth","variety","vegetable",
    "vehicle","yacht"
]
add_words(uk_ks2_56, SRC_UK_KS2)

# --- CBSE INDIA ---
cbse = [
    "chirp","flutter","feast","gleam","peep","scurry","trot","wander","huddle","gasp",
    "shiver","gobble","croak","whimper","grumble","mumble","squeal","trudge","stumble","scramble",
    "pounce","prowl","shelter","hump","sprout","blossom","meadow","orchard","hollow","swoop",
    "glide","soar","perch","waddle","peck","bristle","cherish","foster","prompt","sufficient",
    "genuine","obscure","persist","vivid","feeble","cautious","cobbler","merchant","weaver","pilgrim",
    "famine","harvest","monsoon","courage","voyage","compassion","parcel","vessel","cargo","anchor",
    "pier","harbour","mast","rudder","plough","drought","torrent","brook","cascade","gorge",
    "ravine","cliff","ridge","summit","peak","valley","plateau","marsh","swamp","thicket","canopy",
    "vendor","pedlar","hawker","tinker","recycle","compost","salvage","debris","rubble","castaway",
    "shipwreck","stranded","wilderness","provisions","ration","fortify","stockade","inhabitant","slumber",
    "decrepit","tavern","rustic","miniature","colossal","diminutive","gigantic","voyage","barber","chatter",
    "prattle","babble","ramble","interrupt","hibernate","blizzard","tundra","arctic","crevasse"
]
add_words(cbse, SRC_CBSE)

# --- AUSTRALIAN CURRICULUM ---
australia = [
    "accomplish","appreciate","atmosphere","bargain","calculate","collaborate","compare","concentrate","confident",
    "consider","continue","cooperate","create","curious","decide","demonstrate","describe","determine","develop",
    "discover","disguise","display","elect","encourage","examine","exchange","exclaim","expand","experience",
    "experiment","explore","express","fascinate","frequent","generous","government","gradual","guarantee","hesitate",
    "identify","illustrate","imagine","immediate","impression","increase","independent","indicate","individual",
    "influence","information","inquire","inspect","interfere","investigate","justify","knowledge","language","leisure",
    "magnificent","material","measure","mention","necessary","observe","occasion","occupy","operate","opportunity",
    "organize","original","parliament","particular","patient","perform","permission","persuade","pleasant","position",
    "possess","possible","precious","predict","prefer","prepare","previous","principle","procedure","produce",
    "profession","progress","protect","provide","purpose","quality","quantity","recognize","recommend","reference",
    "reign","represent","request","require","research","resource","response","responsible","result","ridiculous",
    "sacrifice","separate","sequence","significant","similar","solution","source","specific","sufficient","suggest",
    "support","surprise","survive","temperature","temporary","thorough","transfer","transport","triumph","typical",
    "unique","various","version","volunteer",
    "accommodate","accompany","according","achieve","aggressive","amateur","ancient","apparent","appreciate",
    "attached","available","average","awkward","bargain","bruise","category","cemetery","committee","communicate",
    "community","conscience","conscious","controversy","correspond","criticise","curiosity","definite","desperate",
    "determined","develop","disastrous","embarrass","environment","equip","especially","exaggerate","excellent",
    "existence","explanation","familiar","foreign","forty","frequently","government","guarantee","harass","hindrance",
    "identity","immediate","individual","interfere","interrupt","language","leisure","lightning","marvellous",
    "mischievous","muscle","necessary","neighbour","nuisance","occupy","occur","opportunity","parliament","persuade",
    "physical","prejudice","privilege","profession","programme","pronunciation","queue","recognise","recommend",
    "relevant","restaurant","rhyme","rhythm","sacrifice","secretary","shoulder","signature","sincere","soldier",
    "stomach","sufficient","suggest","symbol","system","temperature","thorough","twelfth","variety","vegetable",
    "vehicle","yacht"
]
add_words(australia, SRC_AUSTRALIA)

# --- CAMBRIDGE PRIMARY ---
cambridge = [
    "abroad","adventure","ambulance","balcony","blanket","bracelet","calendar","carpet","castle","cathedral",
    "champion","cliff","coach","competition","concert","curtain","cushion","desert","detective","dictionary",
    "documentary","engineer","envelope","fairy","ferry","flight","flood","fog","forest","frost",
    "furniture","garage","guard","helmet","highway","horror","hurricane","island","jewellery","journey",
    "jungle","ladder","lamp","lightning","luggage","magazine","market","mechanic","museum","ocean",
    "palace","passenger","petrol","pillow","platform","prison","railway","rainbow","reporter","restaurant",
    "sailor","scientist","scarf","shark","slipper","soldier","stadium","storm","suitcase","theatre",
    "thunder","tower","trophy","umbrella","uniform","vehicle","village","volcano","whale","wing"
]
add_words(cambridge, SRC_CAMBRIDGE)

# --- WIT & WISDOM GRADE 3 ---
wit3 = [
    "request","fasten","quiver","shiver","crater","catalog","ignorant","visible","fertilizer","method",
    "mastodon","revolve","tradition","assembly","astronomer","planetarium","orbit","rotation","sphere","galaxy",
    "telescope","kimono","immigrant","journey","voyage","customs","heritage","homeland","inspire","dignified",
    "congregation","modern","exotic","choreography","torrent","soothe","imitate","ordinary","salary","precious",
    "canvas","motion","tangled","gesture","coaxing","prejudice","ovation","recital","humiliation","encore"
]
add_words(wit3, SRC_WIT3)

# --- WIT & WISDOM GRADE 4 ---
wit4 = [
    "literal","figurative","atrium","ventricle","valve","simile","metaphor","infer","stanza","meter",
    "rhythm","rhyme","repetition","imagery","alliteration","onomatopoeia","theme","synthesize","idiom",
    "courageous","concentrate","honorable","circulatory","cardiac","chamber","immortal","anonymous","infinitely",
    "survival","wilderness","essential","desperate","shelter","hatchet","triumph","persevere","perspective",
    "conflict","revolution","convinced","liberty","massacre","propaganda","composition","engraving","defiance",
    "standoff","mobilized","restrain","settlement","morale","civilian","resilience","intelligence","patriotism",
    "frontier","captives","defend","communication","diversity","frontier"
]
add_words(wit4, SRC_WIT4)

# --- SADLIER VOCAB WORKSHOP ---
sadlier = [
    "adage","bonanza","churlish","citadel","collaborate","decree","discordant","evolve","excerpt","grope",
    "hover","jostle","laggard","plaudit","preclude","revert","rubble","servile","vigil","wrangle",
    "antic","avow","banter","bountiful","congest","detriment","durable","enterprise","frugal","gingerly",
    "glut","incognito","invalidate","legendary","maim","minimize","oblique","veer","venerate","wanton",
    "allot","amass","audacious","comply","devoid","elite","grapple","incapacitate","instigate","longevity",
    "myriad","perspective","perturb","prodigious","relevant","skittish","tether","unison","vie","willful",
    "annul","bolster","deplore","frivolous","muster","nonentity","obsess","ornate","oust","peruse",
    "porous","prone","promontory","qualm","recourse","residue","solicitous","staid","sustain",
    "admonish","breach","brigand","circumspect","commandeer","cumbersome","deadlock","debris","diffuse","dilemma",
    "efface","muddle","opinionated","perennial","predispose","relinquish","salvage","spasmodic","spurious","unbridled",
    "adjourn","compensate","dissolute","erratic","expulsion","feint","fodder","fortify","illegible","jeer",
    "lucrative","mediocre","proliferate","subjugate","sully","tantalize","terse","unflinching",
    "abridge","adherent","altercation","cherubic","condone","dissent","eminent","exorcise","fabricate","irate",
    "marauder","pauper","pilfer","rift","semblance","surmount","terminate","trite","usurp",
    "abscond","anarchy","arduous","auspicious","biased","daunt","disentangle","fated","hoodwink","inanimate",
    "incinerate","intrepid","larceny","pliant","pompous","precipice","rectify","reprieve","revile",
    "adroit","amicable","averse","belligerent","benevolent","cursory","duplicity","extol","feasible","grimace",
    "holocaust","impervious","impetus","jeopardy","meticulous","nostalgia","quintessence","retrogress","scrutinize","tepid",
    "accost","animosity","appease","avid","brusque","finesse","hackneyed","inert","infirmity","musty",
    "officious","ominous","pinnacle","remorse","rancid","sophomoric","squeamish","turbulent","venture",
    "adulterate","ambidextrous","augment","bereft","deploy","dour","fortitude","gape","guise","insidious",
    "intimation","opulent","pliable","reiterate","solace","stolid","tentative","unkempt","verbatim"
]
add_words(sadlier, SRC_SADLIER)

# --- WORDLY WISE BOOK 3 ---
ww3 = [
    "cylinder","examine","fatal","feature","grasp","jet","marine","scar","tentacle","attract",
    "crew","ambition","auction","coast","elect","frustrate","govern","haste","injure","pastime",
    "rate","rig","spine","surrender","tournament","vanish","volunteer","accurate","boisterous","cumbersome",
    "harbor","investigate","mimic","obstacle","purchase","tempest","vertical","adopt","arctic","capable",
    "climate","continent","coral","device","diagram","establish","explore","flexible","frequent","frontier",
    "landscape","layer","legend","limit","local","locate","luxury","meadow","mention","method",
    "moist","moral","narrow","necessary","numerous","occur","origin","passage","peer","plunge",
    "possess","preserve","process","region","remain","remark","request","research","scatter","scene",
    "severe","similar","site","soar","source","starve","strain","structure","succeed","surround",
    "survive","swift","talent","technique","temperature","tough","tradition","transfer","treasure","triumph",
    "vast","version","visible","weapon","worthwhile"
]
add_words(ww3, SRC_WORDLY3)

# --- WORDLY WISE BOOK 5 ---
ww5 = [
    "ample","burden","compassion","comply","cumbersome","distress","encounter","exert","indignant","jest",
    "mirth","moral","outskirts","resume","ridicule","awe","execute","stable","colossal","sanctuary",
    "concur","desolate","kindle","precarious","meticulous","congenial","resilient","cursory","emulate","languish",
    "fastidious","craving","gale","blizzard","colony","waddle","cask","accelerate","boisterous","dormant",
    "bungle","erode","accurate","harbor","investigate","mimic","obstacle","purchase","tempest","vertical"
]
add_words(ww5, SRC_WORDLY5)

# --- BENCHMARK ADVANCE ---
benchmark = [
    "ballot","boycott","campaign","polls","candidate","amendment","predicted","denied","insisted","obeyed",
    "united","contribution","ballads","forge","muttered","strolled","reluctantly","vanished","sauntered","brawling",
    "compensate","experimental","practical","renewable","pollution","opinion","emission","transportation","eliminate"
]
add_words(benchmark, SRC_BENCHMARK)

# --- TIER 2 ACADEMIC (Primary Colour 3-4-5 list) ---
tier2 = [
    "abandon","abstract","access","achieve","acquire","adapt","adequate","adjust","advantage","affect",
    "afford","alter","alternative","amaze","amount","analyze","annual","anticipate","apparent","appreciate",
    "approach","appropriate","approve","argue","arrange","assist","associate","assume","assure","attach",
    "attempt","attitude","authority","available","average","avoid","aware","barrier","base","behalf",
    "benefit","bond","brief","capable","capture","category","cause","challenge","chapter","characteristic",
    "circumstance","claim","clarify","classic","collapse","combine","comment","commit","communicate","community",
    "compare","complex","concept","concern","conclude","conduct","confident","confirm","conflict","confuse",
    "connect","consequence","consider","consist","constant","construct","consult","consume","contact","contain",
    "context","continue","contribute","control","convince","cope","core","create","critical","culture",
    "current","cycle","data","debate","decade","define","demonstrate","deny","design","despite",
    "detail","detect","device","devote","dimension","discipline","discover","discuss","display","distinct",
    "distribute","diverse","document","domain","drama","economy","effect","element","eliminate","emerge",
    "emotion","emphasis","enable","encounter","enormous","ensure","environment","episode","equip","era",
    "error","essential","establish","estimate","evaluate","eventually","evidence","evolve","examine","exceed",
    "exclude","exhibit","expand","expect","expert","exploit","expose","external","extract","extreme",
    "factor","feature","final","finance","focus","force","former","foundation","framework","function",
    "fund","fundamental","generate","globe","goal","grade","grant","guarantee","identify","ignore",
    "illustrate","image","impact","implement","imply","import","impose","indicate","individual","influence",
    "initial","injure","input","insert","inspect","instance","institute","integrate","intelligent","intense",
    "internal","interpret","interval","investigate","invest","involve","isolate","issue","item","journal",
    "justify","label","layer","lecture","legal","likewise","link","locate","logic","major",
    "manipulate","mature","maximize","media","method","migrate","minimize","minor","mode","monitor",
    "motivation","navigate","network","normal","notion","nuclear","objective","obtain","obvious","occur",
    "option","orient","outcome","output","overall","overlap","panel","parallel","participate","partner",
    "passive","pattern","perceive","period","permit","persist","perspective","phase","phenomenon","policy",
    "portion","pose","positive","potential","precise","predict","previous","primary","principal","prior",
    "proceed","process","professional","prohibit","project","promote","proportion","prospect","protocol","publish",
    "pursue","range","ratio","react","region","register","regulate","reinforce","reject","relate",
    "release","rely","remove","require","research","resource","respond","restore","restrict","retain",
    "reveal","revenue","reverse","revise","revolution","role","route","scenario","schedule","scheme",
    "scope","section","sector","secure","seek","select","sequence","series","shift","significant",
    "similar","simulate","site","sole","sort","source","specific","stable","status","strategy",
    "structure","style","submit","subsequent","substitute","sum","summary","supplement","survey","survive",
    "suspend","sustain","symbol","target","task","team","technical","technique","technology","temporary",
    "tend","tense","theme","theory","topic","trace","tradition","transfer","transform","transmit",
    "transport","trend","trigger","undergo","unique","update","utilize","valid","version","via",
    "virtual","visible","vision","visual","volume","volunteer"
]
add_words(tier2, SRC_TIER2)

# --- SCHOLASTIC ---
scholastic = [
    "consumer","currency","distribute","economy","labor","genre","metaphor","simile","synonym","theme",
    "tone","immigrant","ancestor","adaptation","ecosystem","independence","democracy","population","frontier",
    "peninsula","parallel","perpendicular","demonstrate","recommend","maximum","minimum"
]
add_words(scholastic, SRC_SCHOLASTIC)

# ============================================================
# STEP 2: Filter out too-easy and too-hard words
# ============================================================

too_easy = {
    "act","run","big","cat","dog","eat","hot","cold","red","blue","green","yellow","sit","stand",
    "walk","jump","swim","fly","push","pull","throw","catch","build","draw","sing","dance","read",
    "write","drink","sleep","wake","kick","stretch","crawl","hop","skip","happy","sad","angry",
    "excited","small","tall","short","sweet","sour","soft","clean","dirty","fast","slow","young",
    "old","kind","teacher","friend","school","class","book","pen","learn","share","help","play",
    "family","home","mother","father","brother","sister","doctor","police","shop","park","library",
    "lesson","test","rule","study","tree","flower","sun","rain","cloud","animal","bird","fish",
    "river","mountain","sky","grass","wind","lake","forest","garden","farm","beach","snow","sand",
    "rock","leaf","seed","the","and","for","are","but","not","you","all","can","her","was",
    "one","our","out","day","had","has","his","how","its","may","new","now","old","see","way",
    "who","get","got","let","say","she","too","use","boy","man","girl","mum","dad","baby",
    "eye","room","bed","hand","food","toy","door","eight","eighth","forty","fruit","potatoes",
    "women","woman","february","simple","normal","basic","complete","early","enough","different",
    "difficult","straight","through","thought","though","although","where","home","put","house",
    "good","people","look","called","first","well","found","next","again","want","name","going",
    "take","two","thing","night","fun","work","here","new","water","away","long","make","great",
    "children","many","every","most","way","still","right","tell","need","head","best","dear",
    "why","three","give","love","end","year","lived","inside","last","another",
    "act","jet","rig","kin","via","sum","era","data","item","mode",
    "cub","fawn","foal","lamb","calf","kitten","pup","chick","hatchling","tadpole",
    "answer","group","guide","heard","heart","weight","special","question","minute",
    "sentence","remember","promise","suppose","surprise","position","possible","important",
    "interest","often","perhaps","probably","regular","recent","quarter","pressure",
    "caught","address","forward","favourite","grammar","guard","height","history","medicine",
    "length","material","naughty","notice","believe"
}

# Words too advanced for grade 5 (college/SAT level)
too_hard = {
    "aberration","accolade","amalgamate","capitulate","clandestine","cogent","complacent","debilitate",
    "decadent","deference","deleterious","didactic","disparage","egregious","ephemeral","esoteric",
    "exacerbate","exonerate","facetious","flagrant","garrulous","gratuitous","hackneyed","harbinger",
    "iconoclast","impetuous","incorrigible","insidious","laconic","lethargic","nefarious","obsequious",
    "pernicious","acrimonious","beguile","kaleidoscopic","labyrinthine","nascent","ostentatious",
    "philanthropic","querulous","recalcitrant","sanguine","taciturn","unassailable","vindictive",
    "munificent","nebulous","spurious","trepidation","loquacious","incandescent","quintessential",
    "ubiquitous","sagacious","xenial","xenophobia","zephyr","whet","conundrum","altruistic",
    "adage","bonanza","churlish","citadel","discordant","servile","wrangle","bountiful","congest",
    "incognito","invalidate","oblique","venerate","wanton","devoid","grapple","incapacitate",
    "instigate","longevity","perturb","prodigious","skittish","tether","annul","deplore","nonentity",
    "obsess","ornate","oust","peruse","porous","promontory","qualm","recourse","residue","solicitous",
    "staid","admonish","brigand","circumspect","commandeer","deadlock","efface","opinionated",
    "predispose","relinquish","spasmodic","unbridled","adjourn","dissolute","expulsion","feint",
    "fodder","subjugate","sully","tantalize","abridge","adherent","altercation","cherubic","condone",
    "dissent","exorcise","fabricate","marauder","pauper","pilfer","semblance","surmount","usurp",
    "abscond","anarchy","arduous","auspicious","hoodwink","inanimate","incinerate","larceny","pliant",
    "pompous","precipice","reprieve","revile","adroit","duplicity","extol","grimace","holocaust",
    "retrogress","tepid","accost","animosity","appease","brusque","finesse","musty","officious",
    "rancid","sophomoric","squeamish","adulterate","ambidextrous","augment","bereft","dour",
    "intimation","reiterate","stolid","unkempt","verbatim","capricious","dexterous","effervescent",
    "flamboyant","hypothetical","judicious","lackadaisical","wistful","vivacious","tenuous",
    "hapless","impervious","voracious","opulent","ebullient","astute","audacious","benign",
    "fastidious","reticent","penchant","unwavering","unprecedented","conscientious","discerning",
    "empathetic","fervent","gregarious","idyllic","impeccable","kinetic","luminous","tenacious",
    "venerable","whimsical","yielding","scrupulous","yearning",
    "abashed","aloof","anguish","pseudonym","avow","antic","gingerly","glut",
    "laggard","preclude","revert","vigil","vie","willful","bolster","frivolous","muster",
    "biased","daunt","disentangle","fated","rectify","amicable","averse","cursory","feasible",
    "impetus","jeopardy","nostalgia","scrutinize","avid","inert","infirmity","pinnacle",
    "remorse","turbulent","deploy","guise","pliable","solace","tentative",
    "proliferate","mediocre","lucrative","terse","unflinching","eminent","irate","rift","trite",
    "intrepid","diffuse","cumbersome","erratic","illegible","fortify","compensate","fabricate",
    "myriad","relevant","elite","comply","prodigious","perennial","amass","spasmodic","salvage",
    "concur","desolate","languish","precarious","cursory","emulate","congenial","dormant",
    "absurd","aesthetic","articulate","authenticate","biodiversity","buoyant","cumulative",
    "dexterity","exemplary","facilitate","fluctuate","fruition","hypothesis","immerse",
    "industrious","juxtapose","lucid","magnify","momentum","nostalgic","opportune","paradox",
    "persistent","replenish","scrutinize","simultaneously","spacious","tangible","unravel",
    "versatile","warrant","zealous","contradict","deplete","fathom",
    "circulatory","cardiac","ventricle","atrium","infinitely","onomatopoeia","alliteration",
    "synthesize","propaganda","mobilized","mastodon","planetarium","choreography",
    "cocoon","chrysalis","rivulet","gorge","ravine","thicket","canopy","crevasse",
    "corroboree","eucalyptus","wattle","billabong","diurnal","anemometer","navvy","osseous","philately"
}

# Filter
filtered = {}
for word, sources in word_sources.items():
    if word in too_easy or word in too_hard:
        continue
    if len(word) < 3:
        continue
    filtered[word] = sources

# ============================================================
# STEP 3: Grade-level assignment
# ============================================================

# Heuristic: use source grade tags + word complexity
grade3_signals = {SRC_CUSTOM, SRC_FLOCAB3, SRC_CC3, SRC_WORDLY3, SRC_WIT3, SRC_CBSE}
grade4_signals = {SRC_FLOCAB4, SRC_CC4, SRC_WORDLY4, SRC_WIT4, SRC_BENCHMARK}
grade5_signals = {SRC_FLOCAB5, SRC_CC5, SRC_WORDLY5, SRC_UK_KS2, SRC_AUSTRALIA, SRC_SINGAPORE, SRC_EDUKATE, SRC_PIACADEMY, SRC_SSAT}

def assign_grade(word, sources):
    g3 = len(sources & grade3_signals)
    g4 = len(sources & grade4_signals)
    g5 = len(sources & grade5_signals)
    
    # Explicit existing words = grade 3
    if SRC_CUSTOM in sources:
        return 3
    
    # If only in advanced international sources, grade 5
    if sources <= {SRC_SINGAPORE, SRC_EDUKATE, SRC_PIACADEMY, SRC_SSAT, SRC_SADLIER}:
        return 5
    
    if g3 > g4 and g3 > g5:
        return 3
    if g4 > g3 and g4 > g5:
        return 4
    if g5 > g4:
        return 5
    
    # Tiebreaker: word length/complexity
    if len(word) <= 5:
        return 3
    elif len(word) <= 7:
        return 4
    else:
        return 5

grade_buckets = {3: [], 4: [], 5: []}
for word, sources in sorted(filtered.items()):
    grade = assign_grade(word, sources)
    grade_buckets[grade].append((word, sorted(sources)))

# ============================================================
# STEP 4: Group into sets of 12
# ============================================================
import random
random.seed(42)

def make_sets(words_with_sources):
    random.shuffle(words_with_sources)
    sets = []
    for i in range(0, len(words_with_sources), 12):
        batch = words_with_sources[i:i+12]
        if len(batch) < 12:
            break  # don't include incomplete sets
        set_words = [w for w, s in batch]
        # Combine all sources
        all_sources = set()
        for w, s in batch:
            all_sources.update(s)
        sets.append({
            "setNumber": len(sets) + 1,
            "words": set_words,
            "sources": sorted(all_sources)
        })
    return sets

result = {}
for grade in [3, 4, 5]:
    sets = make_sets(grade_buckets[grade])
    result[f"grade{grade}"] = {
        "sets": sets,
        "totalWords": sum(len(s["words"]) for s in sets),
        "totalSets": len(sets)
    }

total_unique = sum(r["totalWords"] for r in result.values())
output = {
    "grade3": result["grade3"],
    "grade4": result["grade4"],
    "grade5": result["grade5"],
    "totalUniqueWords": total_unique
}

# Save JSON
with open("/Users/suchitrasharma/vocab-agent/vocab-master-list.json", "w") as f:
    json.dump(output, f, indent=2)

# ============================================================
# STEP 5: Generate summary report
# ============================================================

print("=" * 60)
print("VOCAB MASTER LIST — SUMMARY REPORT")
print("=" * 60)

for grade in [3, 4, 5]:
    g = result[f"grade{grade}"]
    print(f"\nGrade {grade}: {g['totalWords']} words in {g['totalSets']} sets")
    for s in g["sets"]:
        print(f"  Set {s['setNumber']}: {', '.join(s['words'])}")

print(f"\n{'=' * 60}")
print(f"TOTAL UNIQUE WORDS: {total_unique}")
print(f"{'=' * 60}")

# Words appearing in 5+ sources
print(f"\nWORDS IN 5+ SOURCES (most important):")
multi_source = [(w, len(s), sorted(s)) for w, s in filtered.items() if len(s) >= 5]
multi_source.sort(key=lambda x: -x[1])
for w, count, srcs in multi_source:
    print(f"  {w} ({count} sources): {', '.join(srcs)}")

# International-unique words
print(f"\nINTERNATIONAL-UNIQUE WORDS (not in US curricula):")
us_sources = {SRC_CC3, SRC_CC4, SRC_CC5, SRC_FLOCAB3, SRC_FLOCAB4, SRC_FLOCAB5, 
              SRC_WORDLY3, SRC_WORDLY4, SRC_WORDLY5, SRC_SSAT, SRC_SCHOLASTIC,
              SRC_BENCHMARK, SRC_WIT3, SRC_WIT4, SRC_CUSTOM, SRC_TIER2, SRC_SADLIER}
intl_sources = {SRC_SINGAPORE, SRC_EDUKATE, SRC_CAMBRIDGE, SRC_CBSE, SRC_AUSTRALIA, SRC_UK_KS2, SRC_PIACADEMY}
intl_only = [(w, sorted(s)) for w, s in filtered.items() if s & intl_sources and not (s & us_sources)]
intl_only.sort()
for w, srcs in intl_only[:50]:
    print(f"  {w}: {', '.join(srcs)}")
if len(intl_only) > 50:
    print(f"  ... and {len(intl_only) - 50} more")

print(f"\nTotal international-unique: {len(intl_only)}")

