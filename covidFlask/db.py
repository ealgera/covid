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
covid_test   = db["testen"]
covid_casus  = db["covidcasus"]

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

def per_regio(regio, dat_van, dat_tot):
    # Aggregatie pipeline voor sommatie van getallen per provincie en gemeente (binnen de provincie)
    pipeline = [
        {"$match": {
            "sec_reg_naam" : regio, # Een enkele Regio of een List van Regio's icm $in
            "publicatie"   : { "$gte": dat_van, "$lte": dat_tot} }
        },
        {"$group": { 
            "_id"      : "$sec_reg_naam",    # Per Regio
            "getest"   : { "$sum": "$test_tot" },
            "positief" : { "$sum": "$test_pos" },
            } 
        },
        {"$sort": {"_id": 1} }
    ]

    return pipeline

def casus_per_provincie(provincie, dat_van, dat_tot):
    # Aggregatie pipeline voor sommatie van getallen per leeftijdsgroep en per provincie
    pipeline = [ 
        {"$match": {
            "provincie" : provincie,                             # Een enkele Provincie of een List van Provincies icm $in
            "publicatie": { "$gte": dat_van, "$lte": dat_tot} }
        },
        {"$group": 
            {
            # "_id"   : {"groep": "$leeftijd_grp", "prov": "$provincie"},
            "_id"   : {"prov": "$provincie", "groep": "$leeftijd_grp"},
            "aantal": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1} }
    ]

    return pipeline