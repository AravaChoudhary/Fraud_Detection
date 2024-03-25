import numpy as np
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv('ad_dataset.csv')

#Safe --> 1 & Fraudelent --> 0
df.loc[df['label'] == 'safe','label'] =  1
df.loc[df['label'] == 'fraudulent','label'] =0

X = df['description']
Y = df['label']
X_train , X_test , Y_train , Y_test = train_test_split(X,Y,test_size=0.2,random_state = 2)

feature_extraction_add = TfidfVectorizer(min_df = 1 , stop_words = 'english',lowercase =True)

X_train_a = feature_extraction_add.fit_transform(X_train)
X_test_a = feature_extraction_add.transform(X_test)

Y_train = Y_train.astype('int')
Y_test = Y_test.astype('int')

model = LogisticRegression()
model.fit(X_train_a,Y_train)

X_train_prediction = model.predict(X_train_a)
training_data_accuracy = accuracy_score(Y_train , X_train_prediction)
print("Accuracy of TRAINING DATA : ",training_data_accuracy * 100)

#Testing DATA
X_test_prediction = model.predict(X_test_a)
testing_data_accuracy = accuracy_score(Y_test , X_test_prediction)
print("Accuracy of TESTING DATA : ",testing_data_accuracy * 100)

#Predictive System
add_description = "example"
input_add = [add_description]
input_add_num = feature_extraction_add.transform(input_add)

#Making Prediction
prediction = model.predict(input_add_num)
if (prediction[0] == 1):
  print("SAFE ADVERTIsEMENT --> Don't Worry")
else:
  print("! ALERT ! Fraudulent ADVERTISEMENT !")

joblib.dump(model, 'Models/add_model.pkl')
model = joblib.load('Models/add_model.pkl')

joblib.dump(feature_extraction_add, 'Models/feature_extraction_add.pkl')
feature_extraction_add = joblib.load('Models/feature_extraction_add.pkl')