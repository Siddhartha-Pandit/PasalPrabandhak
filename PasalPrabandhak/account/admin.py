from django.contrib import admin

from . models import User,Company,Subscription,Subscription_purchase,attandance,Branch,OTP
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(Subscription)
admin.site.register(Subscription_purchase)
admin.site.register(attandance)
admin.site.register(OTP)
