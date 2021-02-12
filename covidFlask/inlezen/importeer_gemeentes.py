from datetime    import datetime
from collections import defaultdict
from flask       import current_app as app
import requests
import csv

from ..db import covid_col

# hit_datum   = datetime.strptime("19000101", "%Y%m%d")
csv_file    = "COVID-19_aantallen_gemeente_per_dag.csv"
csv_to_save = app.root_path + app.config["UPLOAD_FOLDER"] + csv_file
url         = "https://data.rivm.nl/covid-19/" + csv_file

'''
CSV formaat:
    Date_of_report;
    Date_of_publication;
    Municipality_code;
    Municipality_name;
    Province;
    Security_region_code;
    Security_region_name;
    Municipal_health_service;
    ROAZ_region;
    Total_reported;
    Hospital_admission;
    Deceased
'''

def laatste_datum():
    pipeline = [ 
        {"$group": 
            {
                "_id"       : "null",
                "datumMin"  : {"$min": "$publicatie"},
                "datumMax"  : {"$max": "$publicatie"}
            }
        }
    ]

    datums = covid_col.aggregate(pipeline)
    return list(datums)[0]['datumMax'].strftime('%Y-%m-%d')  # String output


def haal_csv():
    meldingen = []
    fout      = False
    print(f"[COVID] CSV Bestand wordt gehaald... ( {url} )")
    
    try:
        req = requests.get(url, allow_redirects=True)
    except Exception as e:
        fout = True
        print(f"[COVID] FOUT:")
        print(e)
    else:
        if req.headers['Content-Type'].split('/')[1] != "csv":
            fout = True
            meldingen.append("[COVID] CSV Bestand niet gevonden!!")
        else:
            meldingen.append("[COVID] CSV Bestand opgehaald...")

    # meldingen.append(f"[COVID] Status: {req.status_code}")

    with open(csv_to_save, 'wb') as f:
        f.write(req.content)
    
    return meldingen, fout


def verwerk_gemeentes(last_date, dry_run):
    totalen    = defaultdict(int)
    provincies = []
    gemeentes  = []
    last_date  = datetime.strptime(last_date, "%Y-%m-%d")
    max_date   = last_date

    with open(csv_to_save, "r") as txt_file:
        regels = csv.DictReader(txt_file, delimiter=";")

        for regel in regels:
            
            rep_date = datetime.strptime(regel["Date_of_report"], "%Y-%m-%d %H:%M:%S")
            pub_date = datetime.strptime(regel["Date_of_publication"], "%Y-%m-%d")
    
            if pub_date > last_date:
                
                if pub_date > max_date:
                    max_date = pub_date
                if regel["Province"] not in provincies:
                    provincies.append(regel["Province"])
                if regel["Municipality_name"] not in gemeentes:
                    gemeentes.append(regel["Municipality_name"])

                if not dry_run:
                    covid_col.insert_one(
                        { "datum"       : rep_date, #regel["Date_of_report"], 
                          "publicatie"  : pub_date, # regel["Date_of_publication"], 
                          "gem_code"    : regel["Municipality_code"], 
                          "gem_naam"    : regel["Municipality_name"],
                          "provincie"   : regel["Province"],
                          "sec_reg_code": regel["Security_region_code"],
                          "sec_reg_naam": regel["Security_region_name"],
                          "gem_service" : regel["Municipal_health_service"],
                          "roaz_reg"    : regel["ROAZ_region"],
                          "tot_reported": int(regel["Total_reported"]),
                          "opnames"     : int(regel["Hospital_admission"]),
                          "overleden"   : int(regel["Deceased"])
                        }
                    )

                totalen["verwerkt"] += 1
                totalen["gerapporteerd"] += int(regel["Total_reported"])
                totalen["opnames"]   += int(regel["Hospital_admission"])
                totalen["overleden"] += int(regel["Deceased"])

        totalen["gemeentes"]  = len(gemeentes)
        totalen["provincies"] = len(provincies)

    return totalen, max_date
