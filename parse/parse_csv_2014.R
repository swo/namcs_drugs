#!/usr/bin/env Rscript

# age=92 means age >= 92
# race is imputed

import::from(stringr, str_replace)

column_specs = read_tsv('column_specs_2014.tsv')
col_types = do.call(cols_only, setNames(as.list(column_specs$col_type), column_specs$col_name))

#drug_codes = read_tsv('../drug-codes/drug-codes.tsv', col_types='cc')

#extract_number = function(x) as.integer(regmatches(x, regexpr('\\d+', x)))

value_at = function(x, options, outputs) outputs[match(x, options)]

rx_continued_f = function(x) {
  case_when(x == -9 ~ 'blank',
            x == -8 ~ 'bad value (-8)',
            x == -7 ~ 'not applicable (no drug)',
            x == 1 ~ 'new',
            x == 2 ~ 'continued')
}

dat = read_csv('raw/namcs2014.csv', col_types=col_types, na=character()) %>%
  setNames(column_specs$var_name) %>%
  mutate(sex=value_at(sex, c(1, 2), c('female', 'male')),
         race=value_at(race, c(1, 2, 3, 4), c('white', 'black', 'hispanic', 'other')),
         major_reason=value_at(major_reason, c(-9, 1, 2, 3, 4, 5), c('blank', 'new problem (<3 mos.)', 'chronic problem (routine)', 'chronic problem (flare)', 'pre/post-surgery', 'preventative')),
         any_medication=value_at(any_medication, c(0, 1, 2), c('no', 'yes', 'blank'))) %>%
  mutate_at(vars(medicare_payment, tobacco, asthma, copd, psa_test), as.logical) %>%
  mutate_at(vars(matches('rx.._continued')), function(x) value_at(x, c(-9, -8, -7, 1, 2), c('blank', 'bad value (-8)', 'na (no drug)', 'new', 'continued'))) %>%
  mutate(n_chronic_conditions=case_when(between(.$n_chronic_conditions, 0, 11) ~ .$n_chronic_conditions,
                                        .$n_chronic_conditions == -9 ~ as.integer(NA))) %>%
  mutate(visit_id=1:nrow(.))

visits = dat %>%
  select(-starts_with('rx'), -starts_with('dx')) %T>%
  write_tsv('namcs_2014_visits.tsv')

str_match1 = function(x, pattern) stringr::str_match(x, pattern)[,2]

drugs = dat %>%
  select(visit_id, starts_with('rx')) %>%
  gather('raw_key', 'value', -visit_id) %>%
  mutate(rx_no=as.integer(str_match1(raw_key, 'rx(\\d\\d)')), key=str_match1(raw_key, 'rx\\d\\d_(.+)$')) %>%
  select(visit_id, rx_no, key, value) %>%
  spread(key, value) %>%
  filter(id != '') %T>% # remove blank entries
  write_tsv('namcs_2014_drugs.tsv')

dx = dat %>%
  select(visit_id, dx1:dx3) %>%
  gather('dx_number', 'dx', -visit_id) %>%
  mutate(dx_number=as.integer(str_match1(dx_number, 'dx(.)'))) %>%
  filter(!(dx %in% c('-9', 'V997-'))) %T>% # remove blank/"healthy"/"none" entries
  write_tsv('namcs_2014_dx.tsv')
