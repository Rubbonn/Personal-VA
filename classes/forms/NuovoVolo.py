from wtforms import Form, SelectField, ValidationError
from wtforms.validators import InputRequired
from classes.objectmodels.AeromobilePosseduto import AeromobilePosseduto
from classes.objectmodels.Aeroporto import Aeroporto
class NuovoVolo(Form):
	aeromobile: SelectField = SelectField('Aeromobile', validators=[InputRequired('Devi selezionare un aeromobile da utilizzare')], coerce=int, choices=[(aeromobile.id, f'{aeromobile.aeromobile.nome} ({aeromobile.callsign})') for aeromobile in AeromobilePosseduto.getAeromobiliPosseduti()])
	aeroportoPartenza: SelectField = SelectField('Aeroporto di partenza', validators=[InputRequired('Devi selezionare un aeroporto di partenza')], coerce=int, choices=[(aeroporto.id, f'{aeroporto.nome} ({aeroporto.codiceIcao})') for aeroporto in Aeroporto.getAeroporti()])
	aeroportoArrivo: SelectField = SelectField('Aeroporto di arrivo', validators=[InputRequired('Devi selezionare un aeroport di arrivo')], coerce=int, choices=[(aeroporto.id, f'{aeroporto.nome} ({aeroporto.codiceIcao})') for aeroporto in Aeroporto.getAeroporti()])

	def validate_aeromobile(form: Form, field: SelectField):
		if form.aeroportoPartenza.data is None:
			raise ValidationError('Devi selezionare un aeroporto di partenza')
		aeroportoPartenza: Aeroporto = Aeroporto(form.aeroportoPartenza.data)
		aeromobili: list[AeromobilePosseduto] = aeroportoPartenza.getAeromobiliPosseduti()
		if field.data not in [aeromobile.id for aeromobile in aeromobili]:
			raise ValidationError('L\'aeromobile selezionato non è all\'aeroporto di partenza selezionato')