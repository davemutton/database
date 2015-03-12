from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, Context
from property.models import Property, Client, QueryJob, PropertyQuery
from property.forms import QueryJobform
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

 

#reqired for API
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from property import serializers
from serializers import UserSerializer, GroupSerializer,PropertySerializer,ClientSerializer


#helper functions



#end helper functions

# Create your views here.

#no paginantion view

def index(request):
	context = RequestContext(request)
	property_list2 = Property.objects.order_by('postcode')
	context_dict = {'properties':property_list2}
	return render_to_response('property/index.html', context_dict, context)

def CreateQueryJobView(request):
	context = RequestContext(request)
	if request.method == 'POST':
		form = QueryJobform(request.POST)
		if form.is_valid():
			form.save(commit=True)
			redirect_address=str('/property/query/')
			return HttpResponseRedirect(redirect_address,)
		else:
			print form.errors
	else:

		form = QueryJobform()
	return render_to_response('property/query.html', {'form': form}, context)




class CreatePropertyView(CreateView):
	model = Property
	template_name = 'property/edit_contact.html'
	def get_success_url(self):
		return reverse('index')

class UpdatePropertyView(UpdateView):
	model = Property
	template_name = 'property/edit_contact.html'
	def get_success_url(self):
		return reverse('index')





def listing(request):
	#
	#displays propertys 5 on a page
	#
	property_list2 = Property.objects.all()
	for each in property_list2:
		print each.street_address
	paginator = Paginator(property_list2, 5)
	
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

def propertyquerylist(request,queryIDfromurl):
	context = RequestContext(request)
	query_list = PropertyQuery.objects.filter(queryID=queryIDfromurl)
	property_list2 = []
	failed_list = []
	for each in query_list:
		if each.linkedproperty != None:

			property_list2.append(each.linkedproperty)
		else:
			failed_list.append(each)
	print property_list2
	context_dict = {'properties':property_list2,'failed':failed_list,'queryIDfromurl':queryIDfromurl}
	return render_to_response('property/propertyquerylist.html', context_dict, context)


def property_download(request):
	csv_in_memory2 = StringIO()
	writer = csv.writer(csv_in_memory2)
	Property._meta.get_all_field_names()
	field_names = Property._meta.get_all_field_names()
	writer.writerow(field_names)
	property_list2 = Property.objects.all() 
	print property_list2
	for property in property_list2:
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
	in_memory2 = StringIO()
	zip = ZipFile(in_memory2, "a")  
	filenames = []
	property_list2 = Property.objects.all()
	for property in property_list2:
		filenames.append(str(getattr(property, 'imagefile')))
	for fpath in filenames:
		zip.write(os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,fpath), fpath)
	# fix for Linux zip files read in Windows  
	for file in zip.filelist:  
		file.create_system = 0      
	zip.writestr("data.csv",csv_in_memory2.getvalue())
	zip.close()  
	response = HttpResponse(content_type="application/zip")  
	response["Content-Disposition"] = "attachment; filename=properties.zip"  
	in_memory2.seek(0)      
	response.write(in_memory2.read())  
	return response




def queryjoblist(request):
	#
	#displays queries 5 on a page
	#
	query_list = QueryJob.objects.all()

	for each in query_list:
		print each
	paginator = Paginator(query_list, 20)
	
	page = request.GET.get('page')
	try:
		queries = paginator.page(page)
	except PageNotAnInteger:
		 # If page is not an integer, deliver first page.
		queries = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queries = paginator.page(paginator.num_pages)

	return render_to_response('property/queryjoblist.html', {"queries": queries})



def query_download(request, number):
	csv_in_memory2 = StringIO()
	writer = csv.writer(csv_in_memory2)
	Property._meta.get_all_field_names()
	field_names = Property._meta.get_all_field_names()
	writer.writerow(field_names)
	query_list = PropertyQuery.objects.filter(queryID=number) 
	property_list2 = []
	failed_list = []
	for each in query_list:
		if each.linkedproperty != None:
			property_list2.append(each.linkedproperty)
		else:
			failed_list.append(each)
	for property in property_list2:
		row =[]
		for name in field_names:
			try:
				row.append(str(getattr(property, name)))
			except:
				row.append(" ")
		writer.writerow(row)
	failed_in_memory2 = StringIO()
	
	for each in failed_list:
		failed_in_memory2.write(" "+str(each.street_address)+" "+str(each.suburb)+" "+str(each.state)+" "+str(each.postcode)+'\n')
	#
	#create the zip file
	#
	in_memory2 = StringIO()
	zip = ZipFile(in_memory2, "a")  
	filenames = []
	property_list2 = Property.objects.all()
	for property in property_list2:
		filenames.append(str(getattr(property, 'imagefile')))
	for fpath in filenames:
		zip.write(os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,fpath), fpath)
	# fix for Linux zip files read in Windows  
	for file in zip.filelist:  
		file.create_system = 0      
	zip.writestr("data.csv",csv_in_memory2.getvalue())
	zip.writestr("failed.txt",failed_in_memory2.getvalue())
	zip.close()  
	response = HttpResponse(content_type="application/zip")  
	response["Content-Disposition"] = "attachment; filename=properties.zip"  
	in_memory2.seek(0)      
	response.write(in_memory2.read())

	return response






































#API views

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer

class PropertyViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows properties to be viewed or edited.
	"""
	queryset = Property.objects.all()
	serializer_class = PropertySerializer

class ClientViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows properties to be viewed or edited.
	"""
	queryset = Client.objects.all()
	serializer_class = ClientSerializer