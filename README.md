# unslop

A tiny command-line tool that flags the tells that make writing read as AI-generated, so you can rewrite them before you hit send.

It doesn't rewrite anything for you. It just points at the smells — the filler phrases, the overused buzzwords, the "not just X, but Y" reflex, em-dash spray, emoji, and the eerily even sentence rhythm that LLM prose falls into — and gives you a score. What you do about it is up to you.

No dependencies, no network, no telemetry. One Python file, standard library only.

## Why

AI writing has a texture. Once you notice it you can't stop: the same forty words, the same hedging, the same tidy tricolons, an em-dash in every other sentence. Readers notice too, and in a lot of places — a pull request, a cover letter, a code review — that texture gets your writing distrusted or skimmed past. `unslop` is a quick check you can run before that happens.

It's a smell detector, not a grader. A clean score doesn't mean the writing is good, and a flagged word isn't always wrong. Read the output, use your judgment, keep the em-dash if you meant it.

## Install

```bash
pipx install unslop        # once published
# or just grab the file — it has no dependencies:
python unslop.py --help
```

## Use

```bash
unslop draft.md                 # scan a file
git show HEAD:MESSAGE | unslop   # scan a commit message
echo "Let's dive into it" | unslop
unslop --quiet draft.md          # just the verdict line
unslop --json draft.md           # machine-readable
```

The exit code is `0` when the text reads human enough and `1` when it doesn't, so you can wire it into a pre-commit hook or CI:

```bash
# .git/hooks/commit-msg
unslop --quiet "$1" || echo "heads up: that message reads a bit AI. ^"
```

## What it flags

- **Buzzwords** — delve, tapestry, robust, seamless, leverage, pivotal, myriad, harness, and the rest of the usual suspects.
- **Filler phrases** — "it's important to note", "at the end of the day", "when it comes to", "I hope this helps".
- **The "not just X, but Y" frame** and the "it isn't X, it's Y" flip.
- **Em-dash density** — one is fine; a cluster is a tell.
- **Emoji** in prose.
- **Flat rhythm** — sentences that are all suspiciously the same length.

Scores under 10 (per 1,000 words) read clean, 10–25 want a pass, 25+ need a real rewrite. The threshold is tunable with `--threshold`.

## Yes, running it on this README lights up

If you `unslop` this file it flags a pile of hits — because the section above quotes the exact buzzwords and phrases it hunts for, and one example literally pipes in "let's dive into it." The scanner can't tell a quoted example from the real use. This is the one file where the false positives are the whole point.

## Not a language cop

The word lists are opinions, not laws. If your field genuinely uses "robust" or "comprehensive" as terms of art, `--threshold` or a quick eyeball is your friend. The goal is to catch the reflexive version of these, the kind you didn't choose — not to ban words.

## License

MIT. Use it however you like.
