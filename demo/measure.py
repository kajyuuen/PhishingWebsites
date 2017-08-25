import requests
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import sklearn
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("df.csv")
train_df, test_df = train_test_split(df[["having_At_Symbol","URL_Length","URL_of_Anchor","Submitting_to_email", "Result"]], test_size = 0.2)

train_df = train_df.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)
clf = LogisticRegression(C=1, penalty='l2')
clf.fit(train_df.drop('Result', axis=1), train_df['Result'])
pred = clf.predict(test_df.drop('Result', axis=1))


def measure(url):
    url_date = []

    url_date.append(at_sign_symdol(url))
    url_date.append(url_of_anchor(url))
    url_date.append(long_url(url))
    url_date.append(is_send_email(url))

    pred = clf.predict_proba(url_date)

    fishing = pred.tolist()
    return fishing[0][0]

def at_sign_symdol(url_data):
    for character in url_data:
        if(character == "@"):
            ans = -1
            break
        else:
            ans = 0
    return ans


def url_of_anchor(url_data):
    url = url_data
    parsed_url = urlparse(url)
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers) # <Response [200]>

    soup = BeautifulSoup(response.text, 'html.parser')

    cnt = 0.01
    anc_cnt = 0.0
    for link in soup.findAll('a', href=True):
        cnt += 1.0
        if "#" == link['href']:
            anc_cnt += 1.0
        elif "#content" == link['href']:
            anc_cnt += 1.0
        elif "#skip" == link['href']:
            anc_cnt += 1.0
        elif "JavaScript::void(0)" in link['href']:
            anc_cnt += 1.0

    per = anc_cnt / cnt*100
    if per < 31:
        return 1
    elif 31 <= per and per >= 67:
        return 0
    else:
        return -1

def long_url(url_data):
    url_len = len(url_data)
    if 75 >= url_len >= 54:
        ans = 0
    elif url_len >= 54:
        ans = -1
    elif url_len < 54:
        ans = 1
    return ans

def is_send_email(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers) # <Response [200]>
    soup = BeautifulSoup(response.text, 'html.parser')


    cnt = 0.0
    anc_cnt = 0.0
    for link in soup.findAll('a', href=True):
        cnt += 1.0
        if "mailto" in link['href']:
            return -1
        elif "mail()" in link['href']:
            return -1
    return 1
