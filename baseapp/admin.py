from django.contrib import admin
from .models import Category, Region, Lang, District, Skill

admin.site.register(Category)
admin.site.register(Region)
admin.site.register(Lang)
admin.site.register(District)
admin.site.register(Skill)
