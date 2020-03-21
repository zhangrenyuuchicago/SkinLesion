import torchvision
import torch
import SlideDataset
import pickle
import ntpath
import os
import numpy as np
import torch.nn.functional as F
from tensorboardX import SummaryWriter
from optparse import OptionParser
from datetime import datetime
from sklearn import metrics
import glob
from Model import *
from keras.utils import to_categorical

usage = "usage: python msi_advr.py "
parser = OptionParser(usage)

parser.add_option("-b", "--batch_size", dest="batch_size", type="int", default=32,
                    help="batch size")

(options, args) = parser.parse_args()

batch_size = options.batch_size
embed_len = 10
inst_num = 1

minet = MINet(embed_len, inst_num )
minet = torch.nn.DataParallel(minet).cuda()
soft_layer = torch.nn.Softmax(dim=1)

loss_fn_label = torch.nn.CrossEntropyLoss().cuda()

val_transform = torchvision.transforms.Compose([
            torchvision.transforms.Resize(224),
            torchvision.transforms.ToTensor()
        ])

slide_acc_lt = []

label_index = {'None-cancer':0, 'bowens1':1, 'scc1':2, 'bcc1':3}
label_auc = {'None-cancer':[], 'bowens1':[], 'scc1':[], 'bcc1':[]}
macro_avg_auc = []

confusion_matrix_lt = []

for checkpoint_file in glob.glob('../*.pt'):
    checkpoint_name = os.path.basename(checkpoint_file)
    checkpoint_name = checkpoint_name[:-3]
    array = checkpoint_name.split("_")
    fold = int(array[4])
    print(f'current fold: {fold}')
    test_image_data = SlideDataset.SlideDataset('test', '../../settings/image_biopsy.csv',
        '../../gen_tiles/tiles_20X_1000/',
        val_transform, fold)
    test_data_loader = torch.utils.data.DataLoader(test_image_data, num_workers=6, batch_size=7)

    checkpoint = torch.load(checkpoint_file)
    minet.load_state_dict(checkpoint['minet'])
    best_epoch = checkpoint['epoch']
    best_val_auc = checkpoint['best_val_auc']
    print(f'best epoch: {best_epoch}, best val macro-average auc: {best_val_auc}')    
    ground_truth_lt = []
    pred_lt = []
    img_name_lt = []
    count = 0
    sum_loss = 0.0
    minet.eval()
    for id, (item, label, img_name) in enumerate(test_data_loader):
        item = item.cuda()
        label = label.cuda()
        input_var = torch.autograd.Variable(item, requires_grad=False)
        label = torch.squeeze(label, dim=1)
        label_var = torch.autograd.Variable(label)
        with torch.no_grad():
            label_med  = minet.module.resnet18(input_var)
            label_pred = minet.module.cms_pred(label_med)
            label_soft_pred = soft_layer(label_pred)
        loss_label = loss_fn_label(label_pred, label_var)
        loss = loss_label

        cur_loss = loss.data.cpu().numpy()
        sum_loss += cur_loss
        count += 1
    
        label_pred_np = label_soft_pred.data.cpu().numpy()
        pred_lt = list(label_pred_np)
        ground_truth_lt = list(label_var.data.cpu().numpy())
        img_name_lt = list(img_name)

        for i in range(len(pred_lt)):
            img_name = img_name_lt[i]
            img_name = img_name[:-4]
            fout = open('tile_pred/' + img_name + '.txt', 'a')
            fout.write(str(ground_truth_lt[i]) + ' ' + str(pred_lt[i][0]) + ' ' + str(pred_lt[i][1]) + ' ' + str(pred_lt[i][2]) + ' ' + str(pred_lt[i][3]) + '\n')
            fout.close()


