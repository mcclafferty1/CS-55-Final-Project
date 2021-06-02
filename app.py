# Include any dependencies
from flask import Flask, render_template, jsonify
import pandas as pd
from flask import json
from flask_cors import CORS
import json

app = Flask(__name__)
# Use cors to allow for requests from an outside server (IBM Cloud Watson)
CORS(app)

# Setup the homepage route
@app.route("/", methods=['GET'])
def home():

    return render_template("index.html")

# Retrieve sentiment data for a specific stock
@app.route("/stock/<stock>", methods=['GET'])
def stock_sentiment(stock):
    # Read in all data from FullComp1.csv
    all_stock_data = pd.read_csv('./FullComp1.csv')
    stock_data = all_stock_data.loc[all_stock_data['ticker'] == stock]
    final_stock_data = stock_data[['date']]

    # Parse the sentiment from the FullComp1.csv file and include it as an additional column
    sentiment = []
    for index, row in stock_data.iterrows():
        document = row['document']
        strings = document.split()
        sentiment.append(strings[10][:-1])

    final_stock_data['sentiment'] = sentiment

    # return the sentiment data for the stock in a json format
    return final_stock_data.to_json(orient = "records")

# Retrieve the sentiment for the 8 industries we used
@app.route("/industry_sentiment", methods=['GET'])
def industry_sentiment():
    all_stock_data = pd.read_csv('./FullComp1.csv')
    industry_count = {}

    # Parse the sentiment from the FullComp1.csv file for each stock
    sentiment = []

    for index, row in all_stock_data.iterrows():
        document = row['document']
        strings = document.split()
        sentiment.append(strings[10][:-1])

    all_stock_data['sentiment'] = sentiment

    # Loop through each stock and create an average sentiment for each industry
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

    # return the industries and their averages in json format
    return jsonify(industry_average)

app.run()
