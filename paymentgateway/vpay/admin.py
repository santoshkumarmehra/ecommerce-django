from django.contrib import admin
from .models import Product, TotalNumber, CartNumber, TempMyOrder, UserData
# Register your models here.


@admin.register(TempMyOrder)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','productname','money','quantity']

@admin.register(UserData)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','productname','money', 'transactionid']



@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','productname','price','description','image','quantity']


@admin.register(TotalNumber)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','answer']


@admin.register(CartNumber)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','count']