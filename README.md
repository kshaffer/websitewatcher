# websitewatcher

Scrape list of URLs contained on a website on a regular basis and compare lists for new/deleted/changed pages.

## Spider commands

Begin the process by using a spider to download a URL list for a site. For optimal performance, I recommend using ```wget``` on a current site on a regular basis. If you need to compare to old versions you didn't scrape, or if a site blocks spiders or has a Terms of Service that does not allow spiders, you can use ```wget``` on a Wayback Machine snapshot (slow) or the Ruby gem ```wayback_machine_downloader``` (see caveat below).

 To download a list of URLs from a currently available website, such as whitehouse.gov:

```wget -r --spider -o output_filename.txt --no-verbose -e robots=off https://www.whitehouse.gov```

To download a list of URLs from a Wayback Machine snapshot:

```wget -r --spider -o output_filename.txt --no-verbose -e robots=off http://web.archive.org/web/20170120092900/https://www.whitehouse.gov/```

To download a list of URLs and most-recent timestamps on a site from Wayback Machine:

```wayback_machine_downloader -t 20170122000000 --list https://www.whitehouse.gov > ./output_filename.txt```

The ```-t 20170122000000``` option tells the downloader only to consider versions created before midnight (```000000```) on January 20, 2017 (```20170120```).

*Note: If a page on the site links to a page no longer available, this list will return the most recent timestamp for that page. It will* ***not*** *tell you that the page is not part of the website as of that time.*

## Clean URL list

Once you have a text file containing the results of a ```wget``` spider process (above), use ```clean_url_list_wget.py``` to convert the text output into a clean, machine-readable CSV file. Edit the filenames at the top of the script before running.

## Get timestamps of page changes from the Wayback Machine

Use the above spider command to download timestamps for page changes using ```wayback_machine_downloader```. The timestamp put in the script should be the timestamp of the second scrape. Format: ```YYYYMMDDHHMMSS``` (UTC time).

## Compare two URL lists

When you have cleaned the URL list output of two different spider processes on a site and the Wayback Machine timestamps, use ```compare_two_lists.py``` to check for which URLs are in both sites, added or deleted between sites, and then check the Wayback Machine to see if any of the URLs in both sites have changed. Will output text files for each of those checks. Edit the filenames and timestamps at the top of the script before running.

## To do

- Deepen the levels of scraping for the spider scripts, re-run on whitehouse.gov to test.  
- Create a script that will take the output of a scrape comparison and make it into a Jekyll/GitHub Pages blog post.  
- Add a shell script to make the entire process more automatic.  
- Add a cron job to run the process regularly on multiple websites and automatically publish blog posts.  
- Test on other sites and refine the model.  
- Optimize/troubleshoot the diff-checking process.
