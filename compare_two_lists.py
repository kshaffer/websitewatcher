# run program with the following command-line options
#
# python compare_two_lists.py whitehouse 2017-02-08 2017-02-14
#
# This compares the whitehouse.gov (with prefix 'wh') from
# Feb 8, 2017, and Feb 14, 2017

import csv
import json
from subprocess import call
import shlex
from subprocess import Popen, PIPE
import requests
import sys

if len(sys.argv) > 3:
    source_site = sys.argv[1]
    date_earlier = sys.argv[2]
    date_later = sys.argv[3]
else:
    # if not using command-line arguments:
    # provide a website name, data source location,
    # data output location, and two dates to compare
    source_site = 'wh'
    date_earlier = '2017-02-08'
    date_later = '2017-02-14'

source_folder = 'clean_data/'
output_folder = 'output_data/'


# To run script, you should not need to edit any of the code below

# construct filenames for cleaned URL lists
file1 = source_folder + source_site + '-' + date_earlier + '.csv'
file2 = source_folder + source_site + '-' + date_later + '.csv'

# construct filenames for outputs
urls_in_both_filename = output_folder + source_site + '-' + date_later + '-' + 'urls_in_both' + '.txt'
urls_in_1_only_filename = output_folder + source_site + '-' + date_later + '-' + 'urls_in_1_only' + '.txt'
urls_in_2_only_filename = output_folder + source_site + '-' + date_later + '-' + 'urls_in_2_only' + '.txt'
urls_unlinked_filename = output_folder + source_site + '-' + date_later + '-' + 'urls_unlinked' + '.txt'


def read_csv(file):
    """
    reads a CSV file into a list of lists
    """
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        rows = []
        for line in reader:
            row_data = []
            for element in line:
                row_data.append(element)
            if row_data != []:
                rows.append(row_data)
    rows.pop(0)
    return(rows)

def write_to_csv(data, filename):
    """
    writes a list of lists into a CSV file
    """
    with open(filename, 'w') as csvfile:
        w = csv.writer(csvfile, delimiter = ',')
        for row in data:
            try:
                w.writerow(row)
            except:
                print(row, 'not written to file.')
    print(filename, 'created.')

def write_to_text(data, filename):
    """
    writes a list of strings into a text file
    """
    f = open(filename, 'w', encoding = 'utf-8')
    for line in data:
        f.write(line + '\n')
    f.close()

def snapshot_dictionary(snapshot):
    """
    takes a cleaned URL list from wget and
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

# read and parse data files produced by clean_url_list_wget.py
snapshot1 = snapshot_dictionary(read_csv(file1))
snapshot2 = snapshot_dictionary(read_csv(file2))

# find all URLs in both, one, or the other snapshot
unique_urls = all_unique_urls(snapshot1, snapshot2)
urls_in_both = urls_in_both(snapshot1, snapshot2)
urls_in_1_only = urls_in_set_1_only(snapshot1, snapshot2)
urls_in_2_only = urls_in_set_2_only(snapshot1, snapshot2)

# for URLs only in the scrape of the earlier snapshot, use
# requests to check whether each indivudual URL still exists on site
# create list of URLs still present, but *possibly* unlinked from site
# (i.e., URL still exists, but wget couldn't find it)

urls_in_1_only_cleaned = []
urls_unlinked = []

for url in urls_in_1_only:
    if '.js' not in url:
        if requests.get(url).status_code == 200:
            urls_unlinked.append(url)
        else:
            urls_in_1_only_cleaned.append(url)

# save results to text files
write_to_text(urls_in_both, urls_in_both_filename)
write_to_text(urls_in_1_only_cleaned, urls_in_1_only_filename)
write_to_text(urls_in_2_only, urls_in_2_only_filename)
write_to_text(urls_unlinked, urls_unlinked_filename)