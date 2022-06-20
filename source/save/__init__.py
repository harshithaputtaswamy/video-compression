import logging
from typing import Container

import azure.functions as func
from azure.storage.blob import BlobServiceClient

connect_str = "DefaultEndpointsProtocol=https;AccountName=sbivideocompressor;AccountKey=6kwas2q/CgeMBb05D1LYs5wUlGJby+5Va/291rqa5Y8faIlXAZusnAxoi7KuVt6mZelZvHgCwxDi+AStDbPseg==;EndpointSuffix=core.windows.net"
container_name = "output-videos"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        file= req.files['encrypted_data']
        data = file.stream.read()
        fname = req.params['fname']
        if data == None:
            raise ValueError("data not present in bocy")
    except ValueError as e:
        logging.error(e)
        return func.HttpResponse(
            "Bad request format",
            status_code=400
        )
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=fname)
    blob_client.upload_blob(data)
    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )
