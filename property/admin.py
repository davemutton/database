from django.contrib import admin
from property.models import Client, Property
class ClientAdmin(admin.ModelAdmin):
	pass
class PropertyImageInline(admin.TabularInline):
	pass
class PropertyAdmin(admin.ModelAdmin):
	pass

admin.site.register(Client, ClientAdmin)
admin.site.register(Property,PropertyAdmin)
