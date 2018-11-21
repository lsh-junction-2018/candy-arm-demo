import time
import os
import io

import subprocess
from goprocam import GoProCamera, constants

from google.cloud import pubsub_v1
from google.cloud import vision
from google.cloud.vision import types


# TODO project_id = "Your Google Cloud Project ID"
# TODO subscription_name = "Your Pub/Sub subscription name"

print(pubsub_v1.__file__)

dirname = os.path.dirname(__file__)


credential_path = os.path.join(dirname, "acn-ai-playground-6bd16d782647.json")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_name}`
subscription_path = subscriber.subscription_path(
    "acn-ai-playground", "candy")

client = vision.ImageAnnotatorClient()


#goproCamera = GoProCamera.GoPro()


def verify_candy_from_image(candy_type, index):
    goproCamera.take_photo(1)
    custom_filename="candy" + str(index) + ".jpg"
    goproCamera.downloadLastMedia(custom_filename=custom_filename)

    files = os.listdir(dirname)


    for f in files:
        if "GOPRO" in f:
            file_name = os.path.join(
                os.path.dirname(__file__),
                f)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)
        if label.description == candy_type:
            print(candy_type + " candy identified")
    
def search_candy(candy_type):
    verify_candy_from_image(candy_type, 0)
    subprocess.run(["python", os.path.join(dirname, "DobotControl.py")])



def callback(message):
    print('Received message: {}'.format(message))
    message.ack()
    if "RED_CANDY" in str(message.data):
        print("red")
        subprocess.run(["python", os.path.join(dirname, "home_pick_slide_place.py")])
    elif "BLUE_CANDY" in str(message.data):
        print("blue")
        subprocess.run(["python", os.path.join(dirname, "DobotControl.py")])
    elif "YELLOW_CANDY" in str(message.data):
        print("yellow")
        search_candy("yellow")
    elif "RESET" in str(message.data):
        print("reset")
        subprocess.run(["python", os.path.join(dirname, "DobotControl.py")])
    elif "STOP" in str(message.data):
        print("stop")
        subprocess.run(["python", os.path.join(dirname, "DobotControl.py")])



subscriber.subscribe(subscription_path, callback=callback)

# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.
print('Listening for messages on {}'.format(subscription_path))

while True:
    time.sleep(0.5)