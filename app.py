from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

@app.route("/")

def home():
	xs = []
	ys =[]

	df = pd.read_csv('TSLA.csv')

	x =df.iloc[:, 0]
	y = df.iloc[:,1]

	return render_template("home.html",xs = x, ys=y)

if __name__ == "__main__":
	app.run()
	
