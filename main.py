import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["medical_db"]
collection = db["hospitals"]

collection.drop()

file_path = "hospitals_mongodb.json"

with open(file_path, "r", encoding="utf-8") as file:
    file_data = json.load(file)
    if isinstance(file_data, list):
        collection.insert_many(file_data)
    else:
        collection.insert_one(file_data)

pipeline_1 = [
    { "$group": { "_id": None, "count": { "$sum": 1 } } }
]
for doc in collection.aggregate(pipeline_1):
    print(doc)

pipeline_2 = [
    { "$group": { "_id": None, "avg_covered": { "$avg": "$Average_Covered_Charges" } } }
]
for doc in collection.aggregate(pipeline_2):
    print(doc)

pipeline_3 = [
    { "$group": { "_id": "$Provider_ZIP_Code", "avg_covered_charges": { "$avg": "$Average_Covered_Charges" } } },
    { "$sort": { "avg_covered_charges": 1 } },
    { "$limit": 5 }
]
print("\n   Середнє по ZIP-кодах з сортуванням")
pipeline_3 = [
    { "$group": { "_id": "$Provider_ZIP_Code", "avg_covered_charges": { "$avg": "$Average_Covered_Charges" } } },
    { "$sort": { "avg_covered_charges": 1 } },
    { "$limit": 5 }
]
for doc in collection.aggregate(pipeline_3):
    print(doc)

print("\n    Фільтрація груп")
pipeline_4 = [
    { "$group": { "_id": "$Provider_ZIP_Code", "avg_covered_charges": { "$avg": "$Average_Covered_Charges" } } },
    { "$match": { "avg_covered_charges": { "$lt": 50000 } } },
    { "$sort": { "avg_covered_charges": 1 } },
    { "$limit": 5 }
]
for doc in collection.aggregate(pipeline_4):
    print(doc)

print("\n   Збереження в нову колекцію")
pipeline_5 = [
    { "$match": { "Average_Medicare_Payments": { "$lt": 50000 } } },
    { "$group": { "_id": "$Provider_ZIP_Code", "avg_covered_charges": { "$avg": "$Average_Covered_Charges" } } },
    { "$match": { "avg_covered_charges": { "$lt": 50000 } } },
    { "$sort": { "avg_covered_charges": 1 } },
    { "$out": "result_variant_2" }
]

list(collection.aggregate(pipeline_5))
print("Дані збережено в колекцію")

print("\nРезультати з нової колекції:")
for doc in db["result_variant_2"].find().limit(5):
    print(doc)