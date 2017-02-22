library(jsonlite)
library(tidyverse)
library(lubridate)
library(magrittr
        )

# See URL instructions here: 
# https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server

# download datasets
ed_gov <- fromJSON('http://web.archive.org/cdx/search/cdx?url=ed.gov&matchType=domain&output=json&collapse=digest')
wh_gov <- fromJSON('http://web.archive.org/cdx/search/cdx?url=whitehouse.gov&matchType=domain&output=json&collapse=digest')
epa_gov <- fromJSON('http://web.archive.org/cdx/search/cdx?url=epa.gov&matchType=domain&output=json&collapse=digest')
fcc_gov <- fromJSON('http://web.archive.org/cdx/search/cdx?url=fcc.gov&matchType=domain&output=json&collapse=digest')
nps_gov <- fromJSON('http://web.archive.org/cdx/search/cdx?url=nps.gov&matchType=domain&output=json&collapse=digest')
usda_gov <- fromJSON('http://web.archive.org/cdx/search/cdx?url=usda.gov&matchType=domain&output=json&collapse=digest')
wapo <- fromJSON('http://web.archive.org/cdx/search/cdx?url=washingtonpost.com&matchType=domain&output=json&collapse=digest')
target <- fromJSON('http://web.archive.org/cdx/search/cdx?url=target.com&matchType=domain&output=json&collapse=digest')
smt <- fromJSON('http://web.archive.org/cdx/search/cdx?url=societymusictheory.org&matchType=domain&output=json&collapse=digest')
nyt <- fromJSON('http://web.archive.org/cdx/search/cdx?url=nytimes.com&matchType=domain&output=json&collapse=digest')
aspca <- fromJSON('http://web.archive.org/cdx/search/cdx?url=aspca.org&matchType=domain&output=json&collapse=digest')
pt <- fromJSON('http://web.archive.org/cdx/search/cdx?url=psychologytoday.com&matchType=domain&output=json&collapse=digest')

# make all the sites
govsites <- ed_gov[-1,] %>%
  as_tibble() %>%
  select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
  filter(statuscode == '200') %>%
  mutate(site = 'ed.gov') %>%
  full_join(wh_gov[-1,] %>%
              as_tibble() %>%
              select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
              filter(statuscode == '200') %>%
              mutate(site = 'whitehouse.gov')) %>%
  full_join(epa_gov[-1,] %>%
              as_tibble() %>%
              select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
              filter(statuscode == '200') %>%
              mutate(site = 'epa.gov')) %>%
  full_join(fcc_gov[-1,] %>%
              as_tibble() %>%
              select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
              filter(statuscode == '200') %>%
              mutate(site = 'fcc.gov')) %>%
  full_join(nps_gov[-1,] %>%
              as_tibble() %>%
              select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
              filter(statuscode == '200') %>%
              mutate(site = 'nps.gov')) %>%
  full_join(usda_gov[-1,] %>%
              as_tibble() %>%
              select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
              filter(statuscode == '200') %>%
              mutate(site = 'usda.gov')) %>%
  mutate(date = ymd(substr(timestamp, 1, 8)))

comparesites <- wapo[-1,] %>%
  as_tibble() %>%
  select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
  filter(statuscode == '200') %>%
  mutate(site = 'Washington Post') %>%
  full_join(target[-1,] %>%
              as_tibble() %>%
              select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
              filter(statuscode == '200') %>%
              mutate(site = 'Target')) %>%
  full_join(smt[-1,] %>%
              as_tibble() %>%
              select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
              filter(statuscode == '200') %>%
              mutate(site = 'Society for Music Theory')) %>%
  full_join(aspca[-1,] %>%
              as_tibble() %>%
              select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
              filter(statuscode == '200') %>%
              mutate(site = 'ASPCA')) %>%
  full_join(nyt[-1,] %>%
              as_tibble() %>%
              select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
              filter(statuscode == '200') %>%
              mutate(site = 'NY Times')) %>%
  full_join(pt[-1,] %>%
              as_tibble() %>%
              select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7) %>%
              filter(statuscode == '200') %>%
              mutate(site = 'Psychology Today')) %>%
  mutate(date = ymd(substr(timestamp, 1, 8)))

# plot all additions/changes over time, by month
# split by site
govsites %>%
  mutate(time_floor = floor_date(date, unit = "1 month")) %>%
  group_by(time_floor, site) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, color = site)) +
  geom_line() +
  xlab('Date') +
  ylab('Pages added or changed') +
  ggtitle(paste('Page additions and changes found by the Wayback Machine on .gov sites, by month', sep = ''))

# plot all additions/changes over time, by day
# split by site
govsites %>%
  filter(date >= '2017-01-01') %>%
  mutate(time_floor = floor_date(date, unit = "1 day")) %>%
  group_by(time_floor, site) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, color = site)) +
  geom_line() +
  xlab('Date (2017)') +
  ylab('Pages added or changed') +
  ggtitle(paste('Page additions and changes found by the Wayback Machine on .gov sites, by day', sep = ''))

