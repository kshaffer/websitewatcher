library(tidyverse)
library(lubridate)

ed <- read_csv('ed.gov/ed_gov_wayback_2017-02-09_parsed.csv') %>%
  mutate(date = ymd(paste(substr(as.character(date_time), 1, 4),
                          '-',
                          substr(as.character(date_time), 5, 6),
                          '-',
                          substr(as.character(date_time), 7, 8),
                          sep = ''
  ))) %>%
  select(url, date, extension)

unique(ed$extension)

tyoe_count <- ed %>%
  group_by(extension) %>%
  summarise(count = n()) %>%
  mutate(extension = reorder(extension, count))

ed %>%
  filter(date > '2015-01-01',
         extension %in% c('html', 'doc', 'pdf', 'xls')) %>%
  mutate(time_floor = floor_date(date, unit = "1 month")) %>%
  group_by(time_floor, extension) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, fill = extension)) +
  geom_col() +
  xlab('date') +
  ylab('pages added or changed') +
  ggtitle('Page additions and changes found by the Wayback Machine on ed.gov')

ed %>%
  filter(date > '2011-01-01',
         extension %in% c('html', 'doc', 'pdf', 'xls')) %>%
  #mutate(time_floor = floor_date(date, unit = "1 day")) %>%
  ggplot(aes(date, fill = extension)) +
  geom_bar()
