import logging

import azure.functions as func

"""
def main(msg: func.QueueMessage) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
"""

import logging
import azure.functions as func
import json
#from .predict import predict_url
from .predict import predict_image_from_url

def main(msg: func.QueueMessage) -> str:
    image_url = msg.get_body().decode('utf-8')
    logging.info(image_url)
    results = predict_image_from_url(image_url)
    results["url"] = image_url
    #logging.info(f"{results['imageurl']} {image_url}")
    logging.info(results)  
    '''
    return json.dumps({
        'target': 'newResult',
        'argument': [results]
    })   
    '''
    return json.dumps({
        'target': 'newResult',
        'arguments': [{
            'predictedTagName': results['predictedTagName'],
            'url': image_url
        }]
    })