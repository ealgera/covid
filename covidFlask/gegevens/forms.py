from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField, BooleanField
# from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed

class GegevensForm(FlaskForm):
    # keuzes    = RadioField("Keuze", choices=[('provincie','Provincie'),('gemeente','Gemeente')])
    prov_sel  = SelectField("Provincie")
    dat_vanaf = DateField("Vanaf", format="%Y-%m-%d")
    dat_tm    = DateField("Tot en Met", format="%Y-%m-%d")
    gemniveau = BooleanField(label="Per Gemeente?")

    submit    = SubmitField('Laat gegevens zien')

class RegioForm(FlaskForm):
    regio_sel = SelectField("Regio")
    dat_vanaf = DateField("Vanaf", format="%Y-%m-%d")
    dat_tm    = DateField("Tot en Met", format="%Y-%m-%d")

    submit    = SubmitField('Laat gegevens zien')

class CasusForm(FlaskForm):
    # keuzes    = RadioField("Keuze", choices=[('provincie','Provincie'),('gemeente','Gemeente')])
    prov_sel  = SelectField("Provincie")
    dat_vanaf = DateField("Vanaf", format="%Y-%m-%d")
    dat_tm    = DateField("Tot en Met", format="%Y-%m-%d")
    # gemniveau = BooleanField(label="Per Gemeente?")

    submit    = SubmitField('Laat gegevens zien')
