#!/usr/bin/env python

from optparse import OptionParser
import csv
import sys
import os
import tqdm
import glob
import ntpath

import util 

stad_dir = "/mnt/data3/best_digital_pathology/"
slide_path_lt = glob.glob(stad_dir + "/*/*.svs")

def gen_tile_proc(sub_slide_path_lt):
    for file_path in sub_slide_path_lt:
        basename = ntpath.basename(file_path)
        util.gen_tile(file_path, './tiles_20X_299/')


from multiprocessing import Process
proc_num = 40
inter = int(len(slide_path_lt) / proc_num) + 1
p_lt = []

for i in range(proc_num):
    start = i*inter
    end = (i+1)*inter
    if end > len(slide_path_lt):
        end = len(slide_path_lt)
    sub_slide_path_lt = slide_path_lt[start: end]
    p_lt.append(Process(target=gen_tile_proc, args=(sub_slide_path_lt,)))
    p_lt[i].start()

for i in range(proc_num):
    p_lt[i].join()

