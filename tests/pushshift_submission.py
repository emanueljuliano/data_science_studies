import requests
import json
import csv
import datetime
import time
import pandas as pd


def get_pushshift_data_submissions(query, after, before, sub):
    """
    Function that builds PushShift URLs.

    :param query: Keyword that the API will search, as it is an empty string, all the submissions will be collected.
    :param after: Date that the API will start the search.
    :param before: Date that the API will end the search.
    :param sub: Subreddit where the API will search the submissions.
    :return: List of dictionaries containing each element of the JSON result.
    """
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=500&after='+str(after)+'' \
        '&before='+str(before)+'&subreddit='+str(sub)

    print(url)  # print used to verify if the url during the process.

    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


def collect_subm_data(subm):
    """
    Function to extract key data points.

    :param subm: Dictionary from the JSON result containing the content of one submission.
    :return: Nothing
    """

    subm_data = list()  # list to store data points
    title = subm['title'].replace(';', '')
    author = subm['author']
    sub_id = subm['id']
    score = subm['score']
    num_coms = subm['num_comments']
    over_18 = subm['over_18']
    try:
        selftext = subm['selftext'].replace(';', '')
    except KeyError:
        selftext = "NaN"
    try:
        description = subm['description'].replace(';', '')
    except KeyError:
        description = "NaN"

    created = datetime.datetime.fromtimestamp(subm['created_utc'])  # reddit = 1119484800 - 06/23/2005

    subm_data.append((sub_id, title, author, score, num_coms, over_18, selftext, description, created))
    subm_stats[sub_id] = subm_data



def update_subs__file(sub):
    """
    Function that write the csv

    :param sub: subreddit that will be extracted.
    :return: Nothing
    """
    upload_subm_count = 0
    file = f"Submissions-Data/{sub}_Submissions.csv"

    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file)
        headers = ["Post ID", "Title", "Author", "Score", "No. of Comments", "Over 18", "Selftext", "Description",
                   "Publish Date"]
        a.writerow(headers)

        for subm in subm_stats:
            a.writerow(subm_stats[subm][0])
            upload_subm_count += 1

        print(str(upload_subm_count) + f" submissions have been uploaded at {sub}.csv")  # feedback during the process.


if __name__ == '__main__':

    # Run code and loop until all submissions are collected from all subreddits

    # List of subreddits:
    df = pd.read_csv('subreddits.csv')
    subreddits = df.values.tolist()

    for sub in subreddits:
        sub = str(sub)[5:-5]

        before = int(time.time())  # current date
        after = '1119484800'  # 06/23/2005 reddit creation
        query = ''  # look for all submissions
        subm_count = 0
        subm_stats = {}

        data_subm = get_pushshift_data_submissions(query, after, before, sub)

        # Will run until all posts have been gathered

        while len(data_subm) > 0:

            for submission in data_subm:
                collect_subm_data(submission)
                subm_count += 1

            # Calls getPushshiftDataSubmission() with the created date of the las submission.

            print(str(datetime.datetime.fromtimestamp(data_subm[-1]['created_utc'])))  # Date of the last comment.

            after = data_subm[-1]['created_utc']
            data_subm = get_pushshift_data_submissions(query, after, before, sub)

            update_subs__file(sub)  # Upload to CSV file.
