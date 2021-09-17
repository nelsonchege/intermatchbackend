from django.contrib import admin
from .models import User , UserProfile , Tribe , Gender , Incometype
# Register your models here.

admin.site.register(User)
admin.site.register(Gender)
admin.site.register(UserProfile)
admin.site.register(Incometype)
admin.site.register(Tribe)
