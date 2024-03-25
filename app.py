from flask import Flask,render_template,request,jsonify,redirect,url_for
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import vectorize
import requests
import joblib
import pickle
from urllib.parse import unquote
import datetime


app = Flask(__name__,static_url_path='/static')
model = joblib.load('Models/model.pkl')
feature_extraction = joblib.load('Models/feature_extraction.pkl')

model_add = joblib.load('Models/add_model.pkl')
feature_extraction_add = joblib.load('Models/feature_extraction_add.pkl')

API_KEY = 'dd0ff48fddfa430c8e77e46151b39b99'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/api/news')
def get_news():
    try:
        # Specify the News API endpoint and parameters
        url = f'https://newsapi.org/v2/top-headlines'
        params = {
            'q': 'cybersecurity',  
            'language': 'en', 
            'country': 'in',  # Change country as needed
            'sortby': 'publishedAt',
            'category': 'cybersecurity AND hacking',
            'from': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'apiKey': API_KEY
        }

        # Make a GET request to the News API
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            news_data = response.json()
            # Extract relevant news articles from the response
            articles = news_data.get('articles', [])
            # Extract required data from each article
            formatted_articles = [{
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'url': article.get('url', '')
            } for article in articles]
            return jsonify(formatted_articles)
        else:
            return jsonify({'error': 'Failed to fetch news data'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/url',methods = ['GET','POST'])
def predict():
    if request.method == 'POST':
        website = request.form.get('website', '')
        
        if not website:
            return render_template('error.html', message='Please enter a website URL')
        
        if not feature_extraction or not model:
            return render_template('error.html', message='Model not loaded')
        
        try: 
            website_numeric = feature_extraction.transform([website])
            prediction = model.predict(website_numeric)[0]
            prediction_label = "Legitimate" if prediction == 1 else "Fraudulent"
            return render_template('prediction.html', website=website, prediction=prediction_label)
        except Exception as e:
            return render_template('error.html', message=str(e))

    return render_template('url.html')

@app.route('/customer_care',methods=['GET', 'POST'])
def customer_car():  
    if request.method == 'POST':
        try:
            number = int(request.form.get('number', ''))
            
            if not number:
                return render_template('error.html', message='Please enter a phone number')
            
            number_reshaped = np.asarray(number).reshape(1, -1)
            
            if not model:
                return render_template('error.html', message='Model not loaded')
            
            prediction = model.predict(number_reshaped)[0]
            prediction_label = "Legitimate" if prediction == 1 else "Fraudulent"  
            return render_template('predict_numbers.html', number=number, prediction=prediction_label)
        except Exception as e:
            return render_template('error.html', message=str(e))

    return render_template('customer_care.html')
@app.route('/add_content', methods=['GET', 'POST'])
def add_content():
    if request.method == 'POST':
        add_desciption = request.form.get('add_description', '')
        
        if not add_desciption:
            return render_template('error.html', message='Please enter The Advertisements description')
        
        if not feature_extraction_add or not model_add:
            return render_template('error.html', message='Model not loaded')
        
        try: 
            add_desciption_numeric = feature_extraction_add.transform([add_desciption])
            prediction = model_add.predict(add_desciption_numeric)[0]
            prediction_label = "Legitimate" if prediction == 1 else "Fraudulent"
            return render_template('add_predict.html', add_desciption = add_desciption, prediction=prediction_label)
        except Exception as e:
            return render_template('error.html', message=str(e))

    return render_template('add_content.html')

if __name__ == '__main__':
    app.run(host = "127.0.0.1", port = 8080 , debug= True)