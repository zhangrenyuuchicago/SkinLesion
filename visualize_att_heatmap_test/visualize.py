import openslide
import sys
from PIL import Image, ImageDraw
import glob
import os
import numpy as np
grid_size = 1000

index_label = ['None-cancer', 'bowens1', 'scc1', 'bcc1']

def visualize(slide_file):
    slide = openslide.open_slide(slide_file)
    level = slide.level_count - 1
    print(f'level number: {level+1}')
    width, height = slide.level_dimensions[level]
    try:
        image = slide.read_region((0, 0), level, (width, height))
    except:
        print(f'error read image')
        return
    top_width, top_height = slide.level_dimensions[0]
    print(f'read width:{width}, height:{height}')
    thb_width = 3000
    if slide.properties['openslide.objective-power'] == '40':
        size = (2*grid_size, 2*grid_size)
    elif slide.properties['openslide.objective-power'] == '20':
        size = (grid_size, grid_size)
    else:
        print('system fault: no objective power ')
        return
    rate = top_width * 1.0 / thb_width
    thb_height = int(top_height/rate)
    print(f'resize width:{thb_width}, height:{thb_height}')
    small_image = image.resize((thb_width, thb_height), Image.BILINEAR)
    output_small_image = small_image

    slide_id = os.path.basename(slide_file)[:-4]

    file_name = f'{slide_id}_orginal.png'
    if os.path.exists(file_name):
        return
    output_small_image.save(file_name)
    
    base_layer = small_image
    
    color_layer1 = Image.new('RGBA', base_layer.size, (127,127,127))
    draw1 = ImageDraw.Draw(color_layer1, 'RGBA')
    
    color_layer2 = Image.new('RGBA', base_layer.size, (127,127,127))
    draw2 = ImageDraw.Draw(color_layer2, 'RGBA')
 
    color_layer3 = Image.new('RGBA', base_layer.size, (127,127,127))
    draw3 = ImageDraw.Draw(color_layer3, 'RGBA')

    width = int(thb_width*1.0 / top_width * size[0])
    height = width
    ground_truth = 0
    for tile_pred_path in glob.glob(f'tile_pred/{slide_id}*.txt'):
        basename = os.path.basename(tile_pred_path)[:-4]
        array = basename.split('_')
        x = int(array[2][4:])
        y = int(array[3][4:])
        x = int(x/rate)
        y = int(y/rate)
        fin = open(tile_pred_path, 'r')
        pred1_lt, pred2_lt, pred3_lt = [], [], []
        for line in fin.readlines():
            array = line.strip().split()
            ground_truth = int(array[0])
            pred1 = float(array[2])
            pred2 = float(array[3])
            pred3 = float(array[4])
            pred1_lt.append(pred1)
            pred2_lt.append(pred2)
            pred3_lt.append(pred3)
        fin.close()

        mean1 = np.mean(np.array(pred1_lt))
        mean2 = np.mean(np.array(pred2_lt))
        mean3 = np.mean(np.array(pred3_lt))

        color1 = int(mean1*255)
        color2 = int(mean2*255)
        color3 = int(mean3*255)

        draw1.rectangle([(x,y), (x+width-1, y+height-1)], fill=(color1, color1, color1))
        draw2.rectangle([(x,y), (x+width-1, y+height-1)], fill=(color2, color2, color2))
        draw3.rectangle([(x,y), (x+width-1, y+height-1)], fill=(color3, color3, color3))
    
    #small_image = Image.blend(base_layer, color_layer, alpha=0.7)
    small_image1 = color_layer1
    file_name1 = f'{slide_id}_ground_truth_{index_label[ground_truth]}_heat_map_for_bowens1.png'
    small_image1.save(file_name1)

    small_image2 = color_layer2
    file_name2 = f'{slide_id}_ground_truth_{index_label[ground_truth]}_heat_map_for_scc1.png'
    small_image2.save(file_name2)

    small_image3 = color_layer3
    file_name3 = f'{slide_id}_ground_truth_{index_label[ground_truth]}_heat_map_for_bcc1.png'
    small_image3.save(file_name3)


path_lt =  glob.glob('/mnt/data1/New_Best_Digital_Pathology/*/*.svs')
import random
random.shuffle(path_lt)
for slide_file in path_lt:
    visualize(slide_file)


