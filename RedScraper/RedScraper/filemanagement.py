import os
from dotenv import load_dotenv

def getfiles(self, redname):
    load_dotenv()
    data_folder = (os.environ.get('pth'))
    full_path = (f'{data_folder}{redname}' + '/')

    for file in os.listdir(full_path):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"): 
            continue
        else:
            continue