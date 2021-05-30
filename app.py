# from types import MethodDescriptorType
from flask import Flask, render_template
# import pandas as pd
from flask import json
import requests

app = Flask(__name__)

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
	return str(8.43)

@app.route("/industry_sentiment", methods=['GET'])

def industry_sentiment():
	return "The industry sentiment is " + str(8.45)

if __name__ == "__main__":
	app.run()
	# home()
	
