
import numpy as np

class LinearRegression():
    
    def __init__(self, X, y, alpha=0.03, n_iter=500):
        self.alpha = alpha
        self.n_iter = n_iter
        self.n_samples = len(y)
        self.n_features = np.size(X, 1)
        self.X = np.hstack((np.ones(
            (self.n_samples, 1)), (X - np.mean(X, 0)) / np.std(X, 0)))
        self.y = y[:, np.newaxis]
        self.params = np.zeros((self.n_features + 1, 1))
        self.coef_ = None
        self.intercept_ = None


    def fit(self):
        for i in range(self.n_iter):
            self.params = self.params - (self.alpha/self.n_samples)* np.matmul(self.X.T, (np.matmul(self.X,self.params) - self.y))
            print(i)
        self.intercept_ = self.params[0]
        self.coef_ = self.params[1:]

        return self


    def score(self, X=None, y=None):

        if X is None:
            X = self.X
        else:
            n_samples = np.size(X, 0)
            X = np.hstack((np.ones(
                (n_samples, 1)), (X - np.mean(X, 0)) / np.std(X, 0)))

        if y is None:
            y = self.y
        else:
            y = y[:, np.newaxis]

        y_pred = X.dot(self.params) 
        score = 1 - (((y - y_pred)**2).sum() / ((y - y.mean())**2).sum())

        return score

    def RMSE(self, X=None, y=None):
        if X is None:
            X = self.X
        else:
            n_samples = np.size(X, 0)
            X = np.hstack((np.ones(
                (n_samples, 1)), (X - np.mean(X, 0)) / np.std(X, 0)))

        if y is None:
            y = self.y
        else:
            y = y[:, np.newaxis]

        y_pred = X.dot(self.params) 
        error = ((y - y_pred)**2).sum()/n_samples

        return error

    def predict(self, X):
        n_samples = np.size(X, 0)
        X = np.hstack((np.ones((n_samples, 1)), (X-np.mean(X, 0))/ np.std(X, 0)))
        print(X.shape)
        print(self.params.shape)
        y = np.matmul( X , (self.params))
        return y

    def get_params(self):

        return self.params
