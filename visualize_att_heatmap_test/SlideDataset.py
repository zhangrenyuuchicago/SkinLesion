import torch
import torchvision.transforms as transforms
import torch.utils.data as data
import os
import pickle
import numpy as np
import nltk
from PIL import Image
import sys
import glob, os
import ntpath
from torch.autograd import Variable 
import torchvision
import json
import random

class SlideDataset(data.Dataset):
    """COCO Custom Dataset compatible with torch.utils.data.DataLoader."""
    def __init__(self, stage, label_file, dir, transform, fold, inst_num=10):
        '''
        read phenotypes
        '''
        self.stage = stage
        assert stage in {'train', 'val', 'test'}
        self.inst_num = inst_num 
        self.specimen_label = {}
        
        fin = open(label_file, 'r')
        fin.readline()
        while True:
            line = fin.readline().strip()
            if not line:
                break
            array = line.split(',')
            pid, sid = array[1], array[0]
            #bowens1, scc1, bcc1, nmsc1 = int(array[3]), int(array[4]), int(array[5]), int(array[6])
            bowens1 = 0 if len(array[3]) == 0 else int(array[3])
            scc1 = 0 if len(array[4]) == 0 else int(array[4])
            bcc1 = 0 if len(array[5]) == 0 else int(array[5])
            nmsc1 = 0 if len(array[6]) == 0 else int(array[6])

            label = 0
            if nmsc1 == 0:
                label = 0
            elif bowens1 == 1:
                label = 1
            elif scc1 == 1:
                label = 2
            elif bcc1 == 1:
                label = 3
            else:
                print('error')
            if sid not in self.specimen_label:
                self.specimen_label[sid] = label
            else:
                assert self.specimen_label[sid] == label
            
        fin.close()

        ids = glob.glob(dir + "/*/*.jpg") 
        print(f'tiles num: {len(ids)}')

        self.specimen_img = {}
                
        for img_name in ids:
            basename = ntpath.basename(img_name)
            array = basename.split("_")
            slide_id = array[0]
            array = slide_id.split('-')
            specimen_id = array[0]
            if specimen_id in self.specimen_img:
                self.specimen_img[specimen_id].append(img_name)
            else:
                self.specimen_img[specimen_id] = [img_name]
        
        '''
        fold_specimen_lt = None
        with open('../../settings/fold_specimen_lt.json') as f:
            fold_specimen_lt = json.load(f)

        if stage == 'train':
            fold_set = []
            for i in range(3):
                fold_i = (fold + i) % 5
                fold_set.append(fold_i)
            mask_id = []
            for fold_i in fold_set:
                mask_id += fold_specimen_lt[fold_i]
        elif stage == 'val':
            assert fold < 5
            fold_i = (fold + 3) % 5
            mask_id = fold_specimen_lt[fold_i]
        else:
            assert fold < 5
            fold_i = (fold + 4) % 5
            mask_id = fold_specimen_lt[fold_i]
        '''

        self.specimen_id = []
        for specimen_id in self.specimen_label:
            if specimen_id in self.specimen_img and len(self.specimen_img[specimen_id]) > 20:
                self.specimen_id.append(specimen_id)
        
        print(f'specimen num: {len(self.specimen_id)}')
        
        self.tile_id = []
        for specimen_id in self.specimen_id:
            self.tile_id += self.specimen_img[specimen_id]

        num_label = {}
        for label in set(self.specimen_label.values()):
            num_label[label] = 0

        for specimen_id in self.specimen_id:
            label = self.specimen_label[specimen_id]
            num_label[label] += 1

        if self.stage == 'train':
            weight_lt = []
            for specimen_id in self.specimen_id:
                label = self.specimen_label[specimen_id]
                weight_lt.append(1.0 / num_label[label])
            weight = np.array(weight_lt)
            np.savetxt('weight.txt', weight)
        
        self.transform = transform
        print( "Initialize end")

    def __getitem__(self, index):
        """Returns one data pair (image and caption)."""
        tile_id = self.tile_id[index]
        basename = os.path.basename(tile_id)
        array = basename.split('_')
        slide_id = array[0]
        array = slide_id.split('-')
        specimen_id = array[0]
        label = self.specimen_label[specimen_id]
        label = torch.LongTensor([label])

        img_name = tile_id
        image = Image.open(img_name)
        if self.transform is not None:
            image = self.transform(image)

        return image, label, basename

        '''
        specimen_id = self.specimen_id[index]
        label = self.specimen_label[specimen_id]
        label = torch.LongTensor([label])
        
        image_lt = []
        sample_lt = random.sample(self.specimen_img[specimen_id], self.inst_num)
        for img_name in sample_lt:
            image = Image.open(img_name)
            if self.transform is not None:
                image = self.transform(image)
                image_lt.append(image)

        image_lt = torch.stack(image_lt)
        return image_lt, label, specimen_id
        '''

    def __len__(self):
        return len(self.tile_id)


