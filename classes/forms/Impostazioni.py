from wtforms import Form, IntegerField
from wtforms.validators import InputRequired, NumberRange
class Impostazioni(Form):
	intervalloMetar: IntegerField = IntegerField('Intervallo aggiornamento METAR', validators=[InputRequired('Devi inserire un valore'), NumberRange(min=1, message='Inserisci un numero maggiore di 0')])