import pandas as pd
from pandas.core.frame import DataFrame
import os
from dotenv import load_dotenv
from data_a import *

class RedditScraper_analyze:

    def analyze_mostmentioned(self, choice, sub, file):

        subredd = sub
        load_dotenv()
        file_name = file
        data_folder = (os.environ.get('pth'))
        full_path = ""
        file_to_open = (f'{full_path}{file_name}.csv')
        commentData = DataFrame()
        posts, count, tickers = 0, 0, {}

        picks = 10
        
        if choice == 'AC':
            full_path = (f'{data_folder}{subredd}{"comments"}' + '/')
        if choice == 'AT':
            full_path = (f'{data_folder}{subredd}' + '/')
        file_to_open = (f'{full_path}{file_name}')

        #opens and reads file if avaliable to save all 'ID' values for comparison
        if(os.path.isfile(file_to_open)):
            with open(file_to_open, encoding="utf-8", errors='ignore') as f:
                commentData = pd.read_csv(f)

        posts = commentData['Comments']
        for post in posts:
            split = post.split(" ")
            for word in split:
                word = word.replace("$", "")
                if word.isupper() and len(word) <= 5 and word not in blacklist and word in stocks_us:
                    if word in tickers:
                        tickers[word] += 1
                        count += 1
                    else:                            
                        tickers[word] = 1
                        count += 1 

        # sorts the dictionary
        symbols = dict(sorted(tickers.items(), key=lambda item: item[1], reverse = True)[0:picks])
        return symbols
        
if __name__ == '__main__':
    scraper = RedditScraper_analyze()
    scraper.scrapered()


