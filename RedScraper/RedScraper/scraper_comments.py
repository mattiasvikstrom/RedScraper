from genericpath import exists
import pandas as pd
from pandas.core.frame import DataFrame
import praw
import os
from dotenv import load_dotenv
import datetime

class RedditScraper_comments:

    def scrapered(self, red):
        subredd = red
        time = datetime.datetime.now()
        load_dotenv()
        user_agent = "Analyze-Scraper 1.0 /u/Solid-Challenge2405"
        reddit = praw.Reddit(
            client_id = (os.environ.get('pw')),
            client_secret = (os.environ.get('se')),
            user_agent = user_agent
        )
        time = time.strftime("%Y%m%d")
        file_name = (f'{subredd}{"_comments"}_{time}')
        data_folder = (os.environ.get('pth'))
        full_path = (f'{data_folder}{subredd}{"comments"}' + '/')
        file_to_open = (f'{full_path}{file_name}.csv')

        #lists for each column
        body = []       #the comment body
        author = []     #post author
        id = []         #the comment id
        upvotes = []    #the number of upvotes
        postflair = []  #post_flairs
        #dataframe to hold and get all id's already inside the table
        idframe = DataFrame()
        data = DataFrame()

        ids = []

        #Variables to check if to extract comments also
        flairOfInterest = {'Daily Discussion', 'Weekend Discussion', 'Discussion'}
        minRatio = 0.70
        comLimit = 10
        postflair = ""

        #create directory for file is subreddit has not been scraped before
        if not (os.path.exists(full_path)):
            os.mkdir(full_path)

        #opens and reads file if avaliable to save all 'ID' values for comparison
        if(os.path.isfile(file_to_open)):
            with open(file_to_open, encoding="utf-8", errors='ignore') as f:
                idframe = pd.read_csv(f)
            ids = idframe['ID']
        
        #compares existing ids to avoid duplications
        for sub in reddit.subreddit(subredd).hot():
            if subredd == 'wallstreetbets':
                postflair = sub.link_flair_text
            else:
                postflair = None
            if sub.upvote_ratio >= minRatio and sub.ups > comLimit and (postflair in flairOfInterest or postflair is None):
                sub.comment_sort = 'new'
                sub.comments.replace_more(limit=None)
                for comment in sub.comments:
                    if comment.id not in str(ids):
                        body.append(comment.body)
                        author.append(comment.author)
                        id.append(comment.id)
                        upvotes.append(comment.score)
                
        #creates a dataframe of all the lists containing values from the scrape.
        data = pd.DataFrame({'ID': id, 
                        'Author': author, 
                        'Upvotes': upvotes,
                        'Comments': body,
                        })
        #opens and appends to file corresponding to name of the daily file. creates if it does not exist.
        with open(full_path+'%s.csv' % file_name, 'a', encoding="utf-8") as f:
            data.to_csv(f, header=f.tell()==0)

if __name__ == '__main__':
    scraper = RedditScraper_comments()
    scraper.scrapered()