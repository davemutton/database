from django import forms
from property.models import Property, QueryJob

class Propertyform(forms.Form):
	class Meta:
		model = Property
		Fields = "image"

class QueryJobform(forms.ModelForm):
	class Meta:
		model = QueryJob
		fields = ['Json', 'street_column', 'state_column', 'suburb_column','postcode_column']
'''
		Json = forms.te(label='json-submission')
		street_column =forms.CharField(label='street_address-submission')
		state_column =forms.CharField(label='state-submission') 
		suburb_column =forms.CharField(label='suburb-submission') 
		postcode_column =forms.CharField(label='postcode-submission') 
	'''