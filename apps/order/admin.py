from django.contrib import admin
from apps.order import models


admin.site.register(models.Order)
admin.site.register(models.Suggest)
admin.site.register(models.Assign)