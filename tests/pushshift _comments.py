import requests
import json
import csv
import datetime
import time
import pandas as pd
import numpy as np


def get_pushshift_data_comments(query, after, before, sub):
    """
    Function that builds PushShift URLs.

    :param query: Keyword that the API will search, as it is an empty string, all the comments will be collected.
    :param after: Date that the API will start the search.
    :param before: Date that the API will end the search.
    :param sub: Subreddit where the API will search the comments.
    :return: List of dictionaries containing each element of the JSON result.
    """
    url = 'https://api.pushshift.io/reddit/search/comment/?title='+str(query)+'&size=500&after='+str(after)+'' \
        '&before='+str(before)+'&subreddit='+str(sub)

    print(url)  # print used to verify if the url during the process.

    r = requests.get(url)
    data = json.loads(r.text)

    return data['data']


def collect_com_data(com):
    """
    Function to extract key data points.

    :param com: Dictionary from the JSON result containing the content of one comment.
    :return: Nothing
    """
    com_data = list()  # list to store data points
    body = com['body'].replace(';', '')
    author = com['author']
    com_id = com['id']
    score = com['score']
    parent_id = com['parent_id']

    created = datetime.datetime.fromtimestamp(com['created_utc'])  # reddit = 1119484800 - 06/23/2005

    com_data.append((com_id, body, author, score, parent_id, created))
    com_stats[com_id] = com_data


def update_comments_file(sub):
    """
    Function that write the csv

    :param sub: subreddit that will be extracted.
    :return: Nothing.
    """

    upload_com_count = 0
    file = f"Comments-Data/{sub}_Comments.csv"

    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file)
        headers = ["ID", "Comment", "Author", "Score", "Parent id", "Publish Date"]
        a.writerow(headers)

        for com in com_stats:
            a.writerow(com_stats[com][0])
            upload_com_count += 1

        print(str(upload_com_count) + f" comments have been uploaded at {sub}.csv")  # feedback during the process.


if __name__ == '__main__':

    # Run code and loop until all comments are collected from all subreddits

    # List of subreddits:
    df = pd.read_csv('subreddits.csv')
    subreddits = df.values.tolist()

    for sub in subreddits[1:]:
        print(sub)
        sub = str(sub)[5:-5]

        before = int(time.time())  # current date
        after = '1119484800'  # 06/23/2005 reddit creation
        query = ''  # look for all comments
        com_count = 0
        com_stats = {}

        data_com = get_pushshift_data_comments(query, after, before, sub)

        # Will run until all posts have been gathered

        while len(data_com) > 0:

            for coms in data_com:
                collect_com_data(coms)
                com_count += 1

            # Calls get_pushshift_data_comments() with the created date of the last comment.

            print(str(datetime.datetime.fromtimestamp(data_com[-1]['created_utc'])))  # Date of the last comment.

            after = data_com[-1]['created_utc']
            print(after)
            data_com = get_pushshift_data_comments(query, after, before, sub)

            update_comments_file(sub)  # Upload to CSV file.
