from flask    import Blueprint, render_template, flash, redirect, url_for #, request, redirect, url_for, flash #, session
from datetime import datetime

from covidFlask.db        import gemeente_col, covid_col, covid_test
from .forms               import TotGrafiekForm, DatGrafiekForm, TstDatGrafiekForm
from covidFlask.pipelines import per_prov_gem, per_week, testen_per_periode

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
    periode        = "W"
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
        # print(f"FORM - POST: {form.data}")

        if form.pertijd.data == "perdag":
            periode = "D"
        elif form.pertijd.data == "perweek":
            periode = "W"
        else:
            periode = "M"

        if form.dat_tm.data > datetime.date(datetime.now()):
            flash("Datum mag niet in de toekomst liggen!", category="error")
            redirect( url_for("grafieken_bp.datum_grafieken") )
        
        else:
            # print(f"DATUM KLOPT...")
            dat_van = datetime.combine(form.dat_vanaf.data, datetime.min.time()) # Date naar DateTime conversie
            dat_tot = datetime.combine(form.dat_tm.data, datetime.min.time())    # Date naar DateTime conversie
            
            # Provincie: Specifiek -> Gemeente: Alles     -> gegevens alle gemeentes van die provincie
            # Provincie: Specifiek -> Gemeente: Specifiek -> gegevens van alleen die gemeente binnen die provincie
            # filter = per_week("G", periode, form.gem_sel.data, dat_van, dat_tot )
            if form.prov_sel.data == "Alles":   # Provincie: Alles     -> alleen provincie gegevens
                # print(f"ALLEEN ALLE PROVINCIES")
                prov_filter["$in"] = alle_provincies                   # Filter: { "$in: ['List alle provincies'] }
                filter = per_week("P", periode, prov_filter, dat_van, dat_tot )
            elif form.gem_sel.data == "Alles":
                # filter met 1 provincie en alle gemeentes
                # print(f"SPECIFIEKE PROVINCIE, ALLE GEMEENTES")
                filter = per_week("P", periode, form.prov_sel.data, dat_van, dat_tot )
            elif form.gem_sel.data != "Alles":
                # print(f"SPECIFIEKE PROVINCIE, SPECIFIEKE GEMEENTE")
                filter = per_week("G", periode, form.gem_sel.data, dat_van, dat_tot )

            # if form.gem_sel.data != "Alles":
                # print(f"ONGELIJK AAN 'ALLES'")
                # prov_filter["$in"] = alle_provincies # List met alle Provincies
                # filter = per_week("G", form.gem_sel.data, dat_van, dat_tot )
                # print(f"FILTER = {filter}")
            # else:
                print(f"GELIJK AAN 'ALLES'")
                # flash("Kies één Gemeente...", category="error")
                # redirect( url_for("grafieken_bp.datum_grafieken") )
            
            locatie_getallen = covid_col.aggregate(filter)
 
            for item in locatie_getallen:
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

@grafieken_bp.route("/test-grafieken", methods=["GET", "POST"])
def tot_test_grafieken():
    return "<h1>Dit is test-grafieken</h1>"

