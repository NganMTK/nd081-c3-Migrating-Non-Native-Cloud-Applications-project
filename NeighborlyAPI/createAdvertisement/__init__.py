import azure.functions as func
import pymongo
# NganMTK
import os
# basedir = os.path.abspath(os.path.dirname(__file__))

def main(req: func.HttpRequest) -> func.HttpResponse:

    request = req.get_json()

    if request:
        try:
            # NganMTK
            url = os.environ["CosmosDBConnectionString"]  # TODO: Update with appropriate MongoDB connection information
            client = pymongo.MongoClient(url)
            database = client['CosmosDBProject2']
            collection = database['advertisements']

            rec_id1 = collection.insert_one(eval(request))

            return func.HttpResponse(req.get_body())

        except ValueError:
            print("could not connect to mongodb")
            return func.HttpResponse('Could not connect to mongodb', status_code=500)

    else:
        return func.HttpResponse(
            "Please pass name in the body",
            status_code=400
        )