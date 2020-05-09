
from azure.storage.queue import QueueService, QueueMessageFormat
import base64
import time

queue = QueueService(connection_string="DefaultEndpointsProtocol=https;AccountName=cowstoragecloud;AccountKey=wySJgs4UvJqhZUjubvX7lgSiU6/k5qSxUbee2K5hzVPnUq7HsI358u7wzVLQv50b2Kcy66oeIUBB8qESg2C4Tg==;EndpointSuffix=core.windows.net")
queue.encode_function = QueueMessageFormat.text_base64encode


for k in range(5):
    for i in range(1, 16):
        queue.put_message("imagequeue", "https://cowstoragecloud.blob.core.windows.net/cow-images/%s.jpg"%(i))
        print("epoch: %s and send %s message"%(k, i))
        #time.sleep()