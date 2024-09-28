import logging
import azure.functions as func
import pymongo
import json
from bson.json_util import dumps
# NganMTK
import os
# basedir = os.path.abspath(os.path.dirname(__file__))

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python getPosts trigger function processed a request.')

    try:
        # NganMTK
        url = os.environ["CosmosDBConnectionString"]  # TODO: Update with appropriate MongoDB connection information
        client = pymongo.MongoClient(url)
        database = client['CosmosDBProject2']
        collection = database['posts']

        result = collection.find({})
        result = dumps(result)

        return func.HttpResponse(result, mimetype="application/json", charset='utf-8', status_code=200)
    except:
        return func.HttpResponse("Bad request.", status_code=400)