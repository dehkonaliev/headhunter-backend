from django.contrib import admin
from .models import CustomUser, TempUser, MyToken

admin.site.register(CustomUser)
admin.site.register(TempUser)
admin.site.register(MyToken)