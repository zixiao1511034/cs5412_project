# import requests
import os
import json
from azure.storage.blob import BlockBlobService, ContentSettings
from threading import Thread
import time
import sys
# from predict import initialize, predict_image
from azure.storage.queue import QueueService, QueueMessageFormat
import base64
# from video2image import sampling
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor


print("Azure Blob storage v12 - Python quickstart sample")
API_ENDPOINT = "http://127.0.0.1:5000/image"

account_name = "cowimagestorage"
account_key = ""

block_blob_service = BlockBlobService(
    account_name=account_name,
    account_key=account_key
)


queue = QueueService(connection_string="")
queue.encode_function = QueueMessageFormat.text_base64encode

def process_single_file(filename, blob, dirname=""):

    # image = {'imageData': open('../test_image/{filename}'.format(filename=filename), 'rb')}
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # with open('{dirname}/{filename}'.format(filename=filename, dirname=dirname), 'rb') as image:
    
        # predict_start = time.time()
        # response = requests.post(API_ENDPOINT, files=image)
        # print("resquest time: {} sec".format(request_end-request_start))

        # r = predict_image(image)
        # predict_end = time.time()
        # print("predict time: {} sec".format(predict_end-predict_start))

        # tagName = r["predictions"][0]["tagName"]
    tagName = "cow"
    if tagName == "cow":
        print(f'{dirname}/{filename}')
        push_start = time.time()
        container_id = int(filename.split(".")[0])%5 + 1
        print(f'test{container_id}')
        # block_blob_service.create_blob_from_path(f'test{container_id}',
        #                                         f'{filename}',
        #                                         f'{dirname}/{filename}',
        #                                         content_settings=ContentSettings(content_type='image/jpeg'))
        
        # block_blob_service.create_blob_from_bytes(f'test{container_id}',
        #                                         f'{filename}',
        #                                         blob,
        #                                         content_settings=ContentSettings(content_type='image/jpeg'))
                                        
        push_end = time.time()
        print("push blob time: {} sec".format(push_end-push_start))
        put_start = time.time()
        # queue.put_message("imagequeue", f"https://cowimagestorage.blob.core.windows.net/test{container_id}/"+ filename)
        put_end = time.time()
        print("put message: {}".format(put_end-put_start))

    else:
        pass
    print("------------------------------------------------------------------")


# def process_batch_file(file_batch:list):
#     for i, f in enumerate(file_batch):
#         process_single_file(f, i)

# def threaded_process_batch(nthreads, file_list):
#     threads = []
#     for i in range(0,len(file_list),nthreads):
#         file_batch = file_list[i:i+nthreads]
#         print(file_batch)
#         t = Thread(target=process_batch_file, args=([file_batch]))
#         threads.append(t)

#     [t.start() for t in threads]
#     [t.join() for t in threads]

def threaded_process_single(batch_size, file_list):
    threads = []
    index = 0
    while index < len(file_list):
        for i in range(index, min(index+batch_size, len(file_list))):
            t = Thread(target=process_single_file, args=(file_list[i], sample_path))
            threads.append(t)
        index += batch_size
        [t.start() for t in threads]
        [t.join() for t in threads]
        threads = []


def thread_pool_process(file_list, sample_path):
    
    
    with ThreadPoolExecutor(20) as executor:
        jobs = []
        results_done = []

        for i in range(2*len(file_list)):
            kw = {"filename": file_list[i%len(file_list)], "dirname": sample_path}
            jobs.append(executor.submit(process_single_file, **kw))
        
        for job in futures.as_completed(jobs):
            # Read result from future
            result_done = job.result()
            # Append to the list of results
            results_done.append(result_done)

        for result in results_done:
            print("Do something with me {}".format(result))

# initialize()

# video_path = "./mix_video.avi"
# sample_path = "../sample_image"
# sampling(video_path, sample_path)
# file_list = os.listdir(sample_path)

# tik = time.time()

# '''
# Processing single image in sequence, use this part
# '''
# for f in file_list:
#     process_single_file(f, sample_path)
    
# tok = time.time()
# print(f"single: {tok-tik}")

'''
Processing images in multi-thread way, use this part
'''
# threaded_process_batch(4, file_list)

# tik = time.time()

# thread_pool_process(file_list, sample_path)
# tok = time.time()
# print(f"thread: {tok-tik}")

# time.sleep(20)

