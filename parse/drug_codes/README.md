# List of Multum drug codes

The NAMCS documentation for each year includes a list of "Generic codes and
names". (This was Appendix III for 2011-2014.) Unfortunately, these are all in
a pdf, which makes them hard to use. I used some scripts, included here,
followed by manual parsing and correction, to create a tsv list.

## Why are there multiple years?

Each NAMCS data year has its own documentation. Mercifully, the codes are the
same across all the years, which I confirmed by comparing the results of
running this pipeline on each year.

## The pipeline

1. Extract the generic codes pages from each pdf with `pdftk docXXXX.pdf cat YYY-ZZZ output generic_codesXXXX.pdf`, where `YYY` and `ZZZ` are the page ranges for Appendix III.
2. Run `pdftotext` on each generic codes pdf.
3. Use `parse_flat.py` to parse the 2011, 2012, and 2013 codes.
4. Use `collate.R` to stitch them together.

Unfortunately, a few pages of the 2014 codes remain in layout format, even when
calling `pdftotext` without `--layout`. For those pages, I used the use
`parse_flat.py` to parse most of the pages and `parse_layout.py` to parse the
weird remaining pages.

It also seems like some parts of the 2013 codes got mis-parsed. Some codes in
different years also ended up with the page numbers in the descriptions.

I manually corrected codes for differences in abbreviations (e.g., `APAP` used
for `ACETAMINOPHEN`), line breaks, and hyphenations.
