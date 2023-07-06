import matplotlib.pyplot as plt 
import numpy as np 

r1 = np.linspace(0, 50, 500)
r2 = 7.4*r1/(4.6-0.17*r1)

plt.figure()
plt.plot(r1, r2)
plt.show()