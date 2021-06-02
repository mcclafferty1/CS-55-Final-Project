# from types import MethodDescriptorType
from flask import Flask, render_template, jsonify
import pandas as pd
from flask import json
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def home():

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

app.run()
