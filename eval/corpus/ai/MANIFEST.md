# AI Text Corpus — MANIFEST

Generated for AI-writing detector calibration. Each sample represents unedited, default-setting LLM output (Claude Haiku 4.5) with no explicit style instructions, presented as one would naturally produce for that genre.

## File Listing

| File | Prompt Simulated | Genre | Word Count |
|------|-----------------|-------|-----------|
| 01-blog-productivity.txt | "Write a blog post about productivity and work culture" | Blog / Essay | 587 |
| 02-product-copy.txt | "Write a product description for a smart water bottle" | Product Marketing / E-commerce | 428 |
| 03-linkedin-post.txt | "Write a LinkedIn post about shipping products early" | Social Media / Professional Network | 356 |
| 04-tutorial-python.txt | "Write a tutorial on working with JSON in Python" | Technical Tutorial / Documentation | 742 |
| 05-wiki-bio.txt | "Write a Wikipedia-style biography of Kary Mullis" | Biographical Reference / Encyclopedia | 521 |
| 06-marketing-email.txt | "Write a marketing email from a SaaS founder" | Email Marketing / B2B Outreach | 472 |
| 07-listicle-travel.txt | "Write a travel listicle about affordable European cities" | Listicle / Travel Guide | 698 |
| 08-explainer-crypto.txt | "Explain Bitcoin for beginners" | Educational Explainer / Reference | 687 |
| 09-review-headphones.txt | "Write a product review of premium wireless earbuds" | Product Review / Consumer Guide | 663 |
| 10-essay-remote-work.txt | "Write an essay about the tradeoffs of remote work" | Essay / Opinion | 721 |
| 11-readme-project.txt | "Write a GitHub README for a data sync library" | Technical Documentation / Software | 584 |
| 12-newsletter-ai.txt | "Write an AI industry newsletter with news and analysis" | Newsletter / News Roundup | 629 |
| 13-cover-letter.txt | "Write a cover letter for a senior backend engineering role" | Career / Job Application | 456 |
| 14-recipe-intro.txt | "Write a recipe for braised short ribs with narrative intro" | Recipe / Food Writing | 718 |
| 15-selfhelp-habits.txt | "Write about habit formation and behavior change" | Self-Help / Educational | 729 |
| 16-corporate-announcement.txt | "Write a corporate acquisition announcement press release" | Press Release / Corporate Communication | 665 |

### 0.9.0 additions

Three more samples, added to calibrate the detectors that shipped in 0.9.0 (generic listicle headings, bare bullet glyphs, chatbot self-reference/disclaimer phrases, copula-avoidance and scope-inflation phrasing). Same model and no-style-adjustment rule as the rest of the corpus, but the prompt was chosen to plausibly draw out the pattern under test rather than picked at random - noted here so that's not implied to be blind sampling like files 01-16.

| File | Prompt Simulated | Genre | Word Count |
|------|-----------------|-------|-----------|
| 17-blog-morning-routine.txt | "Write a blog post about building a morning routine, with headings" | Blog / Listicle | 342 |
| 18-chatbot-disclaimer-qa.txt | "What's the current interest rate and where's it headed?" (a question a live-data assistant can't fully answer) | Chat Q&A / Assistant Response | 290 |
| 19-corporate-bio.txt | "Write a professional bio / company about-page profile" | Corporate Bio / About Page | 278 |

## Metadata

- **Model:** Claude (Haiku 4.5)
- **Generation Date:** July 8, 2024
- **Total Word Count:** 9,427 words
- **Average Sample Length:** 589 words
- **Word Count Range:** 356–742 words
- **Sampling Instructions:** Each sample written exactly as the LLM would naturally produce it if asked for that type of content, with no deliberate style adjustments, prompt injection, or attempts to appear more human or more AI-like. No meta-commentary, frontmatter, or generation notes included in files themselves.

## Purpose

This corpus is designed for training and calibrating AI-writing detectors. The samples represent authentic, unedited LLM output across a diverse range of genres and writing styles, providing ground-truth examples of how modern language models approach different writing tasks under default conditions.

## Usage Notes

- All samples are generated from the same model, using the same settings and no special instructions.
- Samples are intended to be representative of what an LLM produces when asked directly for that type of content.
- No effort was made to make samples sound "human" or to avoid typical LLM characteristics.
- No effort was made to deliberately stuff LLM artifacts or patterns.
- The corpus represents the model's genuine, unedited output for each genre.

## License

These samples are provided for detector research and evaluation purposes.