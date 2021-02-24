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
        {"$sort": {"reported": 1} }
    ]
    return pipeline

def per_week(niveau, naam, dat_van, dat_tot):
    match, groep = {}, {}
    # match["provincie"] = naam
    # if niveau == "G":
        # match["gem_naam"] = naam
    
    groep["_id"]       = {"$isoWeek": "$publicatie"}
    groep["reported"]  = {"$sum"    : "$tot_reported"}
    groep["opnames"]   = {"$sum"    : "$opnames"}
    groep["overleden"] = {"$sum"    : "$overleden"}

    pipeline = [
        {"$match": 
            {
                "gem_naam" : naam, 
                "publicatie": { "$gte": dat_van, "$lte": dat_tot }
            }
        }, 
        {"$group": groep
            # {
                # "_id"      : {"$isoWeek": "$publicatie"},
                # "_id"      : {"$toDate"    : "$publicatie"},
                # "reported" : {"$sum"    : "$tot_reported"},
                # "opnames"  : {"$sum"    : "$opnames"},
                # "overleden": {"$sum"    : "$overleden"}
            # }  
        }, 
        {"$sort": {"_id": 1}}
    ]

    print(f"PIPELINE: {pipeline}")
    return pipeline
