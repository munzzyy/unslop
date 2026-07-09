# Human corpus sources

16 verbatim excerpts of genuinely human-written prose, used as the human half of the
detector eval. Files 01-14 are US public domain (published before 1930), fetched from
Project Gutenberg plain-text editions with the Gutenberg header/footer boilerplate
stripped. Files 15-16 are documentation from permissively licensed open-source
projects, fetched at pre-2018 tags.

| File | Author | Title | Year | Source | License / status |
|------|--------|-------|------|--------|------------------|
| 01-essay-twain.txt | Mark Twain | "Taming the Bicycle" (from *What Is Man? and Other Essays*) | written c. 1893, collection publ. 1917 | https://www.gutenberg.org/cache/epub/70/pg70.txt | US public domain |
| 02-essay-thoreau.txt | Henry David Thoreau | *Walden* ("Where I Lived, and What I Lived For") | 1854 | https://www.gutenberg.org/cache/epub/205/pg205.txt | US public domain |
| 03-essay-james.txt | William James | *Pragmatism*, Lecture I | 1907 | https://www.gutenberg.org/cache/epub/5116/pg5116.txt | US public domain |
| 04-fiction-cather.txt | Willa Cather | *My Ántonia* (Introduction) | 1918 | https://www.gutenberg.org/cache/epub/242/pg242.txt | US public domain |
| 05-fiction-london.txt | Jack London | *The Call of the Wild*, Chapter I | 1903 | https://www.gutenberg.org/cache/epub/215/pg215.txt | US public domain |
| 06-fiction-wharton.txt | Edith Wharton | *Ethan Frome* (frame narrative) | 1911 | https://www.gutenberg.org/cache/epub/4517/pg4517.txt | US public domain |
| 07-journalism-bly.txt | Nellie Bly | *Ten Days in a Mad-House*, Chapter I | 1887 | https://www.gutenberg.org/files/59899/59899-0.txt | US public domain |
| 08-journalism-riis.txt | Jacob A. Riis | *How the Other Half Lives*, Chapter I ("Genesis of the Tenement") | 1890 | https://www.gutenberg.org/cache/epub/45502/pg45502.txt | US public domain |
| 09-letters-stewart.txt | Elinore Pruitt Stewart | *Letters of a Woman Homesteader*, Letter I | 1914 | https://www.gutenberg.org/cache/epub/16623/pg16623.txt | US public domain |
| 10-memoir-grant.txt | Ulysses S. Grant | *Personal Memoirs of U. S. Grant* (Preface) | 1885 | https://www.gutenberg.org/cache/epub/4367/pg4367.txt | US public domain |
| 11-practical-child.txt | Lydia Maria Child | *The American Frugal Housewife* (Introductory Chapter) | 1832 | https://www.gutenberg.org/cache/epub/13493/pg13493.txt | US public domain |
| 12-practical-farmer.txt | Fannie Merritt Farmer | *The Boston Cooking-School Cook Book* ("Correct Proportions of Food") | 1896 (1910 ed.) | https://www.gutenberg.org/cache/epub/65061/pg65061.txt | US public domain |
| 13-science-darwin.txt | Charles Darwin | *On the Origin of Species*, Chapter III ("Struggle for Existence") | 1859 | https://www.gutenberg.org/cache/epub/1228/pg1228.txt | US public domain |
| 14-science-faraday.txt | Michael Faraday | *The Chemical History of a Candle*, Lecture I | 1861 | https://www.gutenberg.org/cache/epub/14474/pg14474.txt | US public domain |
| 15-docs-rails.txt | Rails core team | Ruby on Rails README, tag v5.0.0 | 2016 | https://raw.githubusercontent.com/rails/rails/v5.0.0/README.md | MIT License. The excerpt is the full README, including its own license section ("Ruby on Rails is released under the MIT License"). |
| 16-docs-cpython.txt | Python core developers | CPython README, tag v2.7.9 | 2014 | https://raw.githubusercontent.com/python/cpython/v2.7.9/README | PSF License (permissive, BSD-style). The excerpt keeps the file's own copyright and license-information section. |
| 17-law-civil-code-ru.txt | Russian Federation (legislature) | Civil Code of the Russian Federation, Part One, Articles 1-3 | enacted 1994, current text as amended | https://www.consultant.ru/document/cons_doc_LAW_5142/ (Articles 1-3; cross-checked against independent legal-database mirrors of the same statute, e.g. https://sudact.ru/law/gk-rf-chast1/razdel-i/podrazdel-1/glava-1/) | Official text of a Russian federal law - not protected by copyright under Article 1259 of this very Code, which excludes official documents of state bodies (laws, court decisions, and other official texts) from copyright. Added in 0.9.0 as the corpus's first non-English human sample: formal/bureaucratic Russian legal prose is exactly the register the 0.9.0 Russian buzzword and "является"-density additions needed a false-positive check against, and this text is genuinely public domain rather than a paraphrase written to order. |

Notes:

- 17-law-civil-code-ru.txt is quoted, not paraphrased, but assembled from
  three separate articles of the same statute (1, 2, 3) rather than one
  continuous passage - flagged here as the one exception to the
  single-continuous-passage rule below, and noted because statute articles
  are numbered, freestanding units by design, unlike a cut mid-paragraph.

- Every excerpt is a single continuous passage, copied verbatim from the fetched
  source. No stitching, no paraphrase.
- Project Gutenberg's trademark license attaches to redistributing their files with
  the PG branding; the underlying pre-1930 texts are public domain in the US, and the
  excerpts here carry none of the PG boilerplate.
- 02-essay-thoreau.txt ends at "without a wheelbarrow." — the source paragraph
  continues into a verse quotation, which was cut at the sentence boundary.
