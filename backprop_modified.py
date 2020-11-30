import backprop as bp
import numpy
import pandas
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer

df = pandas.read_csv("data.csv")
data_full = df[:1100]
data_test = df[1100:]

X_full = data_full.drop('charges', axis=1)
y_full = numpy.array(data_full['charges'])
y_full = y_full.reshape((len(y_full), 1))

X_test = data_test.drop('charges', axis=1)
y_test = numpy.array(data_test['charges'])
y_test = y_test.reshape((len(y_test), 1))


data_inputs_full = numpy.array(X_full).T
data_outputs_full = numpy.array(y_full).T

data_inputs_test = numpy.array(X_test).T
data_outputs_test = numpy.array(y_test).T


mean_full = numpy.mean(data_inputs_full, axis=1, keepdims=True)
std_dev_full = numpy.std(data_inputs_full, axis=1, keepdims=True)

mean_test = numpy.mean(data_inputs_test, axis=1, keepdims=True)
std_dev_test = numpy.std(data_inputs_test, axis=1, keepdims=True)


for i in range(data_inputs_full.shape[0]):
    if std_dev_full[i] != 0:
        data_inputs_full[i] = (data_inputs_full[i] - mean_full[i])/std_dev_full[i]
    else:
        data_inputs_full[i] = data_inputs_full[i] - mean_full[i]

for i in range(data_inputs_test.shape[0]):
    if std_dev_test[i] != 0:
        data_inputs_test[i] = (data_inputs_test[i] - mean_test[i])/std_dev_test[i]
    else:
        data_inputs_test[i] = data_inputs_test[i] - mean_test[i]

num_inputs = 12

description = [{"num_nodes" : 12, "activation" : "relu"},
               {"num_nodes" : 1, "activation" : "relu"}]

model = bp.NeuralNetwork(description,num_inputs,"mean_squared", data_inputs_full, data_outputs_full, learning_rate=0.001)

print(data_inputs_full)

error = model.calc_accuracy(data_inputs_test,data_outputs_test, "RMSE")
f=open("base_error","a")
f.write("0" + "," + str(error) + "\n")
f.close()

for i in range(1,51):
    model.data = data_inputs_full
    model.labels = data_outputs_full
    if i == 1:
        print(model.data)
    model.train(100)
    error = model.calc_accuracy(data_inputs_test,data_outputs_test, "RMSE")
    f=open("base_error","a")
    f.write(str(i) + "," + str(error) + "\n")
    f.close()
    


