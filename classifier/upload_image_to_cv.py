from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateEntry,
)
import os
import random
import glob
import json
import time

ENDPOINT = "<ENDPOINT>"

# Replace with a valid key
training_key = "<TRAINING KEY>"
prediction_key = "<PREDICTION KEY>"
prediction_resource_id = "<RESOURCE ID>"

publish_iteration_name = "ITERATION NAME"

trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)

# Create a new project
print("Creating project...")
project = trainer.create_project("My New Project")
print(project.id)

# create tags in new project
cow_tags = []
cow_tags_strings = ["cow_{id}".format(id=i) for i in range(1, 90)]
for tag in cow_tags_strings:
    train_tag = trainer.create_tag(project.id, tag)
    # print(train_tag)
    cow_tags.append(train_tag)


# upload image from locol dataset and attach tags
image_list = []
cow_ids = [i for i in range(1, 90)]
for id in cow_ids:
    data_path = "E:/Study/Cornell Course Materials 2020 Spring/CS 5412/Project/dataset/2yizcfbkuv4352pzc32n54371r/{folder}".format(
        folder=id
    )
    image_path = glob.glob(os.path.join(data_path, "*.jpg"))
    if len(image_path) < 7:
        continue
    random.shuffle(image_path)
    for image in image_path[:7]:
        image = image.replace("\\", "/")
        print("uploading cow_{id}".format(id=id))
        with open(image, "rb") as image_contents:
            image_list.append(
                ImageFileCreateEntry(
                    name="cow_{id}.jpg".format(id=id),
                    contents=image_contents.read(),
                    tag_ids=[cow_tags[id - 1].id],
                )
            )

    upload_result = trainer.create_images_from_files(project.id, images=image_list)
    image_list = []
    print(upload_result.is_batch_successful)
    time.sleep(5)


if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    exit(-1)
