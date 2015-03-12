from django.contrib.auth.models import User, Group
from rest_framework import serializers
from property.models import Property, Client

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class PropertySerializer(serializers.ModelSerializer):
	class Meta:
		model = Property
		fields = ('propertyUID','client','street_address', 'suburb','state','postcode','date_added','baths','cars','beds','imagesourceURL','imagefile')

class ClientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Client
		fields = ('clientUID','client_name')
