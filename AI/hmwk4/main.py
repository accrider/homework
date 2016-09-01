import numpy as np
import matplotlib.pyplot as plt
import math


def load_data(t):
    types = ["X", "Y", "Z", "L"]
    a = []
    for ty in types:
        a.append(np.loadtxt("data/"+t+ty+".txt"))
    return zip(*a)


def dist(d1,d2):
    return math.sqrt(sum([(d1[idx] - d2[idx])**2 for idx in range(3)]))


def get_neighbors(d, data, k):
    i = 0
    r = []
    for a in sorted(data, key=lambda x: dist(x, d)):
        if i >= k:
            break
        if a != d:
            r.append(a)
            i += 1
    return r


def get_prediction(set):
    return round(sum([x[3] for x in set]) / len(set))

train_data = load_data("train")
test_data = load_data("test")
results = []
for i2 in range(20):
    i = 0.0
    for d in test_data:
        neighbors = get_neighbors(d, train_data, i2+1)
        if get_prediction(neighbors) == d[3]:
            i += 1
    results.append([i2+1, (i / len(test_data)) * 100])
    print(str(i2+1) + ": A: " + str((i / len(test_data))*100) + "%")

best = sorted(results, key= lambda x: x[1], reverse=True)[0]
print("Best results: k=" + str(best[0]) + " Accuracy: " + str(best[1]) + "%")
results = zip(*results)
plt.plot(results[0], results[1])
plt.plot(best[0], best[1], 'ro')
plt.axis([0, 20, 40, 100])
plt.show()
