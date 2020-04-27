import requests
import os
import json
from azure.storage.blob import BlockBlobService, ContentSettings
from threading import Thread
import time
import sys
from .predict import initialize, predict_image

print("Azure Blob storage v12 - Python quickstart sample")

account_name = "<ACCOUNT_NAME>"
account_key = "ACCOUNT_KEY"

block_blob_service = BlockBlobService(
    account_name=account_name,
    account_key=account_key
)

def process_single_file(filename):
    
    with open('../test_image/{filename}'.format(filename=filename), 'rb') as image:
    
        predict_start = time.time()

        r = predict_image(image)
        predict_end = time.time()
        print("predict time: {} sec".format(predict_end-predict_start))
        tagName = r["predictions"][0]["tagName"]
        if tagName == "cow":
            print(f'{dir_name}/{filename}')
            push_start = time.time()
            block_blob_service.create_blob_from_path('<CONTAINER_NAME>',
                                                    f'{filename}',
                                                    f'{dir_name}/{filename}',
                                                    content_settings=ContentSettings(content_type='image/jpeg'))
            push_end = time.time()
            print("push blob time: {} sec".format(push_end-push_start))
        else:
            pass
        print("------------------------------------------------------------------")


def process_batch_file(file_batch:list):
    for f in file_batch:
        process_single_file(f)

def threaded_process_batch(nthreads, file_list):
    threads = []
    for i in range(0,len(file_list),nthreads):
        file_batch = file_list[i:i+nthreads]
        print(file_batch)
        t = Thread(target=process_batch_file, args=([file_batch]))
        threads.append(t)

    [t.start() for t in threads]
    [t.join() for t in threads]


initialize()

#use your own dir
dir_name = "../test_image"
file_list = os.listdir(dir_name)


tik = time.time()

'''
Processing single image in sequence, uncomment this part
'''
# for f in file_list:
#     process_single_file(f)


'''
Processing images in multi-thread way, uncomment this part
'''
# threaded_process_batch(30, file_list)

tok = time.time()
print("running time: {t}sec".format(t=tok-tik))


