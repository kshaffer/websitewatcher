library(jsonlite)
library(tidyverse)
library(lubridate)

# See URL instructions here: 
# https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server

# ed.gov
ed_gov <- fromJSON('http://web.archive.org/cdx/search/cdx?url=ed.gov&matchType=domain&output=json&collapse=digest')
colnames(ed_gov) <- ed_gov[1,]
ed <- as_tibble(ed_gov[-1,]) %>%
  mutate(date = ymd(substr(timestamp, 1, 8)))

ed %>%
  filter(date >= '2015-01-01',
         mimetype %in% c('text/html', 'text/plain', 'application/msword', 'application/pdf')) %>%
  mutate(time_floor = floor_date(date, unit = "1 month")) %>%
  group_by(time_floor, mimetype) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, color = mimetype)) +
  geom_line()

max(ed$date)

# whitehouse.gov
wh_gov <- fromJSON('http://web.archive.org/cdx/search/cdx?url=whitehouse.gov&matchType=domain&output=json&collapse=digest')
colnames(wh_gov) <- wh_gov[1,]
wh <- as_tibble(wh_gov[-1,]) %>%
  mutate(date = ymd(substr(timestamp, 1, 8)))

wh %>%
  filter(date >= '2016-01-01',
         mimetype %in% c('text/html', 'text/plain', 'application/msword', 'application/pdf')) %>%
  mutate(time_floor = floor_date(date, unit = "1 month")) %>%
  group_by(time_floor, mimetype) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, fill = mimetype)) +
  geom_bar(stat = 'identity')

max(wh$date)

# epa.gov
epa_gov <- fromJSON('http://web.archive.org/cdx/search/cdx?url=epa.gov&matchType=domain&output=json&collapse=digest')
colnames(epa_gov) <- epa_gov[1,]
epa <- as_tibble(epa_gov[-1,]) %>%
  mutate(date = ymd(substr(timestamp, 1, 8)))

epa_types <- epa %>%
  group_by(mimetype) %>%
  summarize(count = n()) 

epa %>%
  filter(date >= '2009-01-01',
         mimetype %in% c('text/html',
                         'application/octet-stream',
                         'warc/revisit',
                         'application/pdf',
                         'image/gif')) %>%
  mutate(time_floor = floor_date(date, unit = "1 month")) %>%
  group_by(time_floor, mimetype) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, fill = mimetype)) +
  geom_bar(stat = 'identity')

max(epa$date)
