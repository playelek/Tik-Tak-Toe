class Layer:
    def __init__(self):
        self.input = None
        self.output = None
        self.inputSize = 0
        self.outputSize = 0
        self.weights = None
        self.bias = None
        self.learning_rate = 0.1

    def getWeight(self):
        return self.weights.tolist()

    def setWeight(self, weight):
        # TODO: return output
        pass        
    
    def getBias(self):
        return self.bias.tolist()

    def setBias(self, bias):
        # TODO: return output
        pass  
        
    def forward(self, input):
        # TODO: return output
        pass

    def backward(self, output_gradient):
        # TODO: update parameters and return input gradient
        pass

    def setLearningRate(self, learningRate):
        self.learning_rate = learningRate   
