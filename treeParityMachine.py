import numpy as np
import random

class tpm:
    def __init__(self, N, K, L):
        self.N, self.K, self.L = N, K, L
        self.weights1 = None
        self.weights2 = None
        self.inputs = None
        self.output = None

    def randomWeights(self):
        """Generates random weights for the tree parity machine"""
        random.seed()
        self.weights = np.array([random.randint(-self.L, self.L) for x in range(self.N*self.K)])

    def randomInputs(self):
        """Generates random inputs for the tree parity machine"""
        random.seed()
        self.inputs = np.array([random.randint(-1, 1) for x in range(self.N*self.K)])

    def signum(self, x):
        """Activation function for hidden layer neurons"""
        if x > 0:
            return 1
        return -1

    def calcWeights2(self):
        """Calculates the inputs to the output neuron"""
        self.weights2 = [self.signum(np.dot(self.weights[x*self.N:x*self.N+self.N],self.inputs[x*self.N:x*self.N+self.N])) for x in range(self.K)]

    def tow(self):
        """Activation function for the output neuron"""
        self.output = 1
        for x in self.weights2:
            self.output *= x

    def theta(self, a, b):
        if a != b:
            return 0
        return 1

    def HebbianLearning(self, aout, bout):
        """Modified Hebbian Learning algorithm for updating weights"""
        for x in range(self.N*self.K):
            self.weights[x] += self.weights2[int(x/self.N)]*self.inputs[x]*self.theta(self.weights2[int(x/self.N)], aout)*self.theta(aout, bout)
            
            if self.weights[x] > self.L:
                self.weights[x] = self.L
            elif self.weights[x] < -self.L:
                self.weights[x] = -self.L

