from wtforms import Form, StringField
from wtforms.validators import DataRequired, InputRequired, Length
class Inizializzazione(Form):
	nome = StringField('Nome', validators=[DataRequired('Devi inserire un nome'), InputRequired('Devi inserire un nome'), Length(max=30, message='Il nome deve essere più corto di 30 caratteri')])
	cognome = StringField('Cognome', validators=[DataRequired('Devi inserire un cognome'), InputRequired('Devi inserire un cognome'), Length(max=30, message='Il cognome deve essere più corto di 30 caratteri')])