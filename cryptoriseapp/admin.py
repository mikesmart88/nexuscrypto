from django.contrib import admin
from .models import profile, userimage, account, plansubs, transaction, newfile, price, deposite, withdraw 

# Register your models here.

admin.site.register(userimage)
admin.site.register(account)
admin.site.register(plansubs)
admin.site.register(transaction)
admin.site.register(newfile)
admin.site.register(price)
admin.site.register(deposite)
admin.site.register(withdraw)