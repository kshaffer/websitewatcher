import json
import csv

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
    db = [['url', 'date_time', 'extension']]
    for article in wayback_data_dump:
        record_data = []
        url = json.loads(article)['file_url']
        timestamp = json.loads(article)['timestamp']
        try:
            url_split = url.split('.')
            if len(url_split) > 3:
                extension = url_split[len(url_split) - 1].split('?')[0].split('#')[0].split('%')[0].split('&')[0].split('(')[0].split(':')[0]#.split('/')[0]
                try:
                    int(extension)
                    extension = 'html'
                except:
                    x = 'all good'
                if extension in ['htmlf', 'jhtml', 'htm', 'scrollable', 'edu', "html'", 'gallery', '+of+education', 'w52', 'dummy', 'htmlPress', '3f!=', '1R', 'src', 'net']:
                    extension = 'html'

            else:
                extension = 'html'
        except:
            extension = 'html'
        extension = extension.lower()
        record_data.append(url)
        record_data.append(timestamp)
        record_data.append(extension)
        db.append(record_data)
    return(db)

def write_to_csv(data, filename):
    with open(filename, 'w') as csvfile:
        w = csv.writer(csvfile, delimiter = ',')
        for row in data:
            try:
                w.writerow(row)
            except:
                print(row, 'not written to file.')
    print(filename, 'created.')

write_to_csv(extract_wayback_url_database(read_wayback_dump('test_data/ed_gov_wayback_2_9_2017.txt')), 'test_data/ed_gov_wayback_parsed.csv')
