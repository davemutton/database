from django import forms
from property.models import Property

class Propertyform(forms.Form):
	class Mete:
		model = Property
		Fields =