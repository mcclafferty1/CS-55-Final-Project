# from types import MethodDescriptorType
from flask import Flask, render_template, jsonify
# import pandas as pd
from flask import json
from flask_cors import CORS

import requests
import nltk
import matplotlib.pyplot as plt
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import project_helper
nltk.download('stopwords')
nltk.download('wordnet')
import lxml
import re
import datetime

from ratelimit import limits, sleep_and_retry
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import os



import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions, EmotionOptions

def get_documents(text):
    """
    Extract the documents from the text

    Parameters
    ----------
    text : str
        The text with the document strings inside

    Returns
    -------
    extracted_docs : list of str
        The document strings found in `text`
    """

    # TODO: Implement
    final_docs = []
    start_regex = re.compile(r'<DOCUMENT>')
    end_regex = re.compile(r'</DOCUMENT>')

    start_idx = [x.end() for x in re.finditer(start_regex, text)]
    end_idx = [x.start() for x in re.finditer(end_regex, text)]

    for start_i, end_i in zip(start_idx, end_idx):
        final_docs.append(text[start_i:end_i])

    return final_docs

def get_document_type(doc):
    """
    Return the document type lowercased

    Parameters
    ----------
    doc : str
        The document string

    Returns
    -------
    doc_type : str
        The document type lowercased
    """

    # TODO: Implement
    # Regex explaination : Here I am tryng to do a positive lookbehind
    # (?<=a)b (positive lookbehind) matches the b (and only the b) in cab, but does not match bed or debt.
    # More reference : https://www.regular-expressions.info/lookaround.html

    type_regex = re.compile(r'(?<=<TYPE>)\w+[^\n]+')  # gives out \w
    type_idx = re.search(type_regex, doc).group(0).lower()
    return type_idx

def get_sec_data(cik, doc_type, sec_api,start=0, count=5):
    #sec_api = SecAPI()
    newest_pricing_data = pd.to_datetime('2020-05-01')
    rss_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany' \
        '&CIK={}&type={}&start={}&count={}&owner=exclude&output=atom' \
        .format(cik, doc_type, start, count)
    i=1
    for i in range(10):
      sec_data = sec_api.get(rss_url)
      #print(sec_data)
      feed = BeautifulSoup(sec_data.encode('utf-8'), 'xml').feed
      if feed is not None:
        break
      else:
        time.sleep(1)
        #print("Sleeping!!")

    #print(feed)
    #print(feed)
    entries = [
        (
            entry.content.find('filing-href').getText(),
            entry.content.find('filing-type').getText(),
            entry.content.find('filing-date').getText())
        for entry in feed.find_all('entry', recursive=False)
        if pd.to_datetime(entry.content.find('filing-date').getText()) <= newest_pricing_data]

    return entries


def remove_html_tags(text):
    text = BeautifulSoup(text, 'html.parser').get_text()

    return text


def clean_text(text):
    text = text.lower()
    text = remove_html_tags(text)

    return text


def lemmatize_words(words):
    """
    Lemmatize words 

    Parameters
    ----------
    words : list of str
        List of words

    Returns
    -------
    lemmatized_words : list of str
        List of lemmatized words
    """

    # TODO: Implement
    wnl = WordNetLemmatizer()
    lemmatized_words = [wnl.lemmatize(word, 'v') for word in words]

    return lemmatized_words


example_ticker = 'AMZN'
ten_ks_by_ticker = {}
numbers = {'AMZN': 0, 'BA': 0, 'CNP': 0, 'CVX': 0, 'FL': 0, 'FRT': 0, 'HON': 0}


