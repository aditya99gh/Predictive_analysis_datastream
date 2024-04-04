# Imports
import numpy as np
import mysql.connector
import random
import numpy as np
import pandas as pd
#from skmultiflow.drift_detection import DDM
from skmultiflow.drift_detection.adwin import ADWIN
from skmultiflow.data import DataStream
from skmultiflow.meta import OnlineBoostingClassifier
from skmultiflow.bayes import NaiveBayes
from skmultiflow.meta import OzaBaggingADWINClassifier
from skmultiflow.lazy import KNNADWINClassifier
from skmultiflow.lazy import KNNClassifier
from skmultiflow.meta import OnlineSMOTEBaggingClassifier
from skmultiflow.meta import OzaBaggingClassifier


mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="data_equipments")
mycursor = mydb.cursor(prepared=True)



adwin = ADWIN()

# Adding stream elements to ADWIN and verifying if drift occurred

sql = "select BatchesProduced - BatchesRejected as BatchesGood from tblStream1"
mycursor.execute(sql)
x = mycursor.fetchall()
drift_df = []

for j in x:
    drift_df.append(j[0])

#print(drift_df)
#df = pd.DataFrame(drift_df)

#print(x[0][0])
'''
sql1 = "select CircuitId, ShiftId, BatchesProduced - BatchesRejected from tblStream"
mycursor.execute(sql1)
y = mycursor.fetchall()
df1 = pd.DataFrame(y)
print(df1[:10])

print(final_df[-331])
'''


flag = 0
for i in range(len(x)):
    adwin.add_element(x[i][0])
    if adwin.detected_change():
        print('Change detected in data: ' + str(x[i][0]) + ' - at index: ' + str(i))
        flag = 1

if flag == 0:
    print("No Change Detected")




sql = "select CircuitId, ShiftId, BatchesProduced, BatchesRejected, Efficient from tblStream1"
mycursor.execute(sql)
y = mycursor.fetchall()
df = pd.DataFrame(y)


#OZA BAGGING

stream1 = DataStream(df)
stream1.n_remaining_samples()
stream1.prepare_for_use()
knn = KNNClassifier(n_neighbors=8, leaf_size=40, max_window_size=1000)
learner = OzaBaggingClassifier(base_estimator=knn, n_estimators=3, random_state=112)
first = True


cnt = 0
max_samples = 3500
predictions = []
wait_samples = 100
correct_predictions= 0

while cnt < max_samples:
    X, y = stream1.next_sample()
    # Test samples
    if (cnt % wait_samples == 0) and (cnt != 0):
        predictions.append(learner.predict(X)[0])
        if y[0] == predictions[-1]:
            correct_predictions += 1
    if first:
        learner.partial_fit(X, y, classes=stream1.target_values)
        first = False
    else:
        learner.partial_fit(X, y)
    cnt += 1

performance = correct_predictions / len(predictions)
print('Oza Bagging performance:', performance)



'''
#Online Boosting Algorithm

#Initialize the stream
stream1 = DataStream(df)
stream1.prepare_for_use()
nb = NaiveBayes()

first = True

# Setup variables to control loop and track performance
n_samples = 0
correct_cnt = 0
max_samples = 3500

# Setup the Online Boosting Classifier
learner = OnlineBoostingClassifier(base_estimator=nb, n_estimators=3, random_state=1)


# Train the classifier with the samples provided by the data stream

while n_samples < max_samples and stream1.has_more_samples():
    X, y = stream1.next_sample()
    y_pred = learner.predict(X)
    if y[0] == y_pred[0]:
        correct_cnt += 1
    learner.fit(X, y, classes=stream1.target_values)
    n_samples += 1

# Display results
print('{} samples analyzed.'.format(n_samples))
print('Online Boosting performance: {}'.format(correct_cnt / n_samples))
'''









