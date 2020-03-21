import random
import glob
import ntpath

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

label_specimen = {}
print(f'patient num: {len(patient_lt)}')
fold_specimen_lt = [[] for i in range(5)]
while patient_lt:
    patient_id = patient_lt.pop()
    index = random.randint(0,4)
    for s_id in record_label[patient_id]:
        fold_specimen_lt[index].append(s_id)
        label = record_label[patient_id][s_id]
        if label in label_specimen:
            label_specimen[label].append(s_id)
        else:
            label_specimen[label] = [s_id]

specimen_set = set()
specimen_num = 0
for i in range(len(fold_specimen_lt)):
    specimen_num += len(fold_specimen_lt[i])
    for specimen in fold_specimen_lt[i]:
        specimen_set.add(specimen)
        
print(f'specimen num: {specimen_num}')

slide_set = set()
total_slide_set = set()

ids = glob.glob('../gen_tiles/copy/tiles_20X_299/*/*.jpg')
for img_name in ids:
    basename = ntpath.basename(img_name)
    array = basename.split("_")
    slide_id = array[0]
    array = slide_id.split('-')
    specimen_id = array[0]
    total_slide_set.add(slide_id)

    if specimen_id in specimen_set:
        slide_set.add(slide_id)

print(f'slide num: {len(slide_set)}')
print(f'total slide num: {len(total_slide_set)}')

for label in label_specimen:
    print(f'label num: {label}, specimen num: {len(label_specimen[label])}')



 
