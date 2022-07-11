inputs = [1,2,3,4]
weights = [[1,2,3,4],
           [1,0.2,3,0.5],
           [1,2,3,4]]
biases = [1,2,3]

import numpy as np

output = np.dot(weights,inputs) + biases

print(output)
# print(list(zip(inputs,weights)))

# for n_input,weight in zip(inputs,weights):
#     print(n_input*weight)
# layer_outputs = []
# for n_weight, n_bias in zip(weights,biases):
#     neuron_output = 0
#     for n_input,weight in zip(inputs,n_weight):
#         neuron_output += n_input*weight
#     neuron_output += n_bias
#     layer_outputs.append(neuron_output)

# print(layer_outputs)

# print(layer_outputs)