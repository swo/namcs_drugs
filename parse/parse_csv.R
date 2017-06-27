#!/usr/bin/env Rscript

# age=92 means age >= 92
# race is imputed

import::from(stringr, str_replace)

parse_year = function(year) {
  column_specs_fn = sprintf('column_specs_%i.tsv', year)
  input_fn = sprintf('raw/namcs%i.csv', year)
  visits_fn = sprintf('../namcs_visits_%i.tsv', year)
  dx_fn = sprintf('../namcs_dx_%i.tsv', year)
  drugs_fn = sprintf('../namcs_drugs_%i.tsv', year)

  column_specs = read_tsv(column_specs_fn)
  col_types = do.call(cols_only, setNames(as.list(column_specs$col_type), column_specs$col_name))

  value_at = function(x, options, outputs) outputs[match(x, options)]

  dat = read_csv(input_fn, col_types=col_types, na=character()) %>%
    setNames(column_specs$var_name) %>%
    mutate(sex=value_at(sex, c(1, 2), c('female', 'male')),
          race=value_at(race, c(1, 2, 3, 4), c('white', 'black', 'hispanic', 'other')),
          region=value_at(region, c(1, 2, 3, 4), c('northeast', 'midwest', 'south', 'west')),
          major_reason=value_at(major_reason, c(-9, 1, 2, 3, 4, 5), c('blank', 'new problem (<3 mos.)', 'chronic problem (routine)', 'chronic problem (flare)', 'pre/post-surgery', 'preventative')),
          any_medication=value_at(any_medication, c(0, 1, 2), c('no', 'yes', 'blank'))) %>%
    mutate_at(vars(medicare_payment, tobacco, asthma, copd, psa_test), as.logical) %>%
    mutate_at(vars(matches('rx.._continued')), function(x) value_at(x, c(-9, -8, -7, 1, 2, 3), c('blank', 'bad value (-8)', 'na (no drug)', 'new', 'continued', 'bad value ("new" and "continued" checked)'))) %>%
    mutate(n_chronic_conditions=case_when(between(.$n_chronic_conditions, 0, 11) ~ .$n_chronic_conditions,
                                          .$n_chronic_conditions == -9 ~ as.integer(NA))) %>%
    mutate(visit_id=1:nrow(.))

  visits = dat %>%
    select(-starts_with('rx'), -starts_with('dx')) %T>%
    write_tsv(visits_fn)

  str_match1 = function(x, pattern) stringr::str_match(x, pattern)[,2]
  drug_types = read_tsv('drug_codes/codes.tsv')

  drug = dat %>%
    select(visit_id, starts_with('rx')) %>%
    gather('raw_key', 'value', -visit_id) %>%
    mutate(rx_no=as.integer(str_match1(raw_key, 'rx(\\d\\d)')), key=str_match1(raw_key, 'rx\\d\\d_(.+)$')) %>%
    select(visit_id, rx_no, key, value) %>%
    spread(key, value) %>%
    filter(id != '') %>%
    left_join(drug_types, by='id') %T>% # remove blank entries
    write_tsv(drugs_fn)

  dx = dat %>%
    select(visit_id, dx1:dx3) %>%
    gather('dx_number', 'dx', -visit_id) %>%
    mutate(dx_number=as.integer(str_match1(dx_number, 'dx(.)'))) %>%
    filter(!(dx %in% c('-9', 'V997-'))) %T>% # remove blank/"healthy"/"none" entries
    write_tsv(dx_fn)
}

for (y in 2011:2014) parse_year(y)
