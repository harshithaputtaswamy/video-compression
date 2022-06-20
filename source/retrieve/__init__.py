import logging

import azure.functions as func
from azure.storage.blob import BlobServiceClient
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import random
import hashlib

from cryptography.fernet import Fernet


encryption_key = hashlib.sha256(b'Randomsecretkeyforprototype').digest()
connect_str = "DefaultEndpointsProtocol=https;AccountName=sbivideocompressor;AccountKey=6kwas2q/CgeMBb05D1LYs5wUlGJby+5Va/291rqa5Y8faIlXAZusnAxoi7KuVt6mZelZvHgCwxDi+AStDbPseg==;EndpointSuffix=core.windows.net"
container_name = "output-videos"

def decrypt(cypher):
    fernet = Fernet(encryption_key)
    return fernet.decrypt(cypher)
    iv = cypher[:AES.block_size]
    cipher = AES.new(encryption_key, AES.MODE_CFB, iv)
    return cipher.decrypt(cypher[AES.block_size:])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        file_name = req.params.get('fname')
        if not file_name:
            raise ValueError
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_container_client(container = container_name)
        cipher_data = blob_client.download_blob(file_name).readall()
        video_file = decrypt(cipher_data)

        return func.HttpResponse(
            video_file,
            mimetype="application/octet-stream"
        )
    except ValueError as e:
        logging.error(e)
        return func.HttpResponse(
            "Filename error",
            status_code=400
        )
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(
            "File error",
            status_code=400
        )