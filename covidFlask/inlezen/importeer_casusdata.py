from datetime    import datetime
from collections import defaultdict
from flask       import current_app as app
import csv

from ..db import covid_casus

'''
CSV formaat:
    Date_file;
    Date_statistics;
    Date_statistics_type;
    Agegroup;
    Sex;
    Province;
    Hospital_admission;
    Deceased;
    Week_of_death;
    Municipal_health_service

    Date_statistics_type: Soort datum die beschikbaar was voor datum voor de variabele "Datum voor statistiek", waarbij:
    DOO = Date of disease onset : Eerste ziektedag zoals gemeld door GGD. Let op: het is niet altijd bekend of deze eerste ziektedag ook 
          echt al Covid-19 betrof.
    DPL = Date of first Positive Labresult : Datum van de (eerste) positieve labuitslag. 
    DON = Date of Notification : Datum waarop de melding bij de GGD is binnengekomen.

    Agegroup: Leeftijdsgroep bij leven; 0-9, 10-19, ..., 90+; bij overlijden <50, 50-59, 60-69, 70-79, 80-89, 90+, Unknown = Onbekend
'''
lg = {"0-9": 9, "10-19": 19, "20-29": 29, "30-39": 39, "40-49": 49, "50-59": 59, "60-69": 69, "70-79": 79, "80-89": 89, "90+": 999}

def verwerk_casusdata(csv_file, last_date, dry_run):
    print(f"PARAMETERS: {csv_file, last_date, dry_run}")
    totalen     = defaultdict(int)
    tot_prov    = defaultdict(lambda:defaultdict(int))
    # last_date   = datetime.strptime(last_date, "%Y-%m-%d")
    last_date   = datetime.strptime("2021-03-21", "%Y-%m-%d")
    max_date    = last_date
    fout        = False
    csv_to_save = app.root_path + app.config["UPLOAD_FOLDER"] + csv_file
    print(f"CSV_SAVE: {csv_to_save}")

    with open(csv_to_save, "r") as txt_file:
        regels = csv.DictReader(txt_file, delimiter=";")

        for regel in regels:
            
            rep_date = datetime.strptime(regel["Date_file"], "%Y-%m-%d %H:%M:%S")
            pub_date = datetime.strptime(regel["Date_statistics"], "%Y-%m-%d")
    
            if pub_date > last_date:          # Alleen records verwerken met een stat_dat > laatste verwerkingsdatum
                
                if not dry_run:
                    # print(f"VOOR HET ECHIE....")
                    covid_casus.insert_one(
                        { "datum"        : rep_date,
                          "publicatie"   : pub_date,
                          "stat_type"    : regel["Date_statistics_type"],
                          "leeftijd_grp" : regel["Agegroup"],
                          "geslacht"     : regel["Sex"],
                          "provincie"    : regel["Province"],
                          "ziekenhuis"   : regel["Hospital_admission"],
                          "overleden"    : regel["Deceased"],
                          "week_van_overlijden" : regel["Week_of_death"],
                          "gem_service"  : regel["Municipal_health_service"],
                        }
                    )

                # print(f"REGEL: {regel}")
                max_date                      = pub_date
                totalen[ "verwerkt" ]        += 1
                # tot_prov["Province"]         += 1
                tot_prov[ regel["Agegroup"] ][ regel["Province"] ] += 1
                
                totalen[ regel["Agegroup"] ] += 1
                totalen[ regel["Province"] ] += 1
                totalen[ "Z"+regel["Hospital_admission"] ] += 1
                totalen[ "D"+regel["Deceased"] ] += 1

    return tot_prov, totalen, max_date, fout
