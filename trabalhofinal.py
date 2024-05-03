# -*- coding: utf-8 -*-
"""TrabalhoFinal.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tI26C8PiP-TFtcQzjdIba7dDF2ovl_XP

# Download do repositório
"""

!git clone https://github.com/alsombra/Mask_RCNN-TF2/

# Commented out IPython magic to ensure Python compatibility.
# %pwd

# Commented out IPython magic to ensure Python compatibility.
# %cd Mask_RCNN-TF2/

# Commented out IPython magic to ensure Python compatibility.
# %pwd

!pip install -r requirements.txt

!python setup.py install

# Commented out IPython magic to ensure Python compatibility.
# %cd ..

"""# Importação das bibliotecas"""

import os
import sys
import random
import math
import cv2
import numpy as np
import skimage.io
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow

import tensorflow as tf
tf.__version__

ROOT_DIR = os.path.abspath('./Mask_RCNN-TF2/')
ROOT_DIR

sys.path

sys.path.append(ROOT_DIR)
sys.path

from mrcnn import utils
from mrcnn import visualize
import mrcnn.model as modellib

sys.path.append(os.path.join(ROOT_DIR, 'samples/coco/'))
sys.path

import coco

MODEL_DIR = os.path.join(ROOT_DIR, 'logs')
IMAGE_DIR = os.path.join(ROOT_DIR, 'images')

print(MODEL_DIR, IMAGE_DIR)

"""# Conexão ao Google Drive (necessário a reconexão a cada acesso)"""

from google.colab import drive
drive.mount('/content/gdrive')

!cp -r /content/gdrive/MyDrive/fotos/ fotos

"""# Carregamento da rede neural pré-treinada"""

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

COCO_MODEL_PATH = os.path.join(ROOT_DIR, 'mask_rcnn_coco.h5')

COCO_MODEL_PATH

if not os.path.exists(COCO_MODEL_PATH):
  utils.download_trained_weights(COCO_MODEL_PATH)

"""# Configurações de inferência

"""

class InferenceConfig(coco.CocoConfig):
  GPU_COUNT = 1
  IMAGES_PER_GPU = 1
config = InferenceConfig()

config.display()

"""# Criação do modelo e carregamento dos pesos"""

MODEL_DIR

model = modellib.MaskRCNN(mode='inference', config=config, model_dir=MODEL_DIR)

model.load_weights(COCO_MODEL_PATH, by_name=True)

"""# Definição do nome das classes"""

class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']

len(class_names)

class_names[42]

class_names.index('cup')

"""#Visualização em RGB"""

rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(rgb)

img = cv2.imread('fotos/maya.jpg')
plt.imshow(img);

"""#Visualização em tons de cinza"""

gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
plt.imshow(gray, cmap='gray')

"""#Visualização do histograma"""

histograma, bins = np.histogram(gray, 256, [0,256]) # 180, 255
histograma
plt.plot(histograma);

"""# Predição e visualização"""

from skimage.io import imread
img = imread('fotos/maya.jpg')
plt.imshow(img);

resultados = model.detect([img], verbose = 0)

resultados

r = resultados[0]
r

print(r['class_ids'])

class_names.index('person')

visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])

print('Segmentos detectados: ', str(len(r['scores'])))

r['scores']

img = imread('/content/fotos/maya.jpg')

def mostrar(imagem):
  fig = plt.gcf()
  fig.set_size_inches(18,8)
  plt.imshow(imagem, cmap='gray')
  plt.axis('off')
  plt.show()

mostrar(img)

def segmentar_imagem(img):
  resultados = model.detect([img], verbose = 0)
  r = resultados[0]
  visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
  print('Segmentos detectados: ', len(r['scores']))
  return r

r = segmentar_imagem(img)

r['class_ids']

class_names[17], class_names[1], class_names[57]

img.shape

r['masks'].shape

"""# Remoção do fundo"""

def segmentar(img, r, idx):
  mask = r['masks'][:,:,idx]
  #print(mask.shape)
  mask = np.stack((mask,)*3, axis = -1)
  #print(mask.shape)
  mask = mask.astype('uint8')
  bg = 255 - mask * 255
  #print(bg.shape)
  #print(mask)
  #print(bg)
  mask_exibir = np.invert(bg)
  mask_img = img * mask
  res = mask_img + bg
  return res, mask_exibir

segmentacao, mask_obj = segmentar(img, r, 1)

mostrar(segmentacao)

mostrar(mask_obj)

def mostrar_segmentacao(img, r, idx, show_mask = False):
  segmentacao, mask_obj = segmentar(img, r, idx)
  plt.subplots(1, figsize=(16,16))
  plt.axis('off')
  if show_mask:
    plt.imshow(np.concatenate([mask_obj, segmentacao], axis = 1))
  else:
    plt.imshow(np.concatenate([img, segmentacao], axis = 1))

mostrar_segmentacao(img, r, 1, show_mask = True)

for indice, roi in enumerate(r['rois']):
  #print(indice, roi)
  mostrar_segmentacao(img, r, indice, True)