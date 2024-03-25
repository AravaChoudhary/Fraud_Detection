import numpy as np
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv('fwebsite.csv')
df.isnull().sum()
df.loc[df['Category'] == 'spam' , 'Category' ] = 0
df.loc[df['Category'] == 'ham' , 'Category' ] = 1
df['Category'].value_counts()
X = df['Website']
Y = df['Category']
X_train , X_test , Y_train , Y_test = train_test_split(X ,Y , test_size = 0.2 , random_state = 2)
feature_extraction = TfidfVectorizer(min_df = 1 , stop_words = 'english' , lowercase = True)
X_train_a = feature_extraction.fit_transform(X_train)
X_test_b = feature_extraction.transform(X_test)
Y_train = Y_train.astype('int')
Y_test = Y_test.astype('int')
model = LogisticRegression()
model.fit(X_train_a , Y_train)
        
#TRAINING DATA
X_train_prediction = model.predict(X_train_a)
training_data_accuracy = accuracy_score(Y_train , X_train_prediction)
print("Accuracy of TRAINING DATA : ",training_data_accuracy*100,"%")

#TESTING DATA
X_test_prediction = model.predict(X_test_b)
testing_data_accuracy = accuracy_score(Y_test , X_test_prediction)
print("Accuracy of TESTING DATA : ",testing_data_accuracy*100,"%")
website = "https://example.com"
input_website = [website]
input_website_numeric = feature_extraction.transform(input_website)
prediction = model.predict(input_website_numeric)
if(prediction[0] == 1):
    print("HAM Website --> Usefull Website")
else:
    print("SPAM Website --> Useless Website")



joblib.dump(model, 'Models/model.pkl')
model = joblib.load('Models/model.pkl')

joblib.dump(feature_extraction, 'Models/feature_extraction.pkl')
feature_extraction = joblib.load('Models/feature_extraction.pkl')