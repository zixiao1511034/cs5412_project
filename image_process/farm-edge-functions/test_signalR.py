import requests
import jwt
import time
import json
import threading
"""
iss: jwt签发者
sub: jwt所面向的用户
aud: 接收jwt的一方
exp: jwt的过期时间，这个过期时间必须要大于签发时间
nbf: 定义在什么时间之前，该jwt都是不可用的.
iat: jwt的签发时间
jti: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击
"""
#https://jwt.io/
#http://sonicguo.com/2018/Azure-SignalR-Service-REST-API-Call/
accesskey = "mlZbIlFbnc0tUFbdIZ300LMaVuzEMGys5Cyg4/mS+/w="
payload = {
  "exp": 1588016543,
  "aud": "https://cow-signalr.service.signalr.net/api/v1/hubs/imageclassification"
}
token = jwt.encode(payload, accesskey, algorithm='HS256')
token = "Bearer " + token.decode('utf-8')

print(str(token))

url = 'https://cow-signalr.service.signalr.net/api/v1/hubs/imageclassification'
#https://cow-signalr.service.signalr.net/api/v1/health
#https://<instance-name>.service.signalr.net/api/v1/hubs/<hub-name>
myobj = {
        'target': 'newResult',
        'arguments': [{
            'predictedTagName': "cow_3",
            'url': "https://cowstoragecloud.blob.core.windows.net/cow-images/2.jpg"
        }]
    }

headers = {'Content-type':'application/json','Accept':'application/json', "Authorization": token}


def send():
    for i in range(50):
        x = requests.post(url, json=myobj,  headers=headers)
        print(x)

threadpool = []
for i in range(10):
    threadpool.append(threading.Thread(target=send))
    threadpool[i].start()

for i in range(10):
    threadpool[i].join()

