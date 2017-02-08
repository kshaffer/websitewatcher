import csv

def write_to_csv(data, filename):
    with open(filename, 'w') as csvfile:
        w = csv.writer(csvfile, delimiter = ',')
        for row in data:
            try:
                w.writerow(row)
            except:
                print(row, 'not written to file.')
    print(filename, 'created.')

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

# write list to text file, one URL per line
write_to_csv(extract_url_database('wh-2-8-2nd-wget.txt', '2017-02-08'), '2-8-test2.csv')
