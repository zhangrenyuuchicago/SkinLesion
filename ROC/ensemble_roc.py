import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn import metrics

img_name_lt = []
ground_truth_lt = []
pred_lt = []

fin = open('../ensemble_pred.csv', 'r')
fin.readline()
while True:
    line = fin.readline().strip()
    if not line:
        break
    array = line.split(',')
    img_name = array[0]
    ground_truth = int(array[1])
    pred = [float(array[2]), float(array[3]), float(array[4]), float(array[5])]
    img_name_lt.append(img_name)
    ground_truth_lt.append(ground_truth)
    pred_lt.append(pred)

ground_truth_lt = np.array(ground_truth_lt)
pred_lt = np.array(pred_lt)

cata_ground_truth_lt = np.zeros((ground_truth_lt.size, ground_truth_lt.max()+1))
cata_ground_truth_lt[np.arange(ground_truth_lt.size), ground_truth_lt] = 1

macro_avg_auc = metrics.roc_auc_score(cata_ground_truth_lt, pred_lt, average='macro')
print(f'macro average auc: {macro_avg_auc}')

micro_avg_auc = metrics.roc_auc_score(cata_ground_truth_lt, pred_lt, average='micro')
print(f'micro average auc: {micro_avg_auc}')

fpr, tpr, thresholds = metrics.roc_curve(ground_truth_lt, pred_lt[:,0], pos_label=0)
auc = metrics.auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'None-cancer (AUC = {auc:.3f})')

fpr, tpr, thresholds = metrics.roc_curve(ground_truth_lt, pred_lt[:,1], pos_label=1)
auc = metrics.auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'Bowen\'s (AUC = {auc:.3f})')


fpr, tpr, thresholds = metrics.roc_curve(ground_truth_lt, pred_lt[:,2], pos_label=2)
auc = metrics.auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'SCC (AUC = {auc:.3f})')

fpr, tpr, thresholds = metrics.roc_curve(ground_truth_lt, pred_lt[:,3], pos_label=3)
auc = metrics.auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'BCC (AUC = {auc:.3f})')

#plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Chance', alpha=.8)
plt.plot([0, 1], [0, 1], linestyle='--')

plt.xlabel('FPR')
plt.ylabel('TPR')
#plt.title('ROC of ensemble model on external dataset')
plt.legend(loc='lower right')
plt.savefig('4class_roc.png')


