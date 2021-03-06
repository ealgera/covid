from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField, BooleanField, RadioField, IntegerField
# from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed

class TotGrafiekForm(FlaskForm):
    # keuzes    = RadioField("Keuze", choices=[('provincie','Provincie'),('gemeente','Gemeente')])
    prov_sel  = SelectField("Provincie")
    dat_vanaf = DateField("Vanaf", format="%Y-%m-%d")
    dat_tm    = DateField("Tot en Met", format="%Y-%m-%d")
    gemniveau = BooleanField(label="Per Gemeente?")

    submit    = SubmitField('Laat gegevens zien')

class DatGrafiekForm(FlaskForm):
    prov_sel  = SelectField("Provincie")
    gem_sel   = SelectField("Gemeente")
    dat_vanaf = DateField("Vanaf", format="%Y-%m-%d")
    dat_tm    = DateField("Tot en Met", format="%Y-%m-%d")
    gemniveau = BooleanField(label="Per Gemeente?")
    pertijd   = RadioField("", choices=[ ("perdag","dag"), ("perweek","week"), ("permaand","maand") ], default='perweek' )
    persoort  = RadioField("", choices=[ ("perbesmet","besmet"), ("peropname","opname"), ("peroverlijden","overlijden") ], 
        default='perbesmet' )

    submit    = SubmitField('Laat gegevens zien')

class TstDatGrafiekForm(FlaskForm):
    regio_sel = SelectField("Veiligheidsregio")
    dat_vanaf = DateField("Vanaf", format="%Y-%m-%d")
    dat_tm    = DateField("Tot en Met", format="%Y-%m-%d")
    regniveau = BooleanField(label="Per Veiligheidsregio?")
    pertijd   = RadioField("", choices=[ ("perdag","dag"), ("perweek","week"), ("permaand","maand") ], default='perweek' )
    y_as_min  = IntegerField("Y-as minimum")
    y_as_max  = IntegerField("Y-as maximum")

    submit    = SubmitField('Laat gegevens zien')
