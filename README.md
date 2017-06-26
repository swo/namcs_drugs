# Cleaned-up NAMCS data

The [NAMCS](https://www.cdc.gov/nchs/ahcd/ahcd_questionnaires.htm) data is
useful, but the formats provided are definitely not useful: the CDC provides
them as fixed-width format files. Some of them are downloadable as Windows
`.exe` files. All the fields are encoded in way that requires consultation with
the documentation (e.g., one of the race variables uses the values `1` through
`4` as white, black, Hispanic, and other).

## Ways this data is nicer to work with

*I have a somewhat narrow research question.* So I parse only a subset of the fields.

*I parse the fields of interest into human-readable values.* E.g., `male` rather than `2`.

*I separate the data into three files.* The original data have one line per
visit/record. Each visit can have multiple diagnoses and drugs associated with
it. Each diagnosis has a probability; each drug has many variables associated
with it (e.g., the therapeutic categories of the drugs, whether they are new or
continued, etc.). There are variable numbers of diagnoses and drugs per visit
(i.e., not every visit has 3 diagnoses; not every visit has the maximum of 10
[or 30] drugs). With separate files, you can ask sensible questions, like,
"Which visits had an antibiotic prescribed?" by querying a single column of
data (rather than asking, did any of the variables from this list appear in any
of these 30 columns?).

## Files

I downloaded the documentation was from the [NAMCS website](ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NAMCS)

I downloaded the data in `csv` format from [NBER](http://www.nber.org/data/national-ambulatory-medical-care-survey.html) (rather than in fixed-width format from [NAMCS](ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NAMCS/)).

## Parsing the drug codes

The NAMCS data encodes drug ingredients using a special code list, which is
provided only in pdf pages, which is very unhelpful. I tried to clean up these
codes into useable lists. See the `drug_codes` directory for that.

## Notes on usage

NAMCS is a survey, so the patient weight and stratum variables are essential for analysis:

[Survey](https://stat.ethz.ch/pipermail/r-help/2005-October/080170.html)
