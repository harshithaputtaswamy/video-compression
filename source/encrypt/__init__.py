import logging

import azure.functions as func
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import hashlib
import asyncio
import aiohttp

from cryptography.fernet import Fernet

encryption_key = b'2abIJIe2xU91osdOME9H27O8HBIk20lYNoCOR0iIqik='

async def send_request(encrypted_data,fname):
    url = 'http://localhost:7071/api/save'
    async with aiohttp.ClientSession() as session:
        file = {'encrypted_data': encrypted_data}
        async with session.post(url, data=file,params={'fname':fname}) as response:
            logging.info(response.text())
            return




def encrypt(byte_stream):
    fernet = Fernet(encryption_key)
    return fernet.encrypt(byte_stream)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key=encryption_key, mode= AES.MODE_CFB,iv= iv)
    return base64.b64encode(cipher.encrypt(byte_stream)).decode()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    print(req)
    logging.info(dir(req))
    try:
        logging.info(f"files are {req.params}")
        file= req.files['upload_file']
        fname = req.params['fname']
        data = file.stream.read()
        print("OIUASFCGYA",len(data))
        if data == None:
            raise ValueError("data not present in bocy")
    except ValueError as e :
        logging.error(e)
        return func.HttpResponse(
             "Bad request format",
             status_code=400
        )
    encrypted_data = encrypt(data)

    asyncio.run(send_request(encrypted_data,fname))

    return func.HttpResponse(
             f"Data is  \n  ",
             status_code=200
        )
