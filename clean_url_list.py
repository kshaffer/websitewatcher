import json

def read_text_file(filename):
    f = open(filename, encoding='utf-8')
    table_original = []
    for line in f:
        table_original.append(line.rstrip('\n'))
    return table_original

def write_to_text(data, filename):
    f = open(filename, 'w', encoding = 'utf-8')
    for line in data:
        f.write(line + '\n')
    f.close()

# import URLs from spider output
u = read_text_file('2017-01-31-11-30-00.txt')

# make into list
url_list = ['url']
for article in u:
    url_list.append(json.loads(article)['file_url'])

# write list to text file, one URL per line
write_to_text(url_list, 'breitbart_urls.csv')

# now use clean_it_more.R to strip out erroneous and (some) duplicate URLs
