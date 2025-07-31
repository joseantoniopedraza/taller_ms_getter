
host = 'localhost'
port = 6379

canal = 'canal'

token   = "9DA9DC04-8AD4-4D65-AF30-3683E6194905"
url_licitaciones = f"https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json?fecha=28072025&ticket={token}&estado=activas"

def url_porCodigo(codigo):
    return f"https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json?codigo={codigo}&ticket={token}"

