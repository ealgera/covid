from datetime    import datetime
from collections import defaultdict
from flask       import current_app as app
import csv

from ..db import covid_test

'''
CSV formaat:
    Version;
    Date_of_report;
    Date_of_statistics;
    Security_region_code;
    Security_region_name;
    Tested_with_result;
    Tested_positive;
'''

def verwerk_testdata(csv_file, last_date, dry_run):
    totalen     = defaultdict(int)
    last_date   = datetime.strptime(last_date, "%Y-%m-%d")
    max_date    = last_date
    fout        = False
    csv_to_save = app.root_path + app.config["UPLOAD_FOLDER"] + csv_file

    with open(csv_to_save, "r") as txt_file:
        regels = csv.DictReader(txt_file, delimiter=";")

        for regel in regels:
            
            if regel["Version"] != "1":         # Deze versie wordt verwerkt
                fout = True
                return totalen, max_date, fout
                
            rep_date = datetime.strptime(regel["Date_of_report"], "%Y-%m-%d %H:%M:%S")
            pub_date = datetime.strptime(regel["Date_of_statistics"], "%Y-%m-%d")
    
            if pub_date > last_date:          # Alleen records verwerken met een stat_dat > laatste verwerkingsdatum
                
                if not dry_run:
                    print(f"VOOR HET ECHIE....")
                    covid_test.insert_one(
                        { "datum"        : rep_date,
                          "publicatie"   : pub_date,
                          "sec_reg_code" : regel["Security_region_code"],
                          "sec_reg_naam" : regel["Security_region_name"],
                          "test_tot"     : int(regel["Tested_with_result"]),
                          "test_pos"     : int(regel["Tested_positive"])
                        }
                    )

                max_date             = pub_date
                totalen["verwerkt"] += 1
                totalen["getest"]   += int(regel["Tested_with_result"])
                totalen["positief"] += int(regel["Tested_positive"])

    return totalen, max_date, fout
