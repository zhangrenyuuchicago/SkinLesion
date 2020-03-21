import random

fin = open('image_biopsy.csv', 'r')
line = fin.readline().strip()
print(line)

record_label = {}
while True:
    line = fin.readline().strip()
    if not line:
        break
    array = line.split(',')
    p_id, s_id = array[2], array[1]
    bowens1, scc1, bcc1, nmsc1 = int(array[3]), int(array[4]), int(array[5]), int(array[6]) 
    label = 0
    if nmsc1 == 0:
        label = 0
        assert bowens1 == 0
        assert scc1 == 0
        assert bcc1 == 0
    elif bowens1 == 1:
        label = 1
    elif scc1 == 1:
        label = 2
    elif bcc1 == 1:
        label = 3
    else:
        print('error')

    if p_id not in record_label:
        record_label[p_id] =  {s_id:label}
    else:
        if s_id in record_label[p_id]:
            assert record_label[p_id][s_id] == label
        else:
            record_label[p_id][s_id] = label

fin.close()

for p_id in record_label:
    if len(record_label[p_id]) > 1:
        print(record_label[p_id].values())

patient_lt = list(record_label.keys())

fold_specimen_lt = [[] for i in range(5)]
while patient_lt:
    patient_id = patient_lt.pop()
    index = random.randint(0,4)
    for s_id in record_label[patient_id]:
        fold_specimen_lt[index].append(s_id)

import json

with open('fold_specimen_lt.json', 'w') as json_file:
        json.dump(fold_specimen_lt, json_file)

'''
for p_id in record_label:
    print(len(record_label[p_id]))
'''
#print(record_label)
