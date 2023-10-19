from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(About)
admin.site.register(Service)
admin.site.register(History)
admin.site.register(Team)



admin.site.site_header = 'Smart Pro Centre'
admin.site.site_title = 'Smart Pro Centre'