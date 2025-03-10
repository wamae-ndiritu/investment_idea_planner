from django.contrib import admin
from .models import InvestmentIdea, InvestmentPlan, CustomUser, Saving, Notification

admin.site.register(InvestmentIdea),
admin.site.register(InvestmentPlan),
admin.site.register(CustomUser),
admin.site.register(Saving),
admin.site.register(Notification),
