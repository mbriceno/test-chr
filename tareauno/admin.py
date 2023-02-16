from django.contrib import admin

from tareauno.models import Network, Company, Payment_Types, Station, Location

class Network_Admin(admin.ModelAdmin):
    list_display = ['name', 'external_id',]


class Company_Admin(admin.ModelAdmin):
    list_display = ['name']


class Payment_Types_Admin(admin.ModelAdmin):
    list_display = ['name']


class Station_Admin(admin.ModelAdmin):
    list_display = ['name', 'external_id', 'network_name']

    def network_name(self, obj):
        return "{}".format(obj.network.name)


class Location_Admin(admin.ModelAdmin):
    list_display = ['city', 'country', 'latitude', 'longitude']


admin.site.register(Network, Network_Admin)
admin.site.register(Company, Company_Admin)
admin.site.register(Payment_Types, Payment_Types_Admin)
admin.site.register(Station, Station_Admin)
admin.site.register(Location, Location_Admin)
