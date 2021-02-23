def per_prov_gem(provincie, dat_van, dat_tot, niveau):
    # Aggregatie pipeline voor sommatie van getallen per provincie en gemeente (binnen de provincie)
    pipeline = [
        {"$match": {
            "provincie" : provincie, # Een enkele Provincie of een List van Provincies icm $in
            "publicatie": { "$gte": dat_van, "$lte": dat_tot} }
        },
        {"$group": { 
            "_id"      : niveau,     # Per provincie of per Gemeente
            "reported" : { "$sum": "$tot_reported" },
            "opnames"  : { "$sum": "$opnames" },
            "overleden": { "$sum": "$overleden" }
            } 
        },
        # {"$addFields": 
            # { "totalRep": { "$sum": "$reported" } }
        # },
        {"$sort": {"reported": 1} }
    ]
    return pipeline

def per_week(gemeente: str, datum):
    
    # pipeline = [
    #     {"$match": {
    #         "gem_naam"   : gemeente,
    #          "publicatie": {"$lte": datum} }
    #     },
    #     {"$group": { 
    #         "_id"      : { "$isoWeek": "$publicatie" }, 
    #         "reported" : { "$sum"    : "$tot_reported" },
    #         "opnames"  : { "$sum"    : "$opnames" },
    #         "overleden": { "$sum"    : "$overleden" }
    #         } 
    #     },
    #     {"$sort": {"_id": 1}}
    # ]

    pipeline = [
        {"$match": 
            {"gem_naam"  : gemeente, 
            "publicatie": {"$lte": datum}
            }
        }, 
        {"$group": 
            {
                "_id"      : {"$isoWeek": "$publicatie"},
                # "_id"      : {"$toDate"    : "$publicatie"},
                "reported" : {"$sum"    : "$tot_reported"},
                "opnames"  : {"$sum"    : "$opnames"},
                "overleden": {"$sum"    : "$overleden"}
            }  
        }, 
        {"$sort": {"_id": 1}}
    ]

    return pipeline