@grafieken_bp.route("/test-datum-grafieken", methods=["GET", "POST"])
def tot_test_datum_grafieken():
    labels, valuesA, valuesB = [], [], []
    periode        = "W"
    gevonden       = False
    grafiek_type   = "Periode"
    legenda1       = "Totaal Getest per " + grafiek_type
    legenda2       = "Totaal Positief per " + grafiek_type
    
    locatie_getallen = []
    regio_filter     = {}
    form             = TstDatGrafiekForm()
    alle_regios      = covid_test.distinct("sec_reg_naam")
    alle_regios.insert(0, "Alles")
    y_as_min, y_as_max = 0, 0
    form.regio_sel.choices = alle_regios

    # print(f"REGIO keuzes    : {form.regio_sel.choices}")
    # print(f"REGIO vóór POST : {form.regio_sel.data}")
    if form.validate_on_submit():
        print("\nGEVALIDEERD!")
        print(f"FORM - POST: {form.data}")

        if form.pertijd.data == "perdag":
            periode = "D"
        elif form.pertijd.data == "perweek":
            periode = "W"
        else:
            periode = "M"

        if form.dat_tm.data > datetime.date(datetime.now()):
            flash("Datum mag niet in de toekomst liggen!", category="error")
            redirect( url_for("grafieken_bp.tot_test_datum_grafieken") )
        
        else:
            # print(f"DATUM KLOPT...")
            dat_van = datetime.combine(form.dat_vanaf.data, datetime.min.time()) # Date naar DateTime conversie
            dat_tot = datetime.combine(form.dat_tm.data, datetime.min.time())    # Date naar DateTime conversie
            
            # Provincie: Specifiek -> Gemeente: Alles     -> gegevens alle gemeentes van die provincie
            # Provincie: Specifiek -> Gemeente: Specifiek -> gegevens van alleen die gemeente binnen die provincie
            # filter = per_week("G", periode, form.gem_sel.data, dat_van, dat_tot )
            if form.regio_sel.data == "Alles":   # Regio: Alles  -> Alle testgegevens
                # print(f"ALLEEN ALLE PROVINCIES")
                regio_filter["$in"] = alle_regios                   # Filter: { "$in: ['List alle provincies'] }
                filter = testen_per_periode("A", periode, regio_filter, dat_van, dat_tot )
            elif form.regio_sel.data != "Alles":
                # print(f"SPECIFIEKE PROVINCIE, SPECIFIEKE GEMEENTE")
                filter = testen_per_periode("R", periode, form.regio_sel.data, dat_van, dat_tot )

            if int(form.y_as_min.data) >= int(form.y_as_max.data):
                flash("Y-as minimum moet kleiner zijn dan Y-as maximum!", category="error")
                redirect( url_for("grafieken_bp.tot_test_datum_grafieken") )
            else:
                print(f"Y-AS WAARDEN GEVULD")
                y_as_min = int(form.y_as_min.data)
                y_as_max = int(form.y_as_max.data)
            # print(f"FILTER: {filter}")
            locatie_getallen = covid_test.aggregate(filter)
 
            for item in locatie_getallen:
                gevonden = True
                # if item["_id"] >= 6:
                    # item["_id"] = "2020-" + item["_id"]
                # else:
                    # item["_id"] = "2021-" + item["_id"]
                labels.append(item["_id"])           # Periodenummers van het jaar (dag, week of maand)
                valuesA.append(item["tot_getest"])   # Gerapporteerd per periode
                valuesB.append(item["tot_positief"]) # Gerapporteerd per periode

    else:
        print(f"ERRORS: {form.errors}")
        print(f"DATA  : {form.data}")

    # GET
    form.dat_vanaf.data = datetime.date(datetime.strptime("2021-01-01", "%Y-%m-%d"))
    form.dat_tm.data    = datetime.date(datetime.now())
    form.y_as_min.data, form.y_as_max.data = 0, 0
    # form.regio_sel.choices = alle_regios
    # print(f"REGIO keuzes GET: {alle_regios}")
    

    # print(f"\n\nFORM - GET : {form.data}")

    print(f"LABELS : {labels}")
    print(f"VALUESA: {valuesA}")
    print(f"VALUESB: {valuesB}")
    print(f"Y-MIN: {y_as_min}, Y-MAX: {y_as_max}")

    return render_template("tot-test-dat-grafieken.html", labels=labels, valuesA=valuesA, valuesB=valuesB, 
        legenda1=legenda1, legenda2=legenda2, grafiek_type=grafiek_type, gevonden=gevonden, y_min=y_as_min, y_max=y_as_max, form=form)


@grafieken_bp.route("/grafieken-casuslandelijk", methods=["GET", "POST"])
def grafieken_casuslandelijk():    
    return "<h1>Dit is grafieken_casuslandelijk</h1>"
