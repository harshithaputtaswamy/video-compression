from email import header
import logging
from Katna.video import Video
import azure.functions as func
import timeit
import os
import asyncio
import aiohttp

compression_factor = 20 #should be set from 1-50

async def send_request(fname):
    url = 'http://localhost:7071/api/encrypt'
    with open('c_'+fname.split('.')[0]+".mp4",'rb') as f:
        async with aiohttp.ClientSession() as session:
            file = {'upload_file': f}
            async with session.post(url, data=file, params={'fname':fname}) as response:
                logging.info(response.text())
                return

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes\n"
                 f"funcs {dir(myblob)}\n")
    START = timeit.default_timer()

    content = myblob.read()
    fname = myblob.name.split('/')[-1]
    file = open(fname, 'wb+')
    vd = Video()
    file.write(content)
    file.close()
    vd.compress_video(file_path=fname, crf_parameter=compression_factor,out_file_name='c_'+fname.split('.')[0])
    end = timeit.default_timer()
    print("time:",end-START)

    
    url = "http://localhost:7071/api/encrypt"
    #headers = {'Content-Type': 'application/octet-stream'}
    #headers=headers
    '''
    file = open('c_'+fname.split('.')[0]+".mp4",'rb')
    try:
        files = {'upload_file': file}
        response = requests.post(url, files=files)
        print(response.status_code)
        print(response.json())
    except Exception as e:
        print(e)
    file.close()
    '''
    asyncio.run(send_request(fname.split('.')[0]+".mp4"))

    os.remove(fname)
    os.remove('c_'+fname.split('.')[0]+".mp4")

    #.logging.info(f"Content of the blob is {content}")








