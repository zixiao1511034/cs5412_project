import cv2 as cv
import os

import time
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from azure.storage.blob import BlockBlobService, ContentSettings
from azure.storage.queue import QueueService, QueueMessageFormat

from predict import initialize, predict_image

import pymongo
import datetime

account_name = "cowimagestorage"
account_key = ""

block_blob_service = BlockBlobService(
    account_name=account_name,
    account_key=account_key
)
queue = QueueService(connection_string="")
queue.encode_function = QueueMessageFormat.text_base64encode

 
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["camera-image"]



def process_single_file(filename, blob, dirname=""):

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    with open('{dirname}/{filename}'.format(filename=filename, dirname=dirname), 'rb') as image:
    # record = {"filename": filename,
    #      "blob": blob,
    #      "date": datetime.datetime.utcnow()}
    # records = mydb.records
    # record_id = records.insert_one(record).inserted_id     

        r = predict_image(image)
        #RPC CALL PREDICTION USING DB URL
        tagName = r["predictions"][0]["tagName"]
        # tagName = "cow"
        if tagName == "cow":
            print(f'{dirname}/{filename}')
            push_start = time.time()
            container_id = int(filename.split(".")[0])%5 + 1
            print(f'test{container_id}')
            block_blob_service.create_blob_from_path(f'test{container_id}',
                                                    f'{filename}',
                                                    f'{dirname}/{filename}',
                                                    content_settings=ContentSettings(content_type='image/jpeg'))
            # block_blob_service.create_blob_from_bytes(f'test{container_id}',
            #                                         f'{filename}',
            #                                         blob,
            #                                         content_settings=ContentSettings(content_type='image/jpeg'))
                                            
            push_end = time.time()
            print("push blob time: {} sec".format(push_end-push_start))
            put_start = time.time()
            queue.put_message("imagequeue", f"https://cowimagestorage.blob.core.windows.net/test{container_id}/"+ filename)
            put_end = time.time()
            print("put message: {}".format(put_end-put_start))

        else:
            pass
        print("------------------------------------------------------------------")



def sampling(video, path_output_dir=None):
    vidcap = cv.VideoCapture(video)
    count = 1

    with ThreadPoolExecutor(20) as executor:
        jobs = []
        results_done = []

        while vidcap.isOpened():
            success, image = vidcap.read()
            if success:
                # image = image.tobytes()
                filename = str(count) + ".jpg"
                cv.imwrite(os.path.join(path_output_dir, '%d.jpg') % count, image)
                kw = {"filename": filename, "blob": image, "dirname":path_output_dir}
                jobs.append(executor.submit(process_single_file, **kw))
                count += 1
            else:
                break
        cv.destroyAllWindows()
        vidcap.release()
        
    for job in futures.as_completed(jobs):
            # Read result from future
            result_done = job.result()
            # Append to the list of results
            results_done.append(result_done)

    for result in results_done:
        print("Do something with me {}".format(result))


initialize()
sampling("./mix_video.avi", "../sample_image")
# upload_video("./mix_video.avi")
time.sleep(10)
