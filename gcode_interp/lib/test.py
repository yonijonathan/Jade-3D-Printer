from datetime import datetime
import random

if __name__ == "__main__":
    start = datetime.now()
    x = []
    x2 = []
    sqrt_x = []
    for i in range(10000):
        x.append(random.random() * 100)
    for j in range(len(x)):
        x2.append(x[j]**2)
    for k in range(len(x2)):
        sqrt_x.append(math.sqrt(x2[k]))
    now = datetime.now() - start
    print(now)
