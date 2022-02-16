from genericpath import exists
import pandas as pd
from pandas.core.frame import DataFrame
import praw
import os
from dotenv import load_dotenv
import datetime

class RedditScraper:

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
        file_name = (f'{subredd}_{time}')
        data_folder = (os.environ.get('pth'))
        full_path = (f'{data_folder}{subredd}' + '/')
        file_to_open = (f'{full_path}{file_name}.csv')

        #lists for each column
        titlelist = []  #title
        textlist = []   #self_text
        idlist = []     #id
        scorlist = []   #score
        comlist = []    #num_comments
        urllist = []    #url
        #dataframe to hold and get all id's already inside the table
        idframe = DataFrame()
        data = DataFrame()

        ids = []

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
            if sub.id not in str(ids):
                titlelist.append(sub.title)
                textlist.append(sub.selftext)
                idlist.append(sub.id)
                scorlist.append(sub.score)
                comlist.append(sub.num_comments)
                urllist.append(sub.url)

        #creates a dataframe of all the lists containing values from the scrape.
        data = pd.DataFrame({'Title': titlelist, 
                        'Post Text': textlist, 
                        'ID': idlist,
                        'Score': scorlist,
                        'Total Comments': comlist,
                        'Post URL': urllist,
                        })
        #opens and appends to file corresponding to name of the daily file. creates if it does not exist.
        with open(full_path+'%s.csv' % file_name, 'a', encoding="utf-8") as f:
            data.to_csv(f, header=f.tell()==0, index=False)

if __name__ == '__main__':
    scraper = RedditScraper()
    scraper.scrapered()