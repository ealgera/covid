from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from flask import current_app as app

client  = MongoClient("mongodb://192.168.10.203:27017")
de_data = app.config["DE_DATA"]
# print(f"FROM DB.PY; DE_DATA={de_data}")

db = client[de_data]

covid_col    = db["covidcol"]
gemeente_col = db["gemeentes"]

def alle_rekeningen():
    pass
    # return rekeningen_col.find({})

def eerste_laatste_dat():
    pipeline = [ 
        {"$group": 
            {
                "_id"       : "null",
                "datumMin"  : {"$min": "$publicatie"},
                "datumMax"  : {"$max": "$publicatie"}
            }
        }
    ]

    datums = list(covid_col.aggregate(pipeline))
    # print(f"DATUMS: {datums}")
    return datums[0]['datumMin'].strftime('%Y-%m-%d'), datums[0]['datumMax'].strftime('%Y-%m-%d')  # String output

def totaal_gerapporteerd():
    pipeline = [ 
        {"$group": 
            {
            "_id"       : "null",
            "aantal_rap": {"$sum": "$tot_reported"}
            }
        }
    ]

    totaal = covid_col.aggregate(pipeline)
    return list(totaal)[0]["aantal_rap"]

def tot_per_datum(van, tot):
    pipeline = [
        {"$match": {"publicatie": { "$gte": van, "$lte": tot} }
        },
        {"$group": { 
            "_id"      : "null",
            "reported" : { "$sum": "$tot_reported" },
            "opnames"  : { "$sum": "$opnames" },
            "overleden": { "$sum": "$overleden" }
            } 
        },
    ]

    totaal = covid_col.aggregate(pipeline)
    return list(totaal)