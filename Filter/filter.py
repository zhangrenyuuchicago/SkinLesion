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

patient_lt = list(record_label.keys())

fold_patient_lt = [[] for i in range(5)]
while patient_lt:
    patient_id = patient_lt.pop()
    index = random.randint(0,4)
    fold_patient_lt[index].append(patient_id)

s_id_set = set()
for p_id in record_label:
    for s_id in record_label[p_id]:
        s_id_set.add(s_id)

fin = open('files_to_delete.csv', 'r')
fin.readline()
file_to_delete = set()
while True:
    line = fin.readline().strip()
    if not line:
        break
    array = line.split(',')
    file_to_delete.add(array[1])
fin.close()

file_to_delete2 = set()
fin = open('files_to_delete2.txt', 'r')
while True:
    line = fin.readline().strip()
    if not line:
        break
    file_to_delete2.add(line)

fin.close()

import glob
import os

error_set = set()

for path in glob.glob('../gen_tiles/copy/tiles_20X_299/*/*.jpg'):
    basename = os.path.basename(path)
    array = basename.split('_')
    boxname = boxname = os.path.basename(os.path.dirname(path))
    slide_id = array[0]
    array = slide_id.split('-')
    s_id = array[0]
    if s_id in s_id_set:
        if slide_id in file_to_delete:
            print('found one')
            error_set.add(slide_id)
            os.remove(path)        
        if s_id in file_to_delete2:
            print('found one')

print(error_set)


'''
import json
with open('fold_patient_lt.json', 'w') as json_file:
        json.dump(fold_patient_lt, json_file)
for p_id in record_label:
    print(len(record_label[p_id]))
'''
#print(record_label)
