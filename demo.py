import time
import os
import io

import subprocess
from goprocam import GoProCamera, constants

from google.cloud import pubsub_v1
from google.cloud import vision
from google.cloud.vision import types


# Initialize directory name

dirname = os.path.dirname(os.path.abspath(__file__))

# Set credentials in order to be able to use Google Cloud functionalities (pubsub and vision)

credential_path = os.path.join(dirname, "acn-ai-playground-6bd16d782647.json")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Initialize subscriber to channel running in Google Cloud

subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path("acn-ai-playground", "candy")

client = vision.ImageAnnotatorClient()

# Initilize GoPro camera

goproCamera = GoProCamera.GoPro()

# Start time counter

start_time = time.time()
global command_time
command_time = time.time()


# Take a picture with the GoPro camera and download it to computer
def take_photo():    
    goproCamera.take_photo(1)
    goproCamera.downloadLastMedia()


    files = os.listdir(dirname)

    file_name = ""

    for f in files:
        if "GOPRO" in f:
            file_name = os.path.join(dirname, f)
    return file_name

# Take a picture with the GoPro camera, download it to computer and detect image labels with Google Vision

def take_photo_and_detect_labels():
    # Take a picture
    file_name = take_photo()

    if not file_name:
        print("File not found")
        return

    # Load the image

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

    os.remove(file_name)

    return l

# Take a picture with the GoPro camera, download it to computer and detect image properties with Google Vision

def take_photo_and_analyze():

    file_name = take_photo()

    if not file_name:
        print("File not found")
        return
    
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # Color properties detection

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    for color in props.dominant_colors.colors:
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))

    # Label detection

    response2 = client.label_detection(image=image)
    labels = response2.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)

    # Web detection

    response3 = client.web_detection(image=image)
    annotations = response3.web_detection

    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            print('\nBest guess label: {}'.format(label.label))

    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images found:'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('\n\tPage url   : {}'.format(page.url))

            if page.full_matching_images:
                print('\t{} Full Matches found: '.format(
                       len(page.full_matching_images)))

                for image in page.full_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))

            if page.partial_matching_images:
                print('\t{} Partial Matches found: '.format(
                       len(page.partial_matching_images)))

                for image in page.partial_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('\n\tScore      : {}'.format(entity.score))
            print(u'\tDescription: {}'.format(entity.description))

    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(
            len(annotations.visually_similar_images)))

        for image in annotations.visually_similar_images:
            print('\tImage url    : {}'.format(image.url))

    # Remove image

    os.remove(image_file)


# Action taken when subscriber recieves a message from the channel

def callback(message):
    print('Received message: {}'.format(message))
    message.ack()

    # Discard messages recieved within 5 seconds from connecting to the channel and 1 seconds from previous message
    # That way messages in queue before starting the script and too frequent 

    global command_time
    elapsed_time_from_start = time.time() - start_time
    elapsed_time_since_last_command = time.time() - command_time

    if elapsed_time_from_start > 5 and elapsed_time_since_last_command > 1:

        if "RED_CANDY" in str(message.data):
            print("red")
            command_time = time.time()

            labels = take_photo_and_detect_labels()
            if labels is not None and "red" in labels:
                print("Red candy detected")

            subprocess.run(["python", os.path.join(dirname, "home_pick_slide_place.py")])

        elif "BLUE_CANDY" in str(message.data):
            print("blue")
            labels = take_photo_and_detect_labels()
            if labels is not None and  "blue" in labels:
                print("Blue candy detected")
            subprocess.run(["python", os.path.join(dirname, "home_pick_slide_place.py")])

        elif "YELLOW_CANDY" in str(message.data):
            print("yellow")
            command_time = time.time()

            labels = take_photo_and_detect_labels()
            if labels is not None and  "yellow" in labels:
                print("Yellow candy detected")
            
            subprocess.run(["python", os.path.join(dirname, "home_pick_slide_place.py")])

        elif "RESET" in str(message.data):
            print("reset")
            command_time = time.time()

            subprocess.run(["python", os.path.join(dirname, "home.py")])

        elif "STOP" in str(message.data):
            print("stop")
            command_time = time.time()

        


subscriber.subscribe(subscription_path, callback=callback)

# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.

print('Listening for messages on {}'.format(subscription_path))

while True:
    time.sleep(0.5)