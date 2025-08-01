
import os

host = os.getenv('REDIS_HOST', 'localhost')
port = int(os.getenv('REDIS_PORT', '6379'))

channel = 'messages'

token = os.getenv('API_KEY_MERCADO_PUBLICO', 'test_token')
url_tenders = f"https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json?fecha=28072025&ticket={token}&estado=activas"

def url_by_code(code):
    return f"https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json?codigo={code}&ticket={token}"

