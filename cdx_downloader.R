library(jsonlite)
library(tidyverse)
library(lubridate)

# See URL instructions here: 
# https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server

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
