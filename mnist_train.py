import numpy
import matplotlib.pyplot as plt
import backprop as bp
from scipy.cluster.vq import kmeans, vq

X = numpy.array([1.,2.,3.,5.,2.,4.,100.,101., 150., 160., 201., 202., 204.])

centroids, _ = kmeans(X,2)

clx, _ = vq(X,centroids)

if((clx == 0).sum() > (clx == 1).sum()):
    indices = [i for i, value in enumerate(clx) if value == 0]
else:
    indices = [i for i, value in enumerate(clx) if value == 1]
print(indices)
