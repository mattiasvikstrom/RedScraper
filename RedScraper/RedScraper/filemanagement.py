# import os
# from dotenv import load_dotenv
# import pandas as pd
# from pandas.core.frame import DataFrame
# from data_a import *
# import pandas as pd
# from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia
# import nltk
# from analyze import *
# import numpy as np

# subredd = 'GME'
# load_dotenv()
# file_name = 'GME_comments_20220131.csv'
# data_folder = (os.environ.get('pth'))
# full_path = ""
# file_to_open = (f'{full_path}{file_name}.csv')
# commentData = DataFrame()
# #posts, count, tickers = 0, 0, {}
# commentData = DataFrame()
# posts, count, tickers, comments = 0, 0, {}, {}
# picks = 10

# # if choice == 'AC':
# full_path = (f'{data_folder}{subredd}{"comments"}' + '/')
# # if choice == 'AT':
# #     full_path = (f'{data_folder}{subredd}' + '/')
# file_to_open = (f'{full_path}{file_name}')

# #opens and reads file into dataframe
# if(os.path.isfile(file_to_open)):
#     with open(file_to_open, encoding="utf-8") as f:
#         commentData = pd.read_csv(f)
# #check for which data to be avaliable for analyzing
# #if choice == 'AC':
# posts = commentData['Comments']
# # if choice == 'AT':
# #     posts = commentData['Title']

# #itterates and finds comments containing a stock name, it takes a count and saves that comment for further analysis
# for cmd in posts:
#     try:
#         split = cmd.split(" ")
#     except:
#         print(cmd)
#     for word in split:
#         word = word.replace("$", "")
#         if word.isupper() and len(word) <= 5 and word not in blacklist and word in stocks_us:
#             if word in tickers:
#                 tickers[word] += 1
#                 comments[word].append(cmd)
#                 count += 1
#             else:                               
#                 tickers[word] = 1
#                 comments[word] = [cmd]
#                 count += 1
# #fetches the lexicon and stopwords, if they exist and are uptodate nothing happends.
# nltk.download('vader_lexicon')
# nltk.download('stopwords')
# #instanciates sentimentintensityanalyzer
# vader = sia()
# #add custom words from data_a.py to aid vader with words uncommon outside of these forums
# vader.lexicon.update(new_words)
# #sort results and reserse the order to achieve highest mentioned at the top
# symbols = dict(sorted(tickers.items(), key=lambda item: item[1], reverse = True))
# #pick out the top 10 mentioned symbols 'stocks'
# pick_list = list(symbols.keys())[0:picks]
# scores = {}

# for symbol in pick_list:
#     stock_comments = comments[symbol]
#     for cmt in stock_comments:
#         cmt_score = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
#         score = vader.polarity_scores(cmt)
#         for key, _ in score.items():
#             cmt_score[key] += score[key]
#     # adding score the the specific symbol
#     if symbol in scores:
#         for key, _ in cmt_score.items():
#             scores[symbol][key] += cmt_score[key]
#     else:
#         scores[symbol] = cmt_score

# for key in cmt_score:
#     scores[symbol][key] = scores[symbol][key] / symbols[symbol]
#     scores[symbol][key]  = "{pol:.3f}".format(pol=scores[symbol][key])
# df = pd.DataFrame(scores)
# df.index = ['Bearish', 'Neutral', 'Bullish', 'Total/Compound']
# df = df.astype(float)
# df = df.T

# for i in scores.items():
#     for e in i:
#         print(e)