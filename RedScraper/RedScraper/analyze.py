import pandas as pd
from pandas.core.frame import DataFrame
import os
from dotenv import load_dotenv
from data_a import *

class RedditScraper_analyze:

    def analyze_mostmentioned(self, choice, sub, file):

        subredd = sub #name of subreddit
        load_dotenv() #load environment to access .env file
        file_name = file #filename 
        data_folder = (os.environ.get('pth')) #fetch string of 'pth' from .env
        full_path = "" #instansiation of the variable
        file_to_open = (f'{full_path}{file_name}.csv') #instansiation of variable
        commentData = DataFrame() #instansiation of dataframe
        posts, tickers = 0, {}
        picks = 10

        #finalize path for comments or topics
        if choice == 'AC':
            full_path = (f'{data_folder}{subredd}{"comments"}' + '/')
        if choice == 'AT':
            full_path = (f'{data_folder}{subredd}' + '/')
        file_to_open = (f'{full_path}{file_name}')

        #opens and reads file if avaliable
        if(os.path.isfile(file_to_open)):
            with open(file_to_open, encoding="utf-8", errors='ignore') as f:
                commentData = pd.read_csv(f)
        #determine which type of data is to be analyzed
        if choice == 'AC':
            posts = commentData['Comments']
        if choice == 'AT':
            posts = commentData['Title']
        
        for post in posts:
            try:
                split = post.split(" ") #split each post into words
            except:
                print(post)
            for word in split:
                word = word.replace("$", "") # clear all words containing $sign
                #evaluate uppercase, length, not avaliable in the backlist and contained inside the list of stocks
                if word.isupper() and len(word) <= 5 and word not in blacklist and word in stocks_us:
                    if word in tickers:
                        tickers[word] += 1
                    else:                            
                        tickers[word] = 1

        # sorts the dictionary and returns top 10 listings
        symbols = dict(sorted(tickers.items(), key=lambda item: item[1], reverse = True)[0:picks])
        print(symbols)
        return symbols
        
# if __name__ == '__main__':
#     scraper = RedditScraper_analyze()
#     scraper.analyze_mostmentioned()

#test method for retrieving top ranked posts from comments data
def toprankedposts():

    subredd = 'wallstreetbets'
    load_dotenv()
    file_name = 'wallstreetbets_comments_20220122'
    data_folder = (os.environ.get('pth'))
    full_path = ""
    file_to_open = (f'{full_path}{file_name}.csv')
    commentData = DataFrame()
    #posts, count, tickers = 0, 0, {}

    picks = 10
    full_path = (f'{data_folder}{subredd}{"comments"}' + '/')
    #finalize path for comments or topics
    # if choice == 'AC':
    #     full_path = (f'{data_folder}{subredd}{"comments"}' + '/')
    # if choice == 'AT':
    #     full_path = (f'{data_folder}{subredd}' + '/')
    file_to_open = (f'{full_path}{file_name}')

    #opens and reads file if avaliable to save all 'ID' values for comparison
    if(os.path.isfile(file_to_open)):
        with open(file_to_open, encoding="utf-8", errors='ignore') as f:
            commentData = pd.read_csv(f)

    # if choice == 'AC':
    #     posts = commentData['Comments']
    # if choice == 'AT':
    #     posts = commentData['Title']

    symbols = dict(sorted(commentData.items(), key=lambda item: item[1], reverse = True)[0:picks])
    print(symbols)


