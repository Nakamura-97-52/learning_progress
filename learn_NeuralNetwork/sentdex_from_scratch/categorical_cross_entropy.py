target = [1,0,0]
softmax_output = [0.7,0.2,0.1]

import math

loss = -(target[0]*math.log(softmax_output[0])+
         target[1]*math.log(softmax_output[1])+
         target[2]*math.log(softmax_output[2]))

print(loss)

print(-math.log(softmax_output[0]))

