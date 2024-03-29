import numpy as np
from layer import Layer

class Dense(Layer):
    def __init__(self, input_size, output_size):
        self.inputSize = input_size
        self.outputSize = output_size
        self.weights = np.random.randn(self.outputSize, self.inputSize)
        self.bias = np.random.randn(self.outputSize, 1)

    def forward(self, input):
        self.input = input
        return np.dot(self.weights, self.input) + self.bias

    def backward(self, output_gradient):
        weights_gradient = np.dot(output_gradient, self.input.T)
        input_gradient = np.dot(self.weights.T, output_gradient)
        self.weights -= self.learning_rate * weights_gradient
        self.bias -= self.learning_rate * output_gradient
        return input_gradient

    
