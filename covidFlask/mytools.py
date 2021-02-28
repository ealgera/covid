from   .db    import covid_col, covid_test
from   flask  import Blueprint
from   flask  import current_app as app
import requests

mytools = Blueprint("mytools", __name__)

def laatste_datum(collection="covid_col"):
    pipeline = [ 
        {"$group": 
            {
                "_id"       : "null",
                "datumMin"  : {"$min": "$publicatie"},
                "datumMax"  : {"$max": "$publicatie"}
            }
        }
    ]

    if collection == "covid_col":
        datums = list(covid_col.aggregate(pipeline))
    elif collection == "covid_test":
        datums = list(covid_test.aggregate(pipeline))

    if datums:
        return datums[0]['datumMax'].strftime('%Y-%m-%d')  # String output
    else:
        return "2020-01-01"

def haal_csv(csv_file):
    meldingen = []
    fout      = False

    csv_to_save = app.root_path + app.config["UPLOAD_FOLDER"] + csv_file
    url         = app.config["RIVM_URL"] + csv_file

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
