
import numpy as np

layer_outputs = [[4.8, 1.21,2.385],
                 [8.9,-1.81,0.2],
                 [1.41,1.051,0.026]]

e_nums = np.exp(layer_outputs)
print(e_nums)

normalized_values = e_nums / np.sum(layer_outputs,axis=1,keepdims=True)

print(normalized_values)
print(np.sum(normalized_values, axis=1,keepdims=True))
normalized_values = e_nums / np.sum(e_nums)


# e_nums = [E**n for n in layer_outputs]
# n_base = sum(e_nums)
# normalized_values = [ n / n_base for n in e_nums]
# print(normalized_values)
# print(sum(normalized_values))
