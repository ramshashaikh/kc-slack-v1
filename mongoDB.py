import pymongo
import numpy as np
from bson import ObjectId


def create_record(phone, name, image_url):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["user_queries"]

        user_data = {"userID": phone, "name": name, "sent_image": ""}
        updated_status = {
            "$push": {"image_url": image_url, "stored_image": image_url}}

        result = collection.update_one(user_data, updated_status, upsert=True)

        if result.upserted_id:
            print("New record created.")

        else:
            print("Record updated.")
        return "Success"

    except Exception as e:
        print("create_record error", e)


def find_user(senderID):
    try:

        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["user_queries"]

        query = {"userID": senderID}

        print("query ", collection.find_one(query))
        return collection.find_one(query)

    except Exception as e:
        print("find_user error", e)


def retrieve_field(userID, field_name):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["user_queries"]
        doc = collection.find_one({'userID': userID})
        # collection.create_index("Solution")

        if doc:
            field = doc.get(field_name)
            return field

        else:
            query = "No document found."
            return query
            print("No document found.")
    except Exception as e:
        print("find  error", e)


def update_field_set(phone, filed_name, field_value):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["user_queries"]

        user_data = {"userID": phone}
        updated_status = {"$set": {filed_name: field_value}}

        collection.update_one(user_data, updated_status, upsert=True)
        print("update_field_set ", collection.update_one(
            user_data, updated_status, upsert=True))
        return 200
        # print("update_chat_status ", r)
    except Exception as e:
        print("update set", e)

# * -----------------AGRONOMIST TABLE -----------------


def retrieve_agro_field(agro_name, field_name):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["agronomist"]
        doc = collection.find_one({'agro_name': agro_name})
        # collection.create_index("Solution")

        if doc:
            field = doc.get(field_name)
            return field

        else:
            query = "No document found."
            return query
            print("No document found.")
    except Exception as e:
        print("find  error", e)

        # collection.create_index("Solution")

        # if result:
        #     field = doc.get(field_name)
        #     return field

        # else:
        #     query = "No document found."
        #     return query


def update_push_agro(agroID, field_name, field_value):
    client = pymongo.MongoClient(
        "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
    db = client["Slack_forum"]
    collection = db["agronomist"]

    user_data = {"agro_id": agroID}
    chat_log = {
        "$push": {field_name:
                  {"$each": [field_value]}
                  }
    }

    result = collection.update_one(user_data, chat_log, upsert=True)
    print("update_image_field ", result)


def update_pull_agro(agroID, array_name, array_value):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["agronomist"]

        user_data = {"agro_id": agroID}
        agro_update = {
            "$pull": {array_name: {"solution_text": array_value}}
        }

        result = collection.update_one(user_data, agro_update, upsert=True)
        print("update_pull_agro ", result)
        return result
    except Exception as e:
        print("update_pull_agro error", e)
        return None


# **----------QUERIES TABLE -----------------


def create_query_record(query_id, farmer_phoneNo, query_text, posted_ts):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["queries"]

        query_data = {"query_id": query_id}
        query_update = {"$set":
                        {"query_text": query_text, "query_by": farmer_phoneNo, "posted_ts": posted_ts, "status": "Pending",
                            "Approved_solution": "", "Solution_by": "", "Moderated_by": "", "Moderated_ts": ""}
                        # "$push": {"rejected_solutions": []}
                        }
        # updated_status = {
        #     "$push": {"image_url": image_url, "stored_image": image_url}}

        result = collection.update_one(query_data, query_update, upsert=True)

        print("Query record result ", result.upserted_id)
        if result.upserted_id:
            print("New record created.")

        else:
            print("Record updated.")
        return "Success"

    except Exception as e:
        print("create_record error", e)


def retrieve_query_field(query_text, field_name):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["queries"]
        doc = collection.find_one({'query_text': query_text})
        # print("doc ", doc)
        # collection.create_index("Solution")

        if doc:
            field = doc.get(field_name)
            return field

        else:
            query = "No document found."
            return query
            print("No document found.")
    except Exception as e:
        print("find  error", e)


def update_set_queries(query_id, solution_text, agro_name, moderator_name, action_ts):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["queries"]

        user_data = {"query_id": query_id}
        updated_status = {
            "$set": {"Approved_solution": solution_text, "Solution_by": agro_name, "Moderated_by": moderator_name, "Moderated_ts": action_ts}}

        collection.update_one(user_data, updated_status, upsert=True)
        print("update_field_set ", collection.update_one(
            user_data, updated_status, upsert=True))
        return 200
        # print("update_chat_status ", r)
    except Exception as e:
        print("update set", e)


def update_push_query(query_id, field_name, field_value):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["queries"]

        query_data = {"query_id": query_id}
        # chat_log = {
        #     "$push": {field_name:
        #               {"$each": [field_value]}
        #               }
        # }
        query_update = {
            "$push": {field_name:
                      {"$each": [field_value]}
                      }
        }

        result = collection.update_one(query_data, query_update, upsert=True)
        return result
    except Exception as e:
        print("update_push_query error", e)
        return None


def update_pull_query(query_id, array_name, array_value):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["queries"]

        query_data = {"query_id": query_id}
        query_update = {
            "$pull": {array_name: {"solution_text": array_value}}
        }

        result = collection.update_one(query_data, query_update, upsert=True)
        print("update_pull_agro ", result)
        return result
    except Exception as e:
        print("update_pull_query error", e)
        return None


# update_pull_agro("KC_01")

# * -----------------TRACK LATEST ID -----------------


def get_next_id():
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
        db = client["Slack_forum"]
        collection = db["query_id_track"]

        counter_doc = collection.find_one_and_update(
            {"_id": "counter"},
            {"$inc": {"last_query_id": 1}},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER
        )

        new_id = f"KC_{counter_doc['last_query_id']}"
        return new_id
    except Exception as e:
        print("track id error", e)


# Example usage


# def update_image_url_overwrite(userID, image_url):
#     client = pymongo.MongoClient(
#         "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
#     db = client["Slack_forum"]
#     collection = db["user_queries"]

#     user_data = {"userID": userID}
#     chat_log = {
#         "$set": {"image_url": image_url}}

#     result = collection.update_one(user_data, chat_log, upsert=True)
#     print("update_image_url ", result)


# def update_chat_status(phone, status):
#     try:
#         client = pymongo.MongoClient(
#             "mongodb+srv://ramshasvef:UFWBrBFu813uS5Zm@smartu.q3rms0e.mongodb.net/test")
#         db = client["Slack_forum"]
#         collection = db["user_queries"]

#         user_data = {"userID": phone}
#         updated_status = {"$set": {"status": status}}

#         collection.update_one(user_data, updated_status, upsert=True)
#         # print("update_chat_status ", r)
#     except Exception as e:
#         print("update_chat_status error", e)