# comparison sites
comparesites %>%
  mutate(time_floor = floor_date(date, unit = "1 month")) %>%
  group_by(time_floor, site) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, color = site)) +
  geom_line() +
  xlab('Date') +
  ylab('Pages added or changed') +
  ggtitle(paste('Page additions and changes found by the Wayback Machine on comparison sites, by month', sep = ''))

comparesites %>%
  filter(date >= '2017-01-01') %>%
  mutate(time_floor = floor_date(date, unit = "1 day")) %>%
  group_by(time_floor, site) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, color = site)) +
  geom_line() +
  xlab('Date (2017)') +
  ylab('Pages added or changed') +
  ggtitle(paste('Page additions and changes found by the Wayback Machine on comparison sites, by day', sep = ''))

    
# single site analysis
# assign site
site <- usda_gov
site_name <- 'usda.gov'

# make first row of JSON output into header
# convert timestamp to date
testsite <- as_tibble(site[-1,]) %>%
  select(urlkey = 1, timestamp = 2, original = 3, mimetype = 4, statuscode = 5, digest = 6, length = 7)

site <- as_tibble(site[-1,]) %>%
  filter(statuscode == '200') %>%
  mutate(date = ymd(substr(timestamp, 1, 8)))

# what are the earliest and latest dates in the dataset
min(site$date)
max(site$date)

# what are the most common file types in the dataset
site_types <- site %>%
  group_by(mimetype) %>%
  summarize(count = n()) 

# plot all additions/changes over time, by month
# change '1 month' to '1 day' to plot by day instead
site %>%
  mutate(time_floor = floor_date(date, unit = "1 month")) %>%
  group_by(time_floor, statuscode) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, fill = statuscode)) +
  geom_col() +
  theme(legend.position="none") +
  xlab('date') +
  ylab('pages added or changed') +
  ggtitle(paste('Page additions and changes found by the Wayback Machine on ', site_name, ', by month', sep = ''))


# plot all additions/changes since given date, by month
# change '1 month' to '1 day' to plot by day instead
site %>%
  filter(date >= '2016-01-01') %>%
  mutate(time_floor = floor_date(date, unit = "1 month")) %>%
  group_by(time_floor, statuscode) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, fill = statuscode)) +
  geom_col() +
  theme(legend.position="none") +
  xlab('date') +
  ylab('pages added or changed') +
  ggtitle(paste('Page additions and changes found by the Wayback Machine on ', site_name, ', by month', sep = ''))


# plot all additions/changes since given date by month
# separate by file type
# limit by start date and file type
# change '1 month' to '1 day' to plot by day instead
site %>%
  filter(date >= '2014-01-01',
         mimetype %in% c('text/html', 'text/plain', 'application/msword', 'application/pdf')) %>%
  mutate(time_floor = floor_date(date, unit = "1 month")) %>%
  group_by(time_floor, mimetype) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, fill = mimetype)) +
  geom_bar(stat = 'identity') +
  xlab('date') +
  ylab('pages added or changed') +
  ggtitle(paste('Page additions and changes found by the Wayback Machine on ', site_name, ', by month', sep = ''))

# plot comparison of file types
# limit by list of file types
# change '1 month' to '1 day' to plot by day instead
site %>%
  filter(mimetype %in% c('text/html', 'text/plain', 'application/msword', 'application/pdf')) %>%
  mutate(time_floor = floor_date(date, unit = "1 month")) %>%
  group_by(time_floor, mimetype) %>%
  summarize(count = n()) %>%
  ggplot(aes(time_floor, count, color = mimetype)) +
  geom_line(stat = 'identity') +
  xlab('date') +
  ylab('pages added or changed') +
  ggtitle(paste('Page additions and changes found by the Wayback Machine on ', site_name, ', by month', sep = ''))

# which urls changed the most in the site's history
site %>%
  count(urlkey, sort=TRUE) %>%
  filter(n > 500) %>%
  mutate(urlkey = reorder(urlkey, n)) %>%
  ggplot(aes(urlkey, n, fill = urlkey)) +
  geom_bar(stat = 'identity') +
  xlab('page') +
  ylab('number of times changed') +
  ggtitle(paste('Most frequently changed pages in Wayback Machine archive of ', site_name, sep = '')) +
  theme(legend.position="none") +
  coord_flip()

   
# which urls changed the most since a start date
start_date <- '2017-01-20'
site %>%
  filter(date >= start_date) %>%
  count(urlkey, sort=TRUE) %>%
  filter(n > 10) %>%
  mutate(urlkey = reorder(urlkey, n)) %>%
  ggplot(aes(urlkey, n, fill = urlkey)) +
  geom_bar(stat = 'identity') +
  xlab('page') +
  ylab('number of times changed') +
  ggtitle(paste('Most frequently changed pages in Wayback Machine archive of ', site_name, ' since ', start_date, '.', sep = '')) +
  theme(legend.position="none") +
  coord_flip()

