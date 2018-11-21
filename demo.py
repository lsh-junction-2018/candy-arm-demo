import time
import os
import io

import subprocess
from goprocam import GoProCamera, constants

from google.cloud import pubsub_v1
from google.cloud import vision
from google.cloud.vision import types


# Initialize directory name

dirname = os.path.dirname(__file__)

# Set credentials in order to be able to use Google Cloud functionalities (pubsub and vision)

credential_path = os.path.join(dirname, "acn-ai-playground-6bd16d782647.json")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Initialize subscriber to channel running in Google Cloud

subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path(
    "acn-ai-playground", "candy")

client = vision.ImageAnnotatorClient()

# Initilize GoPro camera

goproCamera = GoProCamera.GoPro()

# Take a picture with the GoPro camera, download it to computer and detect image labels with Google Vision

def take_photo_and_detect_labels():
    goproCamera.take_photo(1)
    custom_filename="candy" + str(index) + ".jpg"
    goproCamera.downloadLastMedia(custom_filename=custom_filename)

    files = os.listdir(dirname)

    for f in files:
        if "GOPRO" in f:
            file_name = os.path.join(
                os.path.dirname(__file__),
                f)

    # Load the image on the computer

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Perform label detection on the image file

    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    l = []
    for label in labels:
        print(label.description)
        l.append(label.description)

    return l


# Action taken when subscriber recieves a message from the channel

def callback(message):
    print('Received message: {}'.format(message))
    message.ack()

    if "RED_CANDY" in str(message.data):
        print("red")
        labels = take_photo_and_detect_labels()
        if "red" in labels:
            print("Red candy detected")
        subprocess.run(["python", os.path.join(dirname, "home_pick_slide_place.py")])

    elif "BLUE_CANDY" in str(message.data):
        print("blue")
        labels = take_photo_and_detect_labels()
        if "blue" in labels:
            print("Blue candy detected")
        subprocess.run(["python", os.path.join(dirname, "home_pick_slide_place.py")])

    elif "YELLOW_CANDY" in str(message.data):
        print("yellow")
        labels = take_photo_and_detect_labels()
        if "yellow" in labels:
            print("Yellow candy detected")
        subprocess.run(["python", os.path.join(dirname, "home_pick_slide_place.py")])

    elif "RESET" in str(message.data):
        print("reset")
        subprocess.run(["python", os.path.join(dirname, "home.py")])

    elif "STOP" in str(message.data):
        print("stop")
        


subscriber.subscribe(subscription_path, callback=callback)

# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.

print('Listening for messages on {}'.format(subscription_path))

while True:
    time.sleep(0.5)