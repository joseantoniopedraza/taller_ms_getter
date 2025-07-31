#!/usr/bin/env python3

import requests
import config
import json
from datetime import datetime
import redis

def send(message):
    r = redis.Redis(host=config.host, 
                    port=config.port)#, 
                    #db=0)

    r.publish(config.canal, message)

def main():
    licitaciones = requests.get(config.url_licitaciones)

    lic = {}

    for i in range(5):
        url = config.url_porCodigo(licitaciones.json()['Listado'][i]['CodigoExterno'])
        licitacion = requests.get(url).json()['Listado'][1]

        message= {
            'id': i,
            'status': "pre-processed",
            'createdAt': datetime.now().strftime('%Y-%m-%d'),
            'payload':{
                'codigo':licitacion['CodigoExterno'],
                'title': licitacion['Nombre'],
                'description': licitacion['Descripcion']
            }
        }

        send(json.dumps(message))

if __name__ == "__main__":
    main() 