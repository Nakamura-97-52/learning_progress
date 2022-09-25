from django.shortcuts import render
import io
import os
import json

from torchvision import models
from torchvision import transforms
from PIL import Image
from django.conf import settings

# Create your views here.
# import model from torch vision
model = models.densenet121(pretrained = True)
# no training, then eval mode
model.eval()

json_path = os.path.join(STATIC_ROOT, 'imagenet_class_index.json')
# json.load() takes an argument of file path, returns json object like dictionary form
# open(file) as f
# 
# data = json.load(f)

# for i in data:
#   print(i)
imagenet_mapping = json.load(json_path)

def transform_image(image_bytes):
    """
    Transform image into required DenseNet format: 224x224 with 3 RGB channels and normalized.
    Return the corresponding tensor.
    """
                                        #255 for what?
    my_transforms = transforms.Compose([transforms.Resize(255),

                                        # densenet121 is set with [224,224]
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        # must have been precomputed for your dataset.
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])

# io.BytesIO opens an argument as binary data 
# similar to open()
    image = Image.open(io.BytesIO(image_bytes))
    # densenet121 requires 3 RGB, then add 1 dimention by unsqueeze
    return my_transforms(image).unsqueeze(0)

    