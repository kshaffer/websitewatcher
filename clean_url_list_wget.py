import csv

# before running this script, update the following filenames appropriately

wget_results = 'source_data/whitehouse.gov/wh-2017-02-14.txt' # results of the wget scrape
date_of_scrape = '2017-02-14' # date of the wget scrape
output_file = 'clean_data/wh-2017-02-14.csv' # output file for cleaned URL list

# once the above filename variables are set, run the script
# you shouldn't have to edit the following code
# run the script once for each scrape before using compare_two_lists.py

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
        print(line)
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

# write list to text file, one URL per line, for each scrape
write_to_csv(extract_url_database(wget_results, date_of_scrape), output_file)