def main_get_files(k, cik_lookup,sec_api):
    sec_data = {}
    #sec_api =project_helper.SecAPI()

    for ticker, cik in cik_lookup.items():
        sec_data[ticker] = get_sec_data(cik, '10-Q',sec_api)

    raw_fillings_by_ticker = {}

    for ticker, data in sec_data.items():
        raw_fillings_by_ticker[ticker] = {}
        for index_url, file_type, file_date in data:
            if (file_type == '10-Q'):
                file_url = index_url.replace('-index.htm', '.txt').replace('.txtl', '.txt')
                raw_fillings_by_ticker[ticker][file_date] = sec_api.get(file_url)

    filling_documents_by_ticker = {}

    for ticker, raw_fillings in raw_fillings_by_ticker.items():
        filling_documents_by_ticker[ticker] = {}
        for file_date, filling in raw_fillings.items():
            filling_documents_by_ticker[ticker][file_date] = get_documents(filling)
    i = 0
    i2 = 0
    for ticker, filling_documents in filling_documents_by_ticker.items():
        if k == 0:
            ten_ks_by_ticker[ticker] = []
        numbers[ticker] = 0
        for file_date, documents in filling_documents.items():
            for document in documents:
                i = i + 1
                if get_document_type(document) == '10-q':
                    i2 = i2 + 1
                    numbers[ticker] = numbers[ticker] + 1
                    ten_ks_by_ticker[ticker].append({
                        'CIK': cik_lookup[ticker],
                        'ten_q': document,
                        'file_date': file_date})
    #print(i)
    #print(i2)
    #print(numbers)
    # print(print(len(ten_ks_by_ticker))
    #for keys in ten_ks_by_ticker:
        #print(keys, " ", len(ten_ks_by_ticker[keys]))

    return ten_ks_by_ticker


# example_ticker='AMZN'
# pprint.pprint(sec_data[example_ticker][:5])

# Old Code Below

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def home():
    # response = requests.get('https://api.covid19api.com/summary')
    # data= response.content
    # df = pd.read_csv('TSLA.csv')

    # year = list(df.iloc[:, 0])
    # price = list(df.iloc[:,1])

    # yp = zip(year,price)

    return render_template("index.html")


