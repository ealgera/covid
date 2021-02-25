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

def per_week(niveau, periode, naam, dat_van, dat_tot):
    match, groep = {}, {}
    
    if niveau == "G":
        match["gem_naam"] = naam
    else:
        match["provincie"] = naam
    match["publicatie"] = { "$gte": dat_van, "$lte": dat_tot }
    
    if periode == "D":
        groep["_id"] = {"$toDate" : "$publicatie"}
    elif periode == "W":
        groep["_id"] = {"$isoWeek": "$publicatie"}
    else:
        groep["_id"] = {"$month"  : "$publicatie"}
    
    groep["reported"]  = {"$sum"    : "$tot_reported"}
    groep["opnames"]   = {"$sum"    : "$opnames"}
    groep["overleden"] = {"$sum"    : "$overleden"}

    pipeline = [
        {"$match": match }, 
        {"$group": groep }, 
        {"$sort" : {"_id": 1}}
    ]

    # print(f"PIPELINE: {pipeline}")
    return pipeline
