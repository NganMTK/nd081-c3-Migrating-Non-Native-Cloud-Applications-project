import azure.functions as func
import pymongo
import json
from bson.json_util import dumps
# NganMTK
import os
basedir = os.path.abspath(os.path.dirname(__file__))

def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        # NganMTK
        url = os.environ["CosmosDBConnectionString"]  # TODO: Update with appropriate MongoDB connection information
        client = pymongo.MongoClient(url)
        database = client['admin-prj2']
        collection = database['advertisements']


        result = collection.find({})
        result = dumps(result)

        return func.HttpResponse(result, mimetype="application/json", charset='utf-8')
    except:
        print("could not connect to mongodb")
        return func.HttpResponse("could not connect to mongodb",
                                 status_code=400)

