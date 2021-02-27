from datetime import datetime
from flask  import Blueprint, render_template, flash
from collections import defaultdict
# from flask.globals import request

from .forms import ImportGemeentenForm
from .      import importeer_gemeentes, importeer_testdata

inlezen_bp = Blueprint("inlezen_bp", __name__, 
    template_folder= "templates",
    static_folder  = "static")

@inlezen_bp.route("/inlezen-gemeentes", methods=["GET", "POST"])
def inlezen_gemeentes():

    is_verwerkt  = False
    laatst_verwerkt_dat = ""
    aantallen    = defaultdict(int)
    form         = ImportGemeentenForm(dry_run=True)
    verwerkt_tot = importeer_gemeentes.laatste_datum()  #laatste_datum() in STR formaat
    form.laatst_verwerkt.data = verwerkt_tot

    if form.is_submitted():  # POST
        meldingen, fout = importeer_gemeentes.haal_csv()
        for melding in meldingen:
            flash(melding, category="info")

        if not fout:
            aantallen, laatst_verwerkt_dat = importeer_gemeentes.verwerk_gemeentes(verwerkt_tot, dry_run=form.dry_run.data)
            laatst_verwerkt_dat = datetime.strftime(laatst_verwerkt_dat, "%Y-%m-%d")
            is_verwerkt = True
            flash(f"[COVID] Aantal verwerkt: {aantallen['verwerkt']}", category="info")

        form.laatst_verwerkt.data = importeer_gemeentes.laatste_datum()

    ## GET

    return render_template("/inlezen-gemeentes.html", form=form, is_verwerkt=is_verwerkt, aantallen=aantallen, laatst_verwerkt_dat=laatst_verwerkt_dat)

@inlezen_bp.route("/inlezen-testdata", methods=["GET", "POST"])
def inlezen_testdata():

    is_verwerkt  = False
    laatst_verwerkt_dat = ""
    aantallen    = defaultdict(int)
    form         = ImportGemeentenForm(dry_run=True)
    verwerkt_tot = importeer_testdata.laatste_datum()  #laatste_datum() in STR formaat
    form.laatst_verwerkt.data = verwerkt_tot

    if form.is_submitted():  # POST
        meldingen, fout = importeer_testdata.haal_csv()
        for melding in meldingen:
            flash(melding, category="info")

        if not fout:
            aantallen, laatst_verwerkt_dat = importeer_testdata.verwerk_testdata(verwerkt_tot, dry_run=form.dry_run.data)
            laatst_verwerkt_dat = datetime.strftime(laatst_verwerkt_dat, "%Y-%m-%d")
            is_verwerkt = True
            flash(f"[COVID] Aantal verwerkt: {aantallen['verwerkt']}", category="info")

        form.laatst_verwerkt.data = importeer_testdata.laatste_datum()

    ## GET

    return render_template("/inlezen-testdata.html", form=form, is_verwerkt=is_verwerkt, aantallen=aantallen, laatst_verwerkt_dat=laatst_verwerkt_dat)
