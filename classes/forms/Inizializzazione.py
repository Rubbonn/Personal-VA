from wtforms import Form, StringField, SelectField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange
class Inizializzazione(Form):
	nome: StringField = StringField('Nome', validators=[DataRequired('Devi inserire un nome'), InputRequired('Devi inserire un nome'), Length(max=30, message='Il nome deve essere più corto di 30 caratteri')])
	cognome: StringField = StringField('Cognome', validators=[DataRequired('Devi inserire un cognome'), InputRequired('Devi inserire un cognome'), Length(max=30, message='Il cognome deve essere più corto di 30 caratteri')])
	base: SelectField = SelectField('Base', validators=[DataRequired('Devi selezionare una base'), InputRequired('Devi selezionare una base')])
	intervalloMetar: IntegerField = IntegerField('Intervallo aggiornamento METAR', validators=[DataRequired('Devi inserire un valore'), InputRequired('Devi inserire un valore'), NumberRange(min=15, message='Inserisci un numero maggiore di 15')])

	def __init__(self, basi=[], *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.base.choices = basi