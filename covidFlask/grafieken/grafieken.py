# from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for #, request, redirect, url_for, flash #, session
# from flask import current_app as app
# from datetime import datetime

from covidFlask.db import gemeente_col, covid_col
from .forms import GrafiekenForm
# from covidFlask import db

grafieken_bp = Blueprint("grafieken_bp", __name__, 
    template_folder= "templates",
    static_folder  = "static")


@grafieken_bp.route("/grafieken-gemeentes", methods=["GET", "POST"])
def grafieken_gemeentes():
    form = GrafiekenForm()
    return render_template("grafieken.html", form=form)

@grafieken_bp.route("/grafieken-casuslandelijk", methods=["GET", "POST"])
def grafieken_casuslandelijk():
    return "<h1>Dit is grafieken_casuslandelijk</h1>"
