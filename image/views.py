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
from skimage.filters import threshold_otsu, try_all_threshold, sobel
from skimage import exposure
from skimage import data 
from skimage.feature import Cascade
from matplotlib import patches

# Import your CNN model and other necessary libraries

trained_file = data.lbp_frontal_face_cascade_filename()


def show_detected_face(result, detected, title="Face image"):
    plt.imshow(result)    
    img_desc = plt.gca()    
    plt.set_cmap('gray')    
    plt.title(title)    
    plt.axis('off')
    for patch in detected:
        print('patch', patch)        
        img_desc.add_patch(
            patches.Rectangle(
            (patch['c'], patch['r']),
            patch['width'],
            patch['height'],
            fill=False,
            color='r',
            linewidth=2))    
        plt.show()


def imageProcess(img):
    rgb_image = io.imread(img)
    resized_image = transform.resize(rgb_image, (200, 200), anti_aliasing=True)
    grayscale_image = color.rgb2gray(resized_image)
    # sobel_edge = sobel(grayscale_image)
    # thresh = threshold_otsu(grayscale_image)
    # binary = grayscale_image > thresh
    # image_eq =  exposure.equalize_hist(grayscale_image)



    detector = Cascade(trained_file)
    print(detector)
    detected = detector.detect_multi_scale(img=resized_image, scale_factor=1.2, step_ratio=1, min_size=(5, 5), max_size=(500, 500))
    print('detected_val', detected)
    # fig, ax = try_all_threshold(grayscale_image, verbose=False)
    show_detected_face(resized_image, detected)




    # print(type(grayscale_image))
    # plt.imshow(image_eq)
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
        img_path = os.path.join(BASE_DIR, 'media','grayscale','gray.png')
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
