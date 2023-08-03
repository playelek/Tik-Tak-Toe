import numpy as np
import json
import os
import sys

class Execution():
    dirpath = os.path.dirname(sys.argv[0])
    coeff_fname = "weight_bias.json"
    dict_coeff = {}
    def __init__(self, network, loss_function = "loss", verbose = True, learning_rate = 0.1, fname = None):
        self.network = list(network)
        self.verbose = verbose
        self.learning_rate = learning_rate
        self.coeff = list()
        if loss_function == "loss":
            self.loss = True
            self.binary_cross = False
        else:
            self.loss = False
            self.binary_cross = True
        self.load_coeff(fname)
        print(f"dictcoeff : {self.dict_coeff}")
        layerCNT = 0
        coeffCNT = 0
        for eachlayer in self.network:
            layerCNT += 1
            eachlayer.setLearningRate(learning_rate)

            if eachlayer.__class__.__name__ == "Dense" and len(self.dict_coeff) > 0:
                thisWeights = self.dict_coeff[coeffCNT]["weights"]
                thisBias = self.dict_coeff[coeffCNT]["bias"]
                if self.verbose == True:
                    print(f"layer : {layerCNT} - coeff : {coeffCNT} - weight : {thisWeights} - bias : {thisBias}")
                eachlayer.weights = np.asarray(thisWeights)
                eachlayer.bias = np.asarray(thisBias)
                coeffCNT += 1
            
    def predict(self, input):
        output = input
        for layer in self.network:
            output = layer.forward(output)
        return output

    def learn(self, x, y, error):
        # forward
        output = self.predict(x)
        thiserror = 0 
        if self.loss :
            # error
            thiserror = self.mse(y, output)+error

            # backward
            grad = self.mse_prime(y, output)
        elif self.binary_cross :
            # error
            thiserror = self.binary_cross_entropy(y, output)+error

            # backward
            grad = self.binary_cross_entropy_prime(y, output)
        else:
                        # error
            thiserror = self.mse(y, output)+error

            # backward
            grad = self.mse_prime(y, output)
                    
        for layer in reversed(self.network):
            grad = layer.backward(grad)
        thiserror /= 2.0
        return thiserror

    def train(self, x_train, y_train, epochs = 1000):
        list_error = list()
        for e in range(epochs):
            error = 0
            for x, y in zip(x_train, y_train):
                error = self.learn(x, y, error)
            # error /= len(x_train)
            list_error.append(error)
            if self.verbose:
                print(f"{e + 1}/{epochs}, error={error}")
                layerCNT = 0
                for eachlayer in self.network:
                    layerCNT += 1
                    # cName = eachlayer.__class__
                    print("class Name : {}".format(eachlayer.__class__.__name__))
                    if eachlayer.__class__.__name__ == "Dense":
                        print(f"{e + 1}/{epochs} - layer : {layerCNT} - weight : {eachlayer.weights} - bias : {eachlayer.bias}")
        layerCNT = 0
        self.coeff = list()
        for eachlayer in self.network:
            layerCNT += 1
            # cName = eachlayer.__class__
            # print("last class Name : {}".format(cName.__name__))
            if eachlayer.__class__.__name__ == "Dense":
                if self.verbose:
                    print(f"layer : {layerCNT} - weight : {eachlayer.weights} - bias : {eachlayer.bias}")
                    print(f"layer : {layerCNT} - weight shape : {eachlayer.weights.shape} - bias shape : {eachlayer.bias.shape}")
                self.coeff.append(dict({"weights" : eachlayer.getWeight(), "bias" : eachlayer.getBias(), "inputSize" : eachlayer.inputSize, "outputSize" : eachlayer.outputSize, "weightShape": eachlayer.weights.shape, "biasShape" : eachlayer.bias.shape}))
        self.save_coeff(self.coeff_fname)
        return list(list_error)
    
    def mse(self, y_true, y_pred):
        return np.mean(np.power(y_true - y_pred, 2))

    def mse_prime(self, y_true, y_pred):
        return 2 * (y_pred - y_true) / np.size(y_true)

    def binary_cross_entropy(self, y_true, y_pred):
        return np.mean(-y_true * np.log(y_pred) - (1 - y_true) * np.log(1 - y_pred))

    def binary_cross_entropy_prime(self, y_true, y_pred):
        return ((1 - y_true) / (1 - y_pred) - y_true / y_pred) / np.size(y_true)

    def load_coeff(self , fname = None):
        if fname == None:
            fname = self.coeff_fname
        print("current file : {}".format(fname))
        flists = open("{}".format(fname), 'r')
        print("flist was open : {}".format(flists))
        dat = flists.read()
        if (self.verbose == True):
            print("JSON data : {}".format(dat))
        if dat :
            self.dict_coeff = json.loads(dat)
        else:
            self.dict_coeff = {}
        # print("state_action : {}".format(self.state_action))

    def save_coeff(self , fname = None):
        if fname == None:
            fname = self.coeff_fname
        coeff_json = json.dumps(self.coeff, indent=4)
        print("current file : {}".format(fname))
        flists = open("{}".format(fname), 'w')
        print("flist was open")
        flists.write(coeff_json)
        flists.close()
        print("flist was closed")
    