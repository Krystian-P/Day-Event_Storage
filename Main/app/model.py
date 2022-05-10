import pymongo as pm

from bson.json_util import loads, dumps, SON
import config


# DB Model
class dataBase(object):
    CONNECTION_STRING = config.Config.MONGO_URI
    DATABASE = None
    COLLECTION = None


    #Init connection
    @staticmethod
    def initialize():
        client = pm.MongoClient(dataBase.CONNECTION_STRING)
        dataBase.DATABASE = client['NetguruRecruitmentTask']
        dataBase.COLLECTION = dataBase.DATABASE["Events"]

    # Add document to db
    @staticmethod
    def insert(jsonData):
        file = dataBase.COLLECTION.insert_one(jsonData)
        fileId = file.inserted_id
        return fileId

    # Find document by id
    @staticmethod
    def findDate(jsonData):
        fileId = dataBase.insert(jsonData)
        cursor = dataBase.COLLECTION.find({'_id': fileId})
        return loads(dumps(cursor))

    # Delete document by id
    @staticmethod
    def delete(fileId):
        result = dataBase.COLLECTION.delete_one({"_id": fileId})
        # print("API call recieved:", result.acknowledged)
        # print("Documents deleted:", result.deleted_count)
        return result.deleted_count

    # Return all documents from collection
    @staticmethod
    def fetchAll(dateList):
        cursor = dataBase.COLLECTION.find({})
        for docs in cursor:
            dateList.append(docs)
        return dateList

    # Group and sort by popularity in collection
    @staticmethod
    def aggregateByMonth():
        pipline = [
            {"$unwind": "$month"},
            {"$group": {"_id": "$month", "days_checked": {"$sum": 1}}},
            {"$sort": SON([("days_checked", -1), ("month", -1)])}
        ]
        return list(dataBase.COLLECTION.aggregate(pipline))

    # Count all document current in collection
    @staticmethod
    def countDocs():
        total_count = dataBase.COLLECTION.find_one({"$query": {}, "$orderby": {"_id": -1}})
        if total_count is None:
            return 1
        else:
            return total_count["_id"] + 1

