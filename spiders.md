# Spider commands

## Download a list of URLs from a currently availabe website

```wget -r --spider -o wh-1-20-wget.txt --no-verbose -e robots=off https://www.whitehouse.gov```

## Download a list of URLs from a Wayback Machine snapshot

```wget -r --spider -o wh-1-20-wget.txt --no-verbose -e robots=off http://web.archive.org/web/20170120092900/https://www.whitehouse.gov/```

## Download a list of URLs and most-recent timestamps on a site from Wayback Machine

```wayback_machine_downloader -t 20170122000000 --list https://www.whitehouse.gov > ./wh-1-22-2017.txt```

The ```-t 20170122000000``` option tells the downloader only to consider versions created before midnight (```000000```) on January 20, 2017 (```20170120```).

*Note: If a page on the site links to a page no longer available, this list will return the most recent timestamp for that page. It will* ***not*** *tell you that the page is not part of the website as of that time.*