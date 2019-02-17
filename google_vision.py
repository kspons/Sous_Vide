#/usr/bin/python3

import os
import io
import subprocess

def detect_labels():
    subprocess.call('fswebcam -d /dev/video1 myfood.jpg', shell=True)

    from google.oauth2 import service_account
    import sys
    credentials = service_account.Credentials.from_service_account_file('/home/pi/sous_vide/credentials.json')
    #def detect_labels(path, credentials):
    """Detects labels in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open('myfood.jpg', 'rb') as image_file:
    #with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    for label in labels:
        #print(label.description)

        if("beef" in label.description.lower() or "red" in label.description.lower()):
            return "beef"
        if("chicken" in label.description.lower() or "poultry" in label.description.lower()):
            return "chicken"
        if("pork" in label.description.lower()):
            return "pork"
        if("vegetable" in label.description.lower() or "green" in label.description.lower()):
            return "vegetable"
    return "chicken"
        # print(label.description)

#capture webcam image and save it

#print(detect_labels(sys.argv[1],credentials))
