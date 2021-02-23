from flask    import Blueprint, render_template, flash, redirect, url_for #, request, redirect, url_for, flash #, session
from datetime import datetime

from covidFlask.db        import gemeente_col, covid_col
from .forms               import TotGrafiekForm, DatGrafiekForm
from covidFlask.pipelines import per_prov_gem, per_week

grafieken_bp = Blueprint("grafieken_bp", __name__, 
    template_folder= "templates",
    static_folder  = "static")


@grafieken_bp.route("/tot-grafieken", methods=["GET", "POST"])
def tot_grafieken():

    labels, values = [], []
    gevonden       = False
    # velden         = {}
    type           = "Provincie"
    legenda        = "Totalen per " + type
    
    locatie_getallen = []
    prov_filter      = {}
    form = TotGrafiekForm()
    alle_provincies       = gemeente_col.distinct("provincie")
    alle_provincies.insert(0, "Alles")
    form.prov_sel.choices = alle_provincies

    if form.validate_on_submit():
        # print("\nGEVALIDEERD!")
        # print(f"FORM - POST: {form.data}")
# 
        niveau   = "$provincie"
        if form.gemniveau.data:
            niveau  = "$gem_naam"
            type    = "Gemeente"
            legenda = "Totalen per " + type
# 
        if form.dat_tm.data > datetime.date(datetime.now()):
            flash("Datum mag niet in de toekomst liggen!", category="error")
            redirect( url_for("grafieken_bp.grafieken_gemeentes") )
        
        else:
            dat_van = datetime.combine(form.dat_vanaf.data, datetime.min.time()) # Date naar DateTime conversie
            dat_tot = datetime.combine(form.dat_tm.data, datetime.min.time())    # Date naar DateTime conversie
            if form.prov_sel.data == "Alles":
                prov_filter["$in"] = alle_provincies # List met alle Provincies
                filter = per_prov_gem(prov_filter, dat_van, dat_tot, niveau)
            else:
                filter = per_prov_gem(form.prov_sel.data, dat_van, dat_tot, niveau)
            
            locatie_getallen = covid_col.aggregate(filter)
 
            for item in locatie_getallen:
                gevonden = True
                labels.append(item["_id"])    # Maanden van het jaar (in tekst)
                # bedrag = round(saldo + item["totaal"], 2)
                values.append(item["reported"])

    else:
        print(f"ERRORS: {form.errors}")

    # GET
    form.dat_vanaf.data = datetime.date(datetime.strptime("2021-01-01", "%Y-%m-%d"))
    form.dat_tm.data    = datetime.date(datetime.now())
    # print(f"\n\nFORM - GET : {form.data}")

    return render_template("tot-grafieken.html", labels=labels, values=values, legenda=legenda, type=type, gevonden=gevonden, form=form)

@grafieken_bp.route("/datum-grafieken", methods=["GET", "POST"])
def datum_grafieken():
    labels, values = [], []
    gevonden       = False
    type           = "Periode"
    legenda        = "Totalen per " + type
    
    locatie_getallen = []
    prov_filter      = {}
    form             = DatGrafiekForm()
    alle_provincies  = gemeente_col.distinct("provincie")
    alle_provincies.insert(0, "Alles")
    form.prov_sel.choices = alle_provincies
    alle_gemeentes   = gemeente_col.distinct("gemeente")
    alle_gemeentes.insert(0, "Alles")
    form.gem_sel.choices = alle_gemeentes

    if form.validate_on_submit():
        print("\nGEVALIDEERD!")
        print(f"FORM - POST: {form.data}")
 
        niveau   = "$provincie"
        # if form.gemniveau.data:
            # niveau  = "$gem_naam"
            # type    = "Gemeente"
            # legenda = "Totalen per " + type
 
        if form.dat_tm.data > datetime.date(datetime.now()):
            flash("Datum mag niet in de toekomst liggen!", category="error")
            redirect( url_for("grafieken_bp.datum_grafieken") )
        
        else:
            print(f"DATUM KLOPT...")
            dat_van = datetime.combine(form.dat_vanaf.data, datetime.min.time()) # Date naar DateTime conversie
            dat_tot = datetime.combine(form.dat_tm.data, datetime.min.time())    # Date naar DateTime conversie
            if form.gem_sel.data != "Alles":
                # print(f"ONGELIJK AAN 'ALLES'")
                # prov_filter["$in"] = alle_provincies # List met alle Provincies
                filter = per_week(form.gem_sel.data, dat_tot )
                # print(f"FILTER = {filter}")
            else:
                # print(f"GELIJK AAN 'ALLES'")
                flash("Kies één Gemeente...", category="error")
                redirect( url_for("grafieken_bp.datum_grafieken") )
            
            locatie_getallen = covid_col.aggregate(filter)
 
            for item in locatie_getallen:
                # print(f"ITEM: {item}")
                gevonden = True
                labels.append(item["_id"])      # Weeknummers van het jaar
                values.append(item["reported"]) # Gerapporteerd per week

    else:
        print(f"ERRORS: {form.errors}")

    # GET
    form.dat_vanaf.data = datetime.date(datetime.strptime("2021-01-01", "%Y-%m-%d"))
    form.dat_tm.data    = datetime.date(datetime.now())
    # print(f"\n\nFORM - GET : {form.data}")

    print(f"LABELS: {labels}")
    print(f"VALUES: {values}")

    return render_template("dat-grafieken.html", labels=labels, values=values, legenda=legenda, type=type, gevonden=gevonden, form=form)

@grafieken_bp.route("/grafieken-casuslandelijk", methods=["GET", "POST"])
def grafieken_casuslandelijk():
    return "<h1>Dit is grafieken_casuslandelijk</h1>"
