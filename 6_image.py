#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from PIL import Image
import csv
import cv2
import numpy as np


# In[2]:


def getcolor(colors, photo_color):
    min_dist_id = 0
    min_dist = 0
    for i in range(len(colors)):
        dist = np.linalg.norm(colors[i]-photo_color)
        if i == 0:
            min_dist = dist
        else:
            if min_dist > dist:
                min_dist = dist
                min_dist_id = i
    #print(i, min_dist)
    return min_dist_id


# In[3]:


def getphotocolor(photo):
    colors = np.array([[255, 0, 0], [255, 127, 0], [255, 255, 0], [127, 255, 0], [0, 255, 0], [0, 255, 127], [0, 255, 255], [0, 127, 255], [0, 0, 255], [127, 0, 255], [255, 0, 255], [255, 0, 127]])
    photo_colors_list = [0 for i in range(len(colors))]
    photo_colors = [[0 for j in range(len(photo[i]))]for i in range(len(photo))]
    for i in range(len(photo)):
        for j in range(len(photo[i])):
            colorindex = getcolor(colors, photo[i, j, :])
            photo_colors[i][j] = colorindex
            photo_colors_list[colorindex] = photo_colors_list[colorindex] + 1
    for i in range(len(photo_colors_list)):
        photo_colors_list[i] = photo_colors_list[i] / (len(photo[0]) * len(photo))
    return  photo_colors_list, photo_colors


# In[4]:


images = pd.read_csv('./shizuoka_imgs.csv',header=None, names=['id', 'lat', 'lon'])
images


# In[9]:


image_photos = []
for i in range(len(images)):
    #print(int(images.iloc[i,0]))
    filepath = './image-data/{}.jpg'.format(int(images.iloc[i,0]))
    bgr_array = cv2.imread(filepath)
    photo_colors_list, photo_colors = getphotocolor(bgr_array)
    image_photos.append(photo_colors_list)
    with open('./image-data_colors/{}.csv'.format(int(images.iloc[i,0])), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(photo_colors)


# In[6]:


#image_photos


# In[10]:


with open('./shizuoka_imagecolors.csv'.format(int(images.iloc[i,0])), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(image_photos)


# In[ ]:




