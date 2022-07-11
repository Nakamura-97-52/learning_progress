import numpy as np

#resetting based paramater to random module
np.random.seed(0)

X = [[1,2,3,2.5],
     [2.0,5.0,-1.0,2.0],
     [1.5,2.7,3.3,-0.8]
]

w_s = [[1,5],
       [3,5],
       [1,5],
]

class Layer_Danse:
    def __init__(self,n_inputs,n_nulons):
        # weights shape should be (numbers of nurons,numbers of inputs)
        # [[2,4,5],
        #  [1,3,6],  this is (2,4), the left side number expresses the more major components, 2 means 2lists,
        # ]          righter nuber 4 means denotes the minor components, like the elements of lists
        #            for no need of Transpose, in advanse made weights reversed looks like (numbers of inputs,numbers of nurons)
        self.weights = 0.1*np.random.randn(n_inputs,n_nulons)
        self.biases = np.zeros((1,n_nulons))
        pass
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
        pass
    
layer1 = Layer_Danse(4, 2)
layer1.forward(X)
layer2 = Layer_Danse(2, 6)
layer2.forward(layer1.output)

print(layer1.output)
print(layer2.weights)