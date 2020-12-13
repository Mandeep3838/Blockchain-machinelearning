import linear_regression as lr

import numpy
import pandas
import sys

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

data = pandas.read_csv('data.csv')

X = data.drop('charges', axis=1)
y = data['charges']

X = numpy.asarray(X)
y = numpy.asarray(y)

# Normalize
mean = numpy.mean(X,0)
std = numpy.std(X,0)
X = X - mean/ std
# print(X.shape)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
X_train = X[:1000]
y_train = y[:1000]
X_test = X[1000:]
y_test = y[1000:]

sk = LinearRegression().fit(X_train, y_train)
LR = lr.LinearRegression(X_train, y_train).fit()
# print(LR.params.shape)
# print(LR.params)
print("Test accuracy by SK", sk.score(X_test, y_test))
print("Train accuracy by LR", LR.score(X_test, y_test))

predict_sk = sk.predict(X_test)
predict_lr = LR.predict(X_test)

print("MSE on SK", mean_squared_error(y_test,predict_sk))
print("MSE on LR", mean_squared_error(y_test, predict_lr))

print(mean_squared_error)