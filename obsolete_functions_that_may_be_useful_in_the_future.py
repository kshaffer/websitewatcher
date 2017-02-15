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

# for URLs in both snapshots, check the Wayback Machine to see when they most recently changed
# assemble a list of lists (urls_changed) containing the URL and most recent change
# for all URLs with a most recent change between the two provided timestamps
# write data to a CSV file

wayback_latest = extract_wayback_url_database(read_wayback_dump(wayback_dump))
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
