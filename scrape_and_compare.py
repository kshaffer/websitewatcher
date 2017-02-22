import csv
import json
from subprocess import call
import shlex
from subprocess import Popen, PIPE
import requests
import sys
import datetime

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
    """
    writes a list of strings into a text file
    """
    f = open(filename, 'w', encoding = 'utf-8')
    for line in data:
        f.write(line + '\n')
    f.close()

def extract_url_database(filename, date_check):
    f = open(filename, encoding='utf-8')
    table_original = []
    for line in f:
        line = line.rstrip('\n')
        if line.split(' ')[0] == date_check:
            table_original.append(line)

    url_list = [['date_scraped', 'time_scraped', 'url']]
    for article in table_original:
        url_object = []
        article_data = article.split(' ')
        url_object.append(article_data[0])
        url_object.append(article_data[1])
        if article_data[2] and article_data[2] == 'URL:' and article_data[4] == '200':
            url_object.append(article_data[3])
        else:
            try:
                url_object.append(article_data[2].replace('URL:', ''))
            except:
                print(article_data)
        url_list.append(url_object)
    return(url_list)

site_to_scrape = sys.argv[1]
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
previous_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
scrape_output_filename = 'source_data/' + site_to_scrape + '/' + site_to_scrape + '-' + current_date + '.txt'
clean_output_filename = 'clean_data/' + site_to_scrape + '/' + site_to_scrape + '-' + current_date + '.csv'

# scrape a URL list from the site uwing wget
scrape_data = get_stdout('wget -r -l 20 --spider --no-verbose -e robots=off https://www.' + site_to_scrape)[2].decode('utf-8')
write_to_text([scrape_data], scrape_output_filename)

# write list to text file, one URL per line, for each scrape
write_to_csv(extract_url_database([scrape_data], current_date), clean_output_filename)
