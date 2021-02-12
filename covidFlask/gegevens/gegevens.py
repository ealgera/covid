from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for #, request, redirect, url_for, flash #, session
# from flask import current_app as app
from datetime import datetime

from covidFlask.db import gemeente_col, covid_col
from .forms import GegevensForm
# from covidFlask import db

gegevens_bp = Blueprint("gegevens_bp", __name__, 
    template_folder= "templates",
    static_folder  = "static")

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


@gegevens_bp.route("/gegevens-gemeentes", methods=["GET", "POST"])
def gegevens_gemeentes():

    locatie_getallen = []
    prov_filter      = {}
    form = GegevensForm()
    alle_provincies       = gemeente_col.distinct("provincie")
    alle_provincies.insert(0, "Alles")
    form.prov_sel.choices = alle_provincies

    if form.validate_on_submit():
        print("\nGAVALIDEERD!")
        # print(f"FORM - POST: {form.data}")

        niveau = "$provincie"
        if form.gemniveau.data:
            niveau = "$gem_naam"

        if form.dat_tm.data > datetime.date(datetime.now()):
            flash("Datum mag niet in de toekomst liggen!", category="error")
            redirect( url_for("gegevens_bp.gegevens_gemeentes") )
        
        else:
            dat_van = datetime.combine(form.dat_vanaf.data, datetime.min.time()) # Date naar DateTime conversie
            dat_tot = datetime.combine(form.dat_tm.data, datetime.min.time()) # Date naar DateTime conversie
            if form.prov_sel.data == "Alles":
                prov_filter["$in"] = alle_provincies # List met alle Provincies
                filter = per_prov_gem(prov_filter, dat_van, dat_tot, niveau)
            else:
                filter = per_prov_gem(form.prov_sel.data, dat_van, dat_tot, niveau)
            
            locatie_getallen = covid_col.aggregate(filter)

            # for item in locatie_getallen:
                # print(f"ITEM: {item}")

    # else:
#         print(f"ERRORS: {form.errors}")

    # GET
    form.dat_vanaf.data = datetime.date(datetime.strptime("2021-01-01", "%Y-%m-%d"))
    form.dat_tm.data    = datetime.date(datetime.now())
    # print(f"\n\nFORM - GET : {form.data}")

    return render_template("/gegevens.html", form=form, locatie_getallen=locatie_getallen)


@gegevens_bp.route("/gegevens-casuslandelijk", methods=["GET", "POST"])
def gegevens_casuslandelijk():
    pass
