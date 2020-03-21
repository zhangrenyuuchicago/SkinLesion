import numpy as np

confusion_matrix = np.loadtxt('confusion_matrix.txt')

from sklearn.preprocessing import normalize

confusion_matrix = normalize(confusion_matrix, axis=1, norm='l1')

print(confusion_matrix)
