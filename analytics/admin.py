from django.contrib import admin
from analytics.models import Page, Location, View, Ad


admin.site.register(Page)
admin.site.register(Location)
admin.site.register(View)
admin.site.register(Ad)