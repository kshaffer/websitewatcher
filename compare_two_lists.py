import csv
import json
from subprocess import call
import shlex
from subprocess import Popen, PIPE

# provide two files (cleaned by clean_url_list_wget.py)
# file1 should be the earlier scrape, file2 the later scrape

file1 = '2-8-test1.csv'
file2 = '2-8-test2.csv'

# provide filenames for outputs:
# filename for a list of URLs in both scrapes
# filename for a list of URLs new in second scrape
# filename for a list of URLs removed or unlinked between scrapes
# filename for a list of URLs changed between scrapes (CSV)

urls_in_both_filename = 'urls_in_both-wh-2-8.txt'
urls_in_1_only_filename = 'urls_in_1_only-wh-2-8.txt'
urls_in_2_only_filename = 'urls_in_1_only-wh-2-8.txt'
urls_changed_filename = 'urls_changed_wh_2_8_wayback.csv' # this one should be CSV!

# provide Wayback-Machine-formatted timestamp of the two scrapes
# 20170208163000 is Feb 8, 2017 (2017 02 08) at 4:30:00pm UTC (16 30 00)
# 20170208000000 is midnight on Feb 8, 2017, UTC
wayback_timestamp_earlier = 20170207163000
wayback_timestamp_later = 20170208163000


# To run script, you should not need to edit any of the code below

def read_csv(file):
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        rows = []
        for line in reader:
            row_data = []
            for element in line:
                row_data.append(element)
            rows.append(row_data)
    rows.pop(0)
    return(rows)

def write_to_csv(data, filename):
    with open(filename, 'w') as csvfile:
        w = csv.writer(csvfile, delimiter = ',')
        for row in data:
            try:
                w.writerow(row)
            except:
                print(row, 'not written to file.')
    print(filename, 'created.')

def write_to_text(data, filename):
    f = open(filename, 'w', encoding = 'utf-8')
    for line in data:
        f.write(line + '\n')
    f.close()

def snapshot_dictionary(snapshot):
    """
    creates a dictionary with URLs as keys and date-time of scrape as value
    """
    url = {}
    for record in snapshot:
        url[record[2]] = record[0] + ' ' + record[1]
    return(url)

def all_unique_urls(snapshot1, snapshot2):
    """
    returns a list of keys (URLs) that appear in one or both dictionaries, duplicates removed
    """
    urls = []
    for url in snapshot1.keys():
        urls.append(url)
    for url in snapshot2.keys():
        urls.append(url)
    return(set(urls))

def urls_in_both(snapshot1, snapshot2):
    """
    returns a list of keys (URLs) that appear in both dictionaries
    """
    unique = all_unique_urls(snapshot1, snapshot2)
    in_both = []
    for url in unique:
        if url in snapshot1.keys() and url in snapshot2.keys():
            in_both.append(url)
    return(in_both)

def urls_in_set_1_only(snapshot1, snapshot2):
    """
    returns a list of keys (URLs) that appear in one dictionary only (the one listed first)
    """
    unique = all_unique_urls(snapshot1, snapshot2)
    in_1_only = []
    for url in unique:
        if url in snapshot1.keys() and url not in snapshot2.keys():
            in_1_only.append(url)
    return(in_1_only)

def urls_in_set_2_only(snapshot1, snapshot2):
    """
    returns a list of keys (URLs) that appear in one dictionary only (the one listed second)
    """
    unique = all_unique_urls(snapshot1, snapshot2)
    in_2_only = []
    for url in unique:
        if url in snapshot2.keys() and url not in snapshot1.keys():
            in_2_only.append(url)
    return(in_2_only)

def get_stdout(cmd):
     """
     return the standard output of a shell command
     used in most_recent_wayback_change()
     """
     args = shlex.split(cmd)
     proc = Popen(args, stdout=PIPE, stderr=PIPE)
     out, err = proc.communicate()
     exitcode = proc.returncode
     return exitcode, out, err

