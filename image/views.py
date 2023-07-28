import os
from django.shortcuts import render, redirect

from imgdetail.settings import BASE_DIR
from .models import ProcessedImage
import skimage
import sklearn
from skimage import io, transform, color
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tempfile
from PIL import Image
from django.core.files import File

# Import your CNN model and other necessary libraries


def imageProcess(img):
    rgb_image = io.imread(img)
    resized_image = transform.resize(rgb_image, (200, 200), anti_aliasing=True)
    grayscale_image = color.rgb2gray(resized_image)
    # print(type(grayscale_image))
    # plt.imshow(resized_image)
    # plt.show()
    # gr_image = plt.imshow(grayscale_image, cmap='gray')
    # print(type(gr_image))
    # plt.show()
    # plt.imsave(os.path.join(BASE_DIR, 'media'), gr_image)   
    return grayscale_image
    
    


def process_image(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        processed_image = imageProcess(image_file)
        im2 = Image.fromarray((processed_image*255).astype(np.uint8))
        img_path = os.path.join(BASE_DIR, 'media/grayscale','gray.png')
        im2.save(img_path)
        processed = ProcessedImage()
        processed.image = image_file
        processed.save()
        with open(img_path, 'rb')as file:
            processed.processed.save(os.path.basename(img_path), File(file), save=True)
        os.remove(img_path)
        return redirect('result_page')
    return render(request, 'home.html')



def result_page(request):
    processed_images = ProcessedImage.objects.all()
    return render(request, 'result.html', {'processed_images': processed_images})
