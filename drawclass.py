import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

x = [0,1,2,3]
y = [ 49,
7589,
2242,
25
      ]

fig = plt.figure()
plt.bar(x, y, 0.4, color="green")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("bar chart")

plt.show()
#plt.savefig("barChart.jpg")