def most_recent_wayback_change(url, timestamp):
    """
    queries the Wayback Machine to find the most recent change of a page
    *before* a given timestamp
    Not reliable at small time scales, as it reports a new capture on the WM,
    not necessarily a new page
    """
    ignore = []
    ignore.append('Remote file does not exist -- broken link!!!')
    ignore.append('unlink: No such file or directory')
    ignore.append('')
    check = get_stdout('wget --spider --no-verbose -e robots=off http://web.archive.org/web/' + timestamp + '/' + url)[2].decode('utf-8')
    url_object = 'NA'
    if check not in ignore:
        if 'Getting snapshot pages' not in check:
            try:
                if check.split(' ')[2] and check.split(' ')[2] == 'URL:' and check.split(' ')[4] and check.split(' ')[4] == '200':
                    url_object = check.split(' ')[3]
            except:
                try:
                    url_object = check.split(' ')[2].replace('URL:', '')
                except:
                    print(check, 'not parsed.')
                    url_object = 'NA'
            return(url_object.replace('http://web.archive.org/web/', '').split('/')[0])

def read_wayback_dump(filename):
    """
    reads and parses a text file of STDOUT from wayback_machine_downloader
    returns a list of lines with valid JSON output
    """
    ignore = []
    ignore.append('[')
    ignore.append(']')
    ignore.append('')
    f = open(filename, encoding='utf-8')
    table_original = []
    for line in f:
        line = line.rstrip('\n')
        if line not in ignore:
            if 'Getting snapshot pages' not in line:
                table_original.append(line.rstrip(','))
    return table_original

def extract_wayback_url_database(wayback_data_dump):
    """
    extracts information from the results of read_wayback_dump
    for each record in data, creates a dictionary record with the URL as key
    and the timestamp of page as the value
    """
    latest_timestamp = {}
    for article in wayback_data_dump:
        url = json.loads(article)['file_url']
        timestamp = json.loads(article)['timestamp']
        latest_timestamp[url] = timestamp
    return(latest_timestamp)

# read and parse data files produced by clean_url_list_wget.py
snapshot1 = snapshot_dictionary(read_csv(file1))
snapshot2 = snapshot_dictionary(read_csv(file2))

# find all URLs in both, one, or the other snapshot
unique_urls = all_unique_urls(snapshot1, snapshot2)
urls_in_both = urls_in_both(snapshot1, snapshot2)
urls_in_1_only = urls_in_set_1_only(snapshot1, snapshot2)
urls_in_2_only = urls_in_set_2_only(snapshot1, snapshot2)

# save results to text files
write_to_text(urls_in_both, urls_in_both_filename)
write_to_text(urls_in_1_only, urls_in_1_only_filename)
write_to_text(urls_in_2_only, urls_in_2_only_filename)

# for URLs in both snapshots, check the Wayback Machine to see when they most recently changed
# assemble a list of lists (urls_changed) containing the URL and most recent change
# for all URLs with a most recent change between the two provided timestamps
# write data to a CSV file

wayback_latest = extract_wayback_url_database(read_wayback_dump('wh-2017-02-08_wayback.txt'))
urls_changed = [['url', 'timestamp_of_change']]
for url in urls_in_both:
    if url in wayback_latest.keys():
        most_recent_change = wayback_latest[url]
    elif (url + '/') in wayback_latest.keys():
        most_recent_change = wayback_latest[url + '/']
    else:
        most_recent_change = 'NA'
    print(url, most_recent_change)
    if most_recent_change == 'NA':
        urls_changed.append([url, 'unable to retrieve data from Wayback Machine'])
    else:
        try:
            most_recent_change = int(most_recent_change)
            if most_recent_change <= wayback_timestamp_later and most_recent_change > (wayback_timestamp_earlier):
                urls_changed.append([url, most_recent_change])
        except:
            urls_changed.append([url, 'unable to retrieve data from Wayback Machine'])

write_to_csv(urls_changed, urls_changed_filename)
