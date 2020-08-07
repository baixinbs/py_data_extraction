from numpy import array
import pandas

data = array([
    [0.1, 0.2],
    [0.2, 0,3],
    [0.3, 0.4],
    [0.4, 0.5],
    [0.5, 0.6]
])

print(data.shape)

data = data.reshape(1,5,2)
print(data.shape)