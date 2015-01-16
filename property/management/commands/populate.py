from django.core.management.base import BaseCommand
from property.models import Property
import csv, json, requests

class Command(BaseCommand):
	help ='populate the Property Model with data'
	




	def handle(self,*args, **options):
		api_key = "0df4a4bd-fd97-4b88-8a44-169659d70b55"
		baseurl = 'https://auspost.com.au/api/postcode/search.json?q='
		Model_import_list =[]
		with open ('data.csv','rU') as csvfile:
			reader = csv.reader(csvfile)
			data=[]
			for row in reader:
				data.append(row)
			headers=data[0]
			data = data[1:-1]
		final_data=[]
		for row in data:
			index = 0
			Temp_list = {}
			for cell in row:
				Temp_list[headers[index]] = cell
				index = index + 1
			final_data.append(Temp_list)

		for each in final_data:
			propertyobject = Property(imagesourceURL=each["imagesourceURL"],street_address=each['street_address'],suburb=each['suburb'],state=each['state'],postcode=0000, baths=each['baths'],cars=each['cars'],beds=each['beds'])
			propertyobject.cache()
			propertyobject.getpostcode()
			propertyobject.save()

		all_entries = Property.objects.all()
		for each in all_entries:
			print 













'''
 propertyUID = models.AutoField(primary_key=True)
   client = models.ManyToManyField(Client,blank=True)
   street_address = models.CharField(max_length=255, db_index=True)
   suburb = models.CharField(max_length=120, db_index=True)
   state = models.CharField(max_length=3, db_index=True)
   postcode = models.IntegerField(max_length=4, db_index=True)
   date_added = models.DateTimeField(editable=False,auto_now=True)
	baths = models.IntegerField(max_length=2,default=0)
	cars = models.IntegerField(max_length=2,default=0)
	beds = models.IntegerField(max_length=2,default=0)

'''

'''

'''