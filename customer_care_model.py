import numpy as np
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


df = pd.read_csv('fraud_and_safe_numbers.csv')
        
#Label Encoding
df.loc[df['type'] == 'fraud' , 'type'] = 0
df.loc[df['type'] == 'safe','type'] = 1
X = df['number']
Y = df['type']
X_numpy = np.asarray(X)
X_reshape = X_numpy.reshape(-1,1)
        
#Splitting the Training and Testing Data
X_train , X_test , Y_train , Y_test = train_test_split(X_reshape ,Y , test_size = 0.2, random_state = 2)

Y_train = Y_train.astype('int')
Y_test = Y_test.astype('int')

model = LogisticRegression()
model.fit(X_train , Y_train)

#TRAINING DATA
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(Y_train,X_train_prediction)
print("Accuracy of the TRAINING DATA : ",training_data_accuracy * 100,"%")

#TESTING DATA
X_test_prediction = model.predict(X_test)
testing_data_accuracy = accuracy_score(Y_test , X_test_prediction)
print("Accuracy of the TESTING DATA : ",testing_data_accuracy * 100,"%")
number = 12345667890
input_number = [number]
input_number_as_array = np.asarray(input_number)
input_number_reshaped = input_number_as_array.reshape(1,-1)

prediction = model.predict(input_number_reshaped)
if(prediction == 1):
    print("Legitimate Mobile Number")
else:
    print("WARNING ! This is not a Legitimate Number")


joblib.dump(model, 'Models/customer_care_model.pkl')
model = joblib.load('Models/customer_care_model.pkl')