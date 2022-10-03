#Library
from distutils.errors import PreprocessError
import pandas as pd
import numpy as np
import re
import csv
import sqlite3

db = sqlite3.connect('Tweet.db', check_same_thread=False)
db.text_factory = bytes
mycursor = db.cursor()
q_kamusalay = "select * from Tweets"
t_kamusalay = pd.read_sql_query(q_kamusalay, db)

df_alay = pd.read_csv('D:/BINAR ZOOM/CHALLENGE/input/data/new_kamusalay.csv', encoding ='iso-8859-1', header=None)
alay_dict = df_alay.rename(columns={0: 'original', 
                                      1: 'replacement'})

def lowercase(text):
    return text.lower()

def remove_unnecessary_char(text):
    text = re.sub('\n',' ',text) #membuang semua '\n'
    text = re.sub('rt',' ',text) #membuang semua simbol retweet
    text = re.sub('user',' ',text) #membuang semua username
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) #membuang semua URL
    text = re.sub('  +', ' ', text) #membuang ekstra spasi
    return text
    
def remove_nonaplhanumeric(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text) 
    return text

#mengubah dataframe menjadi bentuk dictionary
alay_dict_map = dict(zip(alay_dict['original'], alay_dict['replacement']))

#mengubah kata kata alay menjadi kata baku
def normalize_alay(text):
    return ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])


def process_csv_old(input_csv):

    try:
        t_input = pd.read_csv(input_csv, encoding='iso-8859-1')

    except:
        print("Trying another Encoding")
        try:
            t_input = pd.read_csv(input_csv, encoding='utf-8')
        except:
            print("CSV File is unreadable")

    try:

        first_column = t_input.iloc[:, 0] #Nanti kalau saat launching 100 nya dihilangkan
        print(first_column)

        for tweet in first_column:
            tweet_clean = PreprocessError(tweet)
            query_tabel = "insert into tweet (tweet_kotor,tweet_bersih) values (?, ?)"
            val = (tweet, tweet_clean)
            mycursor.execute(query_tabel, val)
            db.commit()
            print(tweet)
    except:
        print("CSV File is unreadable")

def process_csv(input_file):
    first_column = input_file.iloc[:, 0] #Nanti kalau saat launching 100 nya dihilangkan
    print(first_column)

    for tweet in first_column:
        tweet_clean = PreprocessError(tweet)
        query_tabel = "insert into tweet (tweet_kotor,tweet_bersih) values (?, ?)"
        val = (tweet, tweet_clean)
        mycursor.execute(query_tabel, val)
        db.commit()
        print(tweet)
        

def process_text(input_text):
    try: 
        output_text = PreprocessError(input_text)
        return output_text


    except:
        print("Text is unreadable")   