@app.route("/stock/<stock>", methods=['GET'])
def stock_sentiment(stock):
    all_stock_data = pd.read_csv('./FullComp1.csv')

    stock_data = all_stock_data.loc[all_stock_data['ticker'] == stock]
    final_stock_data = stock_data[['date']]
    sentiment = []

    for index, row in stock_data.iterrows():
        document = row['document']
        strings = document.split()
        sentiment.append(strings[10][:-1])

    final_stock_data['sentiment'] = sentiment


    print(final_stock_data)
    return final_stock_data.to_json(orient = "records")
    # cik_lookup = {stock: '0001018724'}
    # # print("Hello")
    # sec_api = project_helper.SecAPI()

    # #for k in range(1):
    # k=0
    # ten_ks_by_ticker=main_get_files(k, cik_lookup,sec_api)

    # master1_ten_ks_by_ticker = {}
    # seen_before = {}

    # for ticks, ten_ks in ten_ks_by_ticker.items():
    #     # i=i+1
    #     master1_ten_ks_by_ticker[ticks] = []

    #     for line in ten_ks_by_ticker[ticks]:
    #         sign = line['file_date'] + ticks
    #         if sign not in seen_before:
    #             # print(line['file_date'])
    #             seen_before[line['file_date'] + ticks] = 1
    #             master1_ten_ks_by_ticker[ticks].append(line)

    # master_ten_ks_by_ticker = {}
    # for tics, ten_kz in master1_ten_ks_by_ticker.items():
    #     master_ten_ks_by_ticker[tics] = []
    #     largest = '2001-01-01'
    #     # print(len(master_ten_ks_by_ticker[tics]))
    #     while len(master1_ten_ks_by_ticker[tics]) > 0:
    #         largest = '2001-01-01'
    #         # print(len(master_ten_ks_by_ticker[tics]))
    #         for line in master1_ten_ks_by_ticker[tics]:
    #             if datetime.datetime.strptime(line['file_date'], '%Y-%m-%d') > datetime.datetime.strptime(largest,
    #                                                                                                       '%Y-%m-%d'):
    #                 largest = line['file_date']
    #                 largestfile = line

    #         for line in master1_ten_ks_by_ticker[tics]:
    #             if datetime.datetime.strptime(line['file_date'], '%Y-%m-%d') == datetime.datetime.strptime(largest,
    #                                                                                                        '%Y-%m-%d'):
    #                 master_ten_ks_by_ticker[tics].append(line)
    #                 master1_ten_ks_by_ticker[tics].remove(line)

    # for ticker, ten_ks in master_ten_ks_by_ticker.items():
    #     for ten_k in ten_ks:
    #         ten_k['file_clean'] = clean_text(ten_k['ten_q'])

    # word_pattern = re.compile('\w+')

    # for ticker, ten_ks in master_ten_ks_by_ticker.items():
    #     for ten_k in ten_ks:
    #         ten_k['file_lemma'] = lemmatize_words(word_pattern.findall(ten_k['file_clean']))

    # lemma_english_stopwords = lemmatize_words(stopwords.words('english'))

    # for ticker, ten_ks in master_ten_ks_by_ticker.items():
    #     for ten_k in ten_ks:
    #         ten_k['file_lemma'] = [word for word in ten_k['file_lemma'] if word not in lemma_english_stopwords]

    # print('Stop Words Removed')

    # sentiments = ['negative', 'positive', 'uncertainty', 'litigious', 'constraining', 'interesting']

    # #sentiment_df = pd.read_csv(os.path.join('..', '..', 'data', 'project_5_loughran_mcdonald', 'loughran_mcdonald_master_dic_2018.csv'))
    # #sentiment_df = pd.read_csv(os.path.join("Desktop","CompLitProjFiles","LoughranMcDonald_MasterDictionary_2018.csv")
    # sentiment_df = pd.read_csv(
    #     "./LoughranMcDonald_MasterDictionary_2018.csv")
    # sentiment_df.columns = [column.lower() for column in sentiment_df.columns]  # Lowercase the columns for ease of use

    # # Remove unused information
    # sentiment_df = sentiment_df[sentiments + ['word']]
    # sentiment_df[sentiments] = sentiment_df[sentiments].astype(bool)
    # sentiment_df = sentiment_df[(sentiment_df[sentiments]).any(1)]

    # # Apply the same preprocessing to these words as the 10-k words
    # sentiment_df['word'] = lemmatize_words(sentiment_df['word'].str.lower())
    # sentiment_df = sentiment_df.drop_duplicates('word')

    # master_dict = {}
    # for index, row in sentiment_df.iterrows():
    #     master_dict[row['word']] = 1
    # #q_dict = {}
    # #for ticker, ten_ks in master_ten_ks_by_ticker.items():
    #     # print(ten_ks)
    #     #for ten_k in ten_ks:
    #         #document1 = ""
    #         #print(len(ten_k))
    #         #for word in ten_k["file_lemma"]:
    #             #if word in master_dict:
    #                 #document1 = document1 + " " + word

    # q_dict = {}
    # for ticker, ten_ks in master_ten_ks_by_ticker.items():
    #     lemma_docs = [' '.join(ten_k['file_lemma']) for ten_k in ten_ks]
    #     for docs in lemma_docs:
    #         # print(docs[12:19])
    #         master_string = ""
    #         for word in docs.split(" "):
    #             if word in master_dict:
    #                 master_string = master_string + " " + word
    #         q_dict[docs[12:19]] = master_string
    # print(q_dict.keys())

    # list0=[]
    # for datenames in q_dict.keys():
    #     list0.append(datenames)


    # authenticator = IAMAuthenticator('be5tVVZfmsFUh572Se2nencOEgqVCzUvZZZukhU5XB58')
    # natural_language_understanding = NaturalLanguageUnderstandingV1(
    #     version='2020-08-01',
    #     authenticator=authenticator
    # )

    # natural_language_understanding.set_service_url(
    #     'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/8b1fe085-04ac-4040-93d5-537db24382e1')

    # response = natural_language_understanding.analyze(
    #     # url='www.wsj.com/news/markets',
    #     #text=q_dict['2019630'],
    #     text=q_dict[list0[0]],
    #     features=Features(
    #         #language="en",
    #         emotion=EmotionOptions(),
    #         sentiment=SentimentOptions())).get_result()



    # return jsonify([response['sentiment']['document']['score']])


@app.route("/industry_sentiment", methods=['GET'])
def industry_sentiment():
    all_stock_data = pd.read_csv('./FullComp1.csv')
    industry_count = {}

    sentiment = []

    for index, row in all_stock_data.iterrows():
        document = row['document']
        strings = document.split()
        sentiment.append(strings[10][:-1])

    all_stock_data['sentiment'] = sentiment


    industry_count = {}
    industry_sum = {}
    industry_average = {}

    for index, row in all_stock_data.iterrows():
        if row['Industry'] not in industry_count:
            industry_count[row['Industry']] = 1
            industry_sum[row['Industry']] = float(row['sentiment'])
            industry_average[row['Industry']] = float(row['sentiment'])
        else:
            industry_count[row['Industry']] += 1
            industry_sum[row['Industry']] += float(row['sentiment'])
            industry_average[row['Industry']] = industry_sum[row['Industry']]/industry_count[row['Industry']]
    print(industry_average)

    return jsonify(industry_average)


if __name__ == "__main__":
    stock_sentiment("AMZN")
app.run()
# home()

