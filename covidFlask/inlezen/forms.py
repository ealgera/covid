from flask_wtf          import FlaskForm
from wtforms            import SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired

class ImportGemeentenForm(FlaskForm):
    laatst_verwerkt = DateField(label="Verwerkt t/m", format="%d-%m-%Y")
    dry_run         = BooleanField(label="Oefenen?")

    submit          = SubmitField('Haal en Verwerk nieuwste gegevens')