from datetime    import datetime
from flask       import Blueprint, render_template, flash
from collections import defaultdict

from .forms import ImportGemeentenForm
from .      import importeer_gemeentes, importeer_testdata
from ..pipelines import test_totalen
from covidFlask import mytools

inlezen_bp = Blueprint("inlezen_bp", __name__, 
    template_folder= "templates",
    static_folder  = "static")

@inlezen_bp.route("/inlezen-gemeentes", methods=["GET", "POST"])
def inlezen_gemeentes():

    is_verwerkt  = False
    laatst_verwerkt_dat = ""
    aantallen    = defaultdict(int)
    form         = ImportGemeentenForm(dry_run=True)
    verwerkt_tot = mytools.laatste_datum()  #laatste_datum() in STR formaat
    form.laatst_verwerkt.data = verwerkt_tot

    if form.is_submitted():  # POST
        # meldingen, fout = importeer_gemeentes.haal_csv()
        csv_file        = "COVID-19_aantallen_gemeente_per_dag.csv"
        meldingen, fout = mytools.haal_csv(csv_file)
        for melding in meldingen:
            flash(melding, category="info")

        if not fout:
            aantallen, laatst_verwerkt_dat = importeer_gemeentes.verwerk_gemeentes(csv_file, verwerkt_tot, dry_run=form.dry_run.data)
            laatst_verwerkt_dat = datetime.strftime(laatst_verwerkt_dat, "%Y-%m-%d")
            is_verwerkt = True
            flash(f"[COVID] Aantal verwerkt: {aantallen['verwerkt']}", category="info")

        if form.dry_run.data:
            flash(f"[COVID] DIT WAS EEN OEFENING...", category="error")

        form.laatst_verwerkt.data = mytools.laatste_datum()

    ## GET

    return render_template("/inlezen-gemeentes.html", form=form, is_verwerkt=is_verwerkt, aantallen=aantallen, laatst_verwerkt_dat=laatst_verwerkt_dat)

@inlezen_bp.route("/inlezen-testdata", methods=["GET", "POST"])
def inlezen_testdata():

    is_verwerkt  = False
    laatst_verwerkt_dat = ""
    aantallen    = defaultdict(int)
    form         = ImportGemeentenForm(dry_run=True)
    verwerkt_tot = mytools.laatste_datum (collection="covid_test")  #laatste_datum() in STR formaat
    form.laatst_verwerkt.data = verwerkt_tot
    totalen = {}

    if form.is_submitted():  # POST
        csv_file        = "COVID-19_uitgevoerde_testen.csv"
        meldingen, fout = mytools.haal_csv(csv_file)
        for melding in meldingen:
            flash(melding, category="info")

        if not fout:
            aantallen, laatst_verwerkt_dat, fout = importeer_testdata.verwerk_testdata(csv_file, verwerkt_tot, dry_run=form.dry_run.data)
            if fout:
                flash(f"[COVID] Er is iets fout gegaan. Versienummer?", category="error")
            else:
                laatst_verwerkt_dat = datetime.strftime(laatst_verwerkt_dat, "%Y-%m-%d")
                is_verwerkt = True
                flash(f"[COVID] Aantal verwerkt: {aantallen['verwerkt']:5,d}".replace(",","."), category="info")

            if form.dry_run.data:
                flash(f"[COVID] DIT WAS EEN OEFENING...", category="error")

        # filter = test_totalen("null")
        # print(f"FILTER: {filter}")
        
        totalen['verwerkt'] = f"{aantallen['verwerkt']:10,d}".replace(",",".")  # Formatering op formulier
        totalen['positief'] = f"{aantallen['positief']:10,d}".replace(",",".")
        totalen['getest']   = f"{aantallen['getest']:5,d}".replace(",",".")
        print(f"TOTALEN: {totalen}")
        
    ## GET

    return render_template("/inlezen-testdata.html", form=form, is_verwerkt=is_verwerkt, aantallen=totalen, laatst_verwerkt_dat=laatst_verwerkt_dat)
