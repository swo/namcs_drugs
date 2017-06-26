#!/usr/bin/env Rscript

f = function(year_fn, y) read_tsv(sprintf('codes%s.tsv', year_fn)) %>% mutate(year=as.integer(y))

bind_rows(f('2011', 2011), f('2012', 2012), f('2013', 2013),
          f('2014_pt1', 2014), f('2014_pt2', 2014)) %>%
  select(year, code, desc, doc_page) %>%
  arrange(code, year, doc_page) %>%
  write_tsv('codes.tsv')
