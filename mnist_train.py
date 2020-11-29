import numpy
import matplotlib.pyplot as plt
import backprop as bp


from sklearn.datasets import make_regression
X, y = make_regression(n_samples=100, n_features= 10, noise=0.75)


data_inputs = numpy.array(X).T
data_outputs = numpy.array(y).T

mean = numpy.mean(data_inputs, axis = 1, keepdims=True)
std_dev = numpy.std(data_inputs, axis = 1, keepdims=True)

for i in range(data_inputs.shape[0]):
    if std_dev[i] != 0:
        data_inputs[i] = (data_inputs[i] - mean[i])/std_dev[i]
    else:
        data_inputs[i] = data_inputs[i] - mean[i]

num_inputs = 10

description = [{"num_nodes" : 10, "activation" : "relu"},
               {"num_nodes" : 1, "activation" : "tanh"}]

NN_model = bp.NeuralNetwork(description,num_inputs,"mean_squared", data_inputs, data_outputs, learning_rate=0.001)

NN_model.train(4000)

error = NN_model.calc_accuracy(data_inputs, data_outputs, "RMSE")

print(error)
