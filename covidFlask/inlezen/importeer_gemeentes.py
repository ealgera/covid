from datetime    import datetime
from collections import defaultdict
from flask       import current_app as app
import csv
import time
import pandas as pd

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

def verwerk_gemeentes(csv_file, last_date, dry_run): # Input: CSV-bestand, laatste verwerkingsdatum, wel of niet oefenen
    totalen     = defaultdict(int)
    provincies  = []
    gemeentes   = []

    start_time  = time.time()
    print(f"FILTER CSV...")

    last_date   = datetime.strptime(last_date, "%Y-%m-%d")
    max_date    = last_date
    csv_to_save = app.root_path + app.config["UPLOAD_FOLDER"] + csv_file

    with open(csv_to_save, "r") as txt_file:
        regels = csv.DictReader(txt_file, delimiter=";")

        for regel in regels:
            
            rep_date = datetime.strptime(regel["Date_of_report"], "%Y-%m-%d %H:%M:%S")  # Rapportdatum
            pub_date = datetime.strptime(regel["Date_of_publication"], "%Y-%m-%d")      # Datum waarop de covid-data is vastgesteld
    
            if pub_date > last_date:                             # Deze regel nog niet verwerkt?
                
                if pub_date > max_date:                          # Bepaal de 'laatste' datum in het CSV-bestand
                    max_date = pub_date
                if regel["Province"] not in provincies:          # Bewaar verwerkte provincies
                    provincies.append(regel["Province"])
                if regel["Municipality_name"] not in gemeentes:  # Bewaar verwerkte gemeentes
                    gemeentes.append(regel["Municipality_name"])

                if not dry_run:                                  # Niet oefenen? Dan voor het echie...
                    covid_col.insert_one(                        # Voeg dan een nieuw COVID-record toe
                        { "datum"       : rep_date,
                          "publicatie"  : pub_date,
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

    print(f"VERWERKEN CSV: {time.time()-start_time}")

    return totalen, max_date                     # Geef de totalen en de laatste verwerkingsdatum terug.

def verwerk_gemeentes_via_pandas(csv_file, last_date, dry_run): # Input: CSV-bestand, laatste verwerkingsdatum, wel of niet oefenen
    totalen     = defaultdict(int)
    provincies  = []
    gemeentes   = []
    start_time  = time.time()

    # print(f"FILTER CSV... {last_date}")
    csv_to_save = app.root_path + app.config["UPLOAD_FOLDER"] + csv_file
    csv_df = pd.read_csv(csv_to_save, delimiter=";")
    filter = csv_df["Date_of_publication"] > last_date
    csv_now = csv_df[filter]
    print(f"GEFILTERED: {csv_now}")
    # print(f"FILTER CSV: {time.time()-start_time}")

    last_date = datetime.strptime(last_date, "%Y-%m-%d")
    max_date  = last_date

    for index, regel in csv_now.iterrows():

        rep_date = datetime.strptime(regel["Date_of_report"], "%Y-%m-%d %H:%M:%S")  # Rapportdatum
        pub_date = datetime.strptime(regel["Date_of_publication"], "%Y-%m-%d")      # Datum waarop de covid-data is vastgesteld

        if pub_date > max_date:                          # Bepaal de 'laatste' datum in het CSV-bestand
            max_date = pub_date
        if regel["Province"] not in provincies:          # Bewaar verwerkte provincies
            provincies.append(regel["Province"])
        if regel["Municipality_name"] not in gemeentes:  # Bewaar verwerkte gemeentes
            gemeentes.append(regel["Municipality_name"])

        if not dry_run:                                  # Niet oefenen? Dan voor het echie...
            covid_col.insert_one(                        # Voeg dan een nieuw COVID-record toe
                { "datum"       : rep_date,
                    "publicatie"  : pub_date,
                    "gem_code"    : regel["Municipality_code"] if not pd.isna(regel['Municipality_code']) else "", 
                    "gem_naam"    : regel["Municipality_name"] if not pd.isna(regel["Municipality_name"]) else "",
                    "provincie"   : regel["Province"],
                    "sec_reg_code": regel["Security_region_code"],
                    "sec_reg_naam": regel["Security_region_name"],
                    "gem_service" : regel["Municipal_health_service"],
                    "roaz_reg"    : regel["ROAZ_region"] if not pd.isna(regel["ROAZ_region"]) else "",
                    "tot_reported": int(regel["Total_reported"]),
                    "opnames"     : int(regel["Hospital_admission"]),
                    "overleden"   : int(regel["Deceased"])
                }
            )
            # print(test)
            # print()

        totalen["verwerkt"] += 1
        totalen["gerapporteerd"] += int(regel["Total_reported"])
        totalen["opnames"]   += int(regel["Hospital_admission"])
        totalen["overleden"] += int(regel["Deceased"])

    totalen["gemeentes"]  = len(gemeentes)
    totalen["provincies"] = len(provincies)

    print(f"\nVERWERKEN CSV: {time.time()-start_time}")
    print(f"VERWERKT     : {totalen['verwerkt']}")
 
    return totalen, max_date                     # Geef de totalen en de laatste verwerkingsdatum terug.
