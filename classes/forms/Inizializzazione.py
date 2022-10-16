from wtforms import Form, StringField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange
class Inizializzazione(Form):
	nome: StringField = StringField('Nome', validators=[InputRequired('Devi inserire un nome'), Length(max=30, message='Il nome deve essere più corto di 30 caratteri')])
	cognome: StringField = StringField('Cognome', validators=[InputRequired('Devi inserire un cognome'), Length(max=30, message='Il cognome deve essere più corto di 30 caratteri')])
	base: SelectField = SelectField('Base', validators=[InputRequired('Devi selezionare una base')], coerce=int)
	intervalloMetar: IntegerField = IntegerField('Intervallo aggiornamento METAR', validators=[InputRequired('Devi inserire un valore'), NumberRange(min=1, message='Inserisci un numero maggiore di 0')])

	def __init__(self, basi=[], *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.base.choices = basi