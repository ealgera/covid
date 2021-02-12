from flask import Blueprint, render_template
# from covidFlask.db import gemeente_col, covid_col
from .      import db
import datetime

algemeen = Blueprint("algemeen", __name__)

@algemeen.route("/")
def index():

    eerste_dat, laatste_dat = db.eerste_laatste_dat()   # String
    # print(f"EERSTE: {eerste_dat}, LAATSTE: {laatste_dat}")
    totaal_rap  = db.totaal_gerapporteerd()             # Integer
    
    # Rapportage laatste dag
    dat_tot    = datetime.datetime.strptime(laatste_dat, "%Y-%m-%d")
    dat_van    = dat_tot
    rap_laatste = db.tot_per_datum(dat_van, dat_tot)    # List met Dict: reported, opnames, overleden

    # dat_tot    = datetime.datetime.strptime(laatste_dat, "%Y-%m-%d")
    dat_van    = datetime.datetime.strptime(eerste_dat, "%Y-%m-%d")
    totaal_rap = db.tot_per_datum(dat_van, dat_tot)     # List met Dict: reported, opnames, overleden
    return render_template("index.html", rap_laatste=rap_laatste, eerste_dat=eerste_dat, laatste_dat=laatste_dat, totaal_rap=totaal_rap)
    