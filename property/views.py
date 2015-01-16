from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from property.models import Property
from django.conf import settings

#required for paginantion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#required for csv download
import csv

#required for create page
from django.core.urlresolvers import reverse
from django.views.generic import CreateView

#required for edit page
from django.views.generic import UpdateView



#required for image download
import os
from StringIO import StringIO  
from zipfile import ZipFile





#helper functions



#end helper functions

# Create your views here.

#no paginantion view

def index(request):
	context = RequestContext(request)
	property_list = Property.objects.order_by('postcode')
	context_dict = {'properties':property_list}
	return render_to_response('property/index.html', context_dict, context)


class CreatePropertyView(CreateView):
	model = Property
	template_name = 'property/edit_contact.html'
	def get_success_url(self):
		return reverse('index')






def listing(request):
	#
	#displays propertys 5 on a page
	#
	property_list = Property.objects.all()
	for each in property_list:
		print each.street_address
	paginator = Paginator(property_list, 5)
	
	page = request.GET.get('page')
	try:
		propertys = paginator.page(page)
	except PageNotAnInteger:
		 # If page is not an integer, deliver first page.
		propertys = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		propertys = paginator.page(paginator.num_pages)

	return render_to_response('property/list.html', {"propertys": propertys})


def property_download(request):
	csv_in_memory = StringIO()
	writer = csv.writer(csv_in_memory)
	Property._meta.get_all_field_names()
	field_names = Property._meta.get_all_field_names()
	writer.writerow(field_names)
	property_list = Property.objects.all()
	for property in property_list:
		row =[]
		for name in field_names:
			try:
				row.append(str(getattr(property, name)))
			except:
				row.append(" ")
		writer.writerow(row)
	#
	#create the zip file
	#
	in_memory = StringIO()
	zip = ZipFile(in_memory, "a")  
	filenames = []
	property_list = Property.objects.all()
	for property in property_list:
		filenames.append(str(getattr(property, 'imagefile')))
	for fpath in filenames:
		zip.write(os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,fpath), fpath)
	# fix for Linux zip files read in Windows  
	for file in zip.filelist:  
		file.create_system = 0      
	zip.writestr("data.csv",csv_in_memory.getvalue())
	zip.close()  
	response = HttpResponse(content_type="application/zip")  
	response["Content-Disposition"] = "attachment; filename=properties.zip"  
	in_memory.seek(0)      
	response.write(in_memory.read())  
	return response


