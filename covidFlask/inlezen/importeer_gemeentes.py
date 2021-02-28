from datetime    import datetime
from collections import defaultdict
from flask       import current_app as app
import csv

from ..db import covid_col

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

def verwerk_gemeentes(csv_file, last_date, dry_run):
    totalen     = defaultdict(int)
    provincies  = []
    gemeentes   = []
    last_date   = datetime.strptime(last_date, "%Y-%m-%d")
    max_date    = last_date
    csv_to_save = app.root_path + app.config["UPLOAD_FOLDER"] + csv_file

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
