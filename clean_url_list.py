import json
import csv

"""
def write_to_text(data, filename):
    f = open(filename, 'w', encoding = 'utf-8')
    for line in data:
        f.write(line + '\n')
    f.close()
"""

def read_text_file(filename):
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

def write_to_csv(data, filename):
    with open(filename, 'w') as csvfile:
        w = csv.writer(csvfile, delimiter = ',')
        for row in data:
            try:
                w.writerow(row)
            except:
                print(row, 'not written to file.')
    print(filename, 'created.')

def extract_url_database(filename):
    u = read_text_file(filename)
    url_list = [['url', 'timestamp', 'id']]
    for article in u:
        url_object = []
        url_object.append(json.loads(article)['file_url'])
        url_object.append(json.loads(article)['timestamp'])
        url_object.append(json.loads(article)['file_id'])
        url_list.append(url_object)
    return(url_list)

# write list to text file, one URL per line
write_to_csv(extract_url_database('whg.txt'), 'whg_url_data.csv')

