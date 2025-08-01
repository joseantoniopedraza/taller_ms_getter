#!/usr/bin/env python3

import requests
import redis
import json
from datetime import datetime
import config

def send(message):
    print("Sending message")
    r = redis.Redis(host=config.host, 
                    port=config.port)#, 
                    #db=0)

    r.publish(config.channel, message)

def main():
    print("Initializing getter service")           
    tenders = requests.get(config.url_tenders)

    for i in range(5):

        url = config.url_by_code(tenders.json()['Listado'][i]['CodigoExterno'])
        tender = requests.get(url).json()['Listado'][0]

        message= {
            'id': i,
            'status': "pre-processed",
            'createdAt': datetime.now().strftime('%Y-%m-%d'),
            'payload':{
                'code':tender['CodigoExterno'],
                'title': tender['Nombre'],
                'description': tender['Descripcion']
            }
        }

        send(json.dumps(message))

if __name__ == "__main__":
    main() 