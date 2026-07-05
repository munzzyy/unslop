#!/usr/bin/env python3
"""unslop - flag the AI tells in a piece of writing.

Reads text from a file argument or stdin and prints the patterns that make prose
read as LLM-generated: filler phrases, overused buzzwords, the "not just X, but Y"
frame, em-dash spray, emoji, and suspiciously even sentence rhythm. It does NOT
rewrite anything - that's your job. It just shows you where to look.

Standard library only. No network, no dependencies.

Usage:
  unslop path/to/text.md
  echo "some text here" | unslop
  unslop --json path/to/text.md      # machine-readable
  unslop --quiet path/to/text.md     # verdict line only

Exit code is 0 when the text reads human enough, 1 when it needs a pass -
so you can drop it into a pre-commit hook or CI.
"""
import sys
import re
import json
import argparse

__version__ = "0.1.0"

# Words that show up far more in LLM prose than in how people actually write.
BUZZWORDS = [
    "delve", "delved", "delving", "tapestry", "testament", "realm", "realms",
    "landscape", "navigate", "navigating", "robust", "seamless", "seamlessly",
    "leverage", "leveraging", "leverages", "underscore", "underscores",
    "underscoring", "pivotal", "crucial", "comprehensive", "intricate",
    "intricacies", "myriad", "plethora", "foster", "fostering", "elevate",
    "elevates", "elevating", "embark", "unlock", "unlocks", "unlocking",
    "harness", "harnessing", "cutting-edge", "game-changer", "game-changing",
    "boasts", "boasting", "nestled", "bustling", "vibrant", "showcase",
    "showcasing", "spearhead", "meticulous", "meticulously", "ever-evolving",
    "ever-changing", "holistic", "synergy", "paradigm", "profound", "nuanced",
    "multifaceted", "beacon", "treasure trove", "delve into", "rich tapestry",
    "supercharge", "turbocharge", "effortless", "effortlessly", "unleash",
    "empower", "empowering", "transformative", "reimagine", "reimagined",
    "streamline", "streamlined", "peace of mind", "dive deep", "deep dive",
]

# Whole-phrase tics. Matched case-insensitively as substrings.
PHRASES = [
    "it's important to note", "it is important to note", "it's worth noting",
    "it is worth noting", "in conclusion", "in summary", "to sum up",
    "that said", "rest assured", "needless to say", "at the end of the day",
    "in today's world", "in today's fast-paced", "let's dive", "dive into",
    "let's break it down", "here's the thing", "i hope this helps",
    "feel free to", "happy to help", "great question", "as an ai",
    "as a language model", "this is where", "look no further",
    "without further ado", "the key takeaway", "let's explore",
    "let's take a look", "buckle up", "when it comes to", "at its core",
    "the world of", "in the realm of", "plays a vital role",
    "plays a crucial role", "a wide range of", "more than just",
    "not just a", "whether you're a", "gone are the days",
]

# (label, regex, weight, hint)
PATTERNS = [
    ("'not just X but Y' construction",
     r"\bnot (?:just|only)\b[^.?!\n]{1,70}?\bbut\b", 3,
     "state it plainly instead of the contrast frame"),
    ("'it isn't X, it's Y' flip",
     r"\bis(?:n't| not)\b[^.?!\n]{1,45}?\bit'?s\b", 2,
     "just say what it is"),
    ("rhetorical question opener",
     r"(?im)^\s*(?:ever wondered|have you ever|what if|imagine (?:a|if|that)|picture this)\b", 2,
     "open with the point, not a hook"),
    ("hedge stack (may/can/often/typically)",
     r"\b(?:may|might|can|could|often|typically|generally|usually|arguably)\b", 0,
     "too many hedges reads evasive - commit or cut"),
]

# Real emoji + the decorative dingbats used as slop. Deliberately does NOT
# include plain glyphs that belong in technical prose: check/cross marks
# (U+2713 U+2717), arrows (U+2192...), bullets, box-drawing, etc.
_BMP_EMOJI = "✅❌✨⭐⭕❗⚡❤⬆\U0001F004"
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U0001F1E6-\U0001F1FF" + _BMP_EMOJI + "️]")


def load_text(path):
    if path and path != "-":
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    return sys.stdin.read()


def find_all(text_lower, needle):
    start, hits = 0, []
    while True:
        i = text_lower.find(needle, start)
        if i < 0:
            break
        hits.append(i)
        start = i + len(needle)
    return hits


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def analyze(text):
    lower = text.lower()
    words = re.findall(r"[A-Za-z][A-Za-z'\-]+", text)
    wc = max(len(words), 1)
    per1k = lambda n: round(n * 1000.0 / wc, 1)

    buzz = []
    for w in BUZZWORDS:
        if " " in w or "-" in w:
            hits = find_all(lower, w)
        else:
            hits = [m.start() for m in re.finditer(r"\b" + re.escape(w) + r"\b", lower)]
        if hits:
            buzz.append((w, len(hits), [line_of(text, h) for h in hits[:5]]))
    buzz.sort(key=lambda x: -x[1])
    buzz_total = sum(n for _, n, _ in buzz)

    phr = []
    for p in PHRASES:
        hits = find_all(lower, p)
        if hits:
            phr.append((p, len(hits), [line_of(text, h) for h in hits[:5]]))
    phr.sort(key=lambda x: -x[1])
    phr_total = sum(n for _, n, _ in phr)

    pat = []
    for label, rx, weight, hint in PATTERNS:
        matches = list(re.finditer(rx, text))
        if matches:
            pat.append((label, len(matches), weight, hint,
                        [line_of(text, m.start()) for m in matches[:5]]))

    emdash = len(re.findall(r"—", text))
    emoji = len(EMOJI.findall(text))

    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    slens = [len(re.findall(r"[A-Za-z'\-]+", s)) for s in sentences if s.strip()]
    uniformity = None
    if len(slens) >= 5:
        mean = sum(slens) / len(slens)
        sd = (sum((x - mean) ** 2 for x in slens) / len(slens)) ** 0.5
        uniformity = round((sd / mean) if mean else 0, 2)

    raw = (buzz_total * 3) + (phr_total * 3)
    for _, n, weight, _, _ in pat:
        raw += n * weight
    emdash_excess = max(0, emdash - max(2, wc // 90))
    raw += emdash_excess
    raw += emoji * 2
    # repeated "**Term:** explanation" bullets - a formatting tell
    bold_bullets = len(re.findall(r"(?m)^\s*[-*+]\s+\*\*[^*\n]{1,45}?(?::\*\*|\*\*:)", text))
    if bold_bullets >= 3:
        raw += (bold_bullets - 2) * 2
    score = per1k(raw)
    if uniformity is not None and uniformity < 0.35:
        score += 8

    verdict = "looks human"
    if score >= 25:
        verdict = "reads as AI - needs a real rewrite"
    elif score >= 10:
        verdict = "some AI tells - worth a pass"

    return {
        "words": wc, "score_per_1k": score, "verdict": verdict,
        "buzzwords": buzz, "phrases": phr, "patterns": pat,
        "em_dashes": emdash, "em_dash_excess": emdash_excess, "emoji": emoji,
        "bold_label_bullets": bold_bullets, "sentence_uniformity_cv": uniformity,
    }


def report(r, quiet=False):
    out = [f"words: {r['words']}   AI-tell score: {r['score_per_1k']}/1k   -> {r['verdict']}"]
    if quiet:
        return "\n".join(out)
    if r["buzzwords"]:
        out.append("\nLLM buzzwords:")
        for w, n, lines in r["buzzwords"]:
            out.append(f"  {n:>2}x  {w:<18} (lines {', '.join(map(str, lines))})")
    if r["phrases"]:
        out.append("\nFiller phrases:")
        for p, n, lines in r["phrases"]:
            out.append(f'  {n:>2}x  "{p}" (lines {", ".join(map(str, lines))})')
    if r["patterns"]:
        out.append("\nConstructions:")
        for label, n, weight, hint, lines in r["patterns"]:
            tag = "" if weight else "  [style, not scored]"
            out.append(f"  {n:>2}x  {label}{tag} (lines {', '.join(map(str, lines))})")
            out.append(f"        -> {hint}")
    misc = []
    if r["em_dash_excess"]:
        misc.append(f"{r['em_dashes']} em dashes is dense for the length (vary the punctuation)")
    if r["emoji"]:
        misc.append(f"{r['emoji']} emoji (usually worth dropping in prose)")
    if r["sentence_uniformity_cv"] is not None and r["sentence_uniformity_cv"] < 0.35:
        misc.append(f"sentence lengths very even (cv={r['sentence_uniformity_cv']}) - vary the rhythm")
    if r.get("bold_label_bullets", 0) >= 3:
        misc.append(f"{r['bold_label_bullets']} '**Term:** ...' bullets - a formatting tell; write some as prose")
    if misc:
        out.append("\nRhythm & surface:")
        for m in misc:
            out.append(f"  - {m}")
    if not (r["buzzwords"] or r["phrases"] or r["patterns"] or misc):
        out.append("\nNothing flagged. Reads clean.")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="unslop", description="Flag the AI tells in a piece of writing.")
    ap.add_argument("path", nargs="?", default="-", help="text file, or - for stdin")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--quiet", action="store_true", help="verdict line only")
    ap.add_argument("--threshold", type=float, default=10.0,
                    help="score at/above which exit code is 1 (default 10)")
    ap.add_argument("--version", action="version", version=f"unslop {__version__}")
    args = ap.parse_args(argv)

    r = analyze(load_text(args.path))
    print(json.dumps(r, indent=2) if args.json else report(r, quiet=args.quiet))
    return 0 if r["score_per_1k"] < args.threshold else 1


if __name__ == "__main__":
    sys.exit(main())
