from django.http import HttpResponse, JsonResponse
import json
import random
import re
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# from .models import Question, Result,UserData
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, TotalNumber, CartNumber, TempMyOrder, UserData
from django.conf import settings
from django.db.models import Sum


def user_home(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'vpay/home.html', {'user':user})
    else:
        return redirect('/signin/')


def checkemail(s):
    pat = "[a-zA-Z-_\.\-]+@[a-zA-Z]+\.[a-z]{2,3}$"
    if re.match(pat,s):
        return s
    else:
        return None


def user_sign_up(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mailvalidation = checkemail(email)
        if first_name == '' or last_name == '' or email == '' or password == '' :
            messages.error(request, "fill the field correctly")
            return render(request, 'vpay/signup.html')
        elif  mailvalidation == None:
            messages.error(request, "invalid email")
            return render(request, 'vpay/signup.html')
        else:
            User.objects.create(username=first_name,first_name=first_name, last_name=last_name, email=email, password=make_password(password))
            # MyOrder.objects.create(user=first_name)
            messages.success(request, 'Account has been created !!!')
            return render(request, 'vpay/signup.html')
    return render(request, 'vpay/signup.html')


def user_sign_in(request):
    # import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
    if request.method == "POST":
        email = request.POST.get('email')
        # print(email)
        password = request.POST.get('password')
        user_data= User.objects.all()
        for data in user_data:
            if data.email == email:
                # MyOrder.User.create(user=data.username)
                user_object = authenticate(request, username=data.username, password=password)
                if user_object is not None:
                    login(request, user_object)
                    # print(user_object)
                    return redirect('/products/')
        return render(request, 'vpay/signin.html')
    elif request.user.is_authenticated:
        return redirect('/products/')
    else:
        return render(request, 'vpay/signin.html')


def user_product(request):
    # import pdb;pdb.set_trace()
    if request.user.is_authenticated:
        # user = User.objects.all()
        # print(request.user)
        product = Product.objects.all()
        return render(request, 'vpay/product.html', {'product':product})#, 'user':user})
    else:
        return redirect('/signin/')


def user_products(request):
    if request.user.is_authenticated:        
        username = request.user
        if request.method =="POST":
            minus = request.POST.get('minus')
            # print(minus)
            data = Product.objects.filter(id=minus)
            for query in data:                                    
                for query1 in TempMyOrder.objects.all():
                    if  query.productname == query1.productname:
                        TempMyOrder.objects.filter(productname=query.productname).earliest('productname').delete()
                    value = 0
                    money = TempMyOrder.objects.filter(username=username).aggregate(Sum('money'))
                    for rupee in money:
                        value = money[rupee]
                    val = 0    
                    for noofproduct in TempMyOrder.objects.filter(username=username):
                        val += 1         
                    product = Product.objects.all()
                    return render(request, 'vpay/products.html', {'product':product, 'amount':value, 'count':val})
              
            productname = request.POST.get('plus')            
            # print(plus)
            value = request.POST.get('money')   
            productname = request.POST.get('productname')
            # print(productname)  
            val1 = int(float(value))
            TotalNumber.objects.create(username=username, answer=val1)
            CartNumber.objects.create(username=username, count=val1)
            TempMyOrder.objects.create(username=username, productname=productname, money=value)

        for products in Product.objects.all():
            val = TempMyOrder.objects.filter(username=username).get(products.id)
            
        value = 0
        # money = TotalNumber.objects.aggregate(Sum('answer'))
        money = TempMyOrder.objects.filter(username=username).aggregate(Sum('money'))
        for rupee in money:
            value = money[rupee]
        #for cart
        val = 0    
        for noofproduct in TempMyOrder.objects.filter(username=username):
            val += 1         
        product = Product.objects.all()
        return render(request, 'vpay/products.html', {'product':product, 'amount':value, 'count':val})
    
    else:
        redirect('/signin/')






def myorder(request):
    if request.user.is_authenticated:
        user = request.user
        val = 0
        for tempmoney in CartNumber.objects.filter(username=user):
            val += 1        
        money = TempMyOrder.objects.aggregate(Sum('money'))
        value=0
        for rupee in money:
            value = money[rupee]      
        allvalue = UserData.objects.filter(username=user)
        return render(request, 'vpay/myorder.html', {'count':val, 'allvalue':allvalue, 'value':value})
    else:
        return redirect('/signin/')


def user_signout(request):
    logout(request)
    return redirect('/signin/')


@login_required(login_url='/signin/')
def buy(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method =="POST":
        # print(request.POST.get('id'))
            value = request.POST.get('money')   
            val1 = int(float(value))
            TotalNumber.objects.create(answer=val1)
        # amount = TotalNumber.objects.all()
        TN = TotalNumber.objects.aggregate(Sum('answer'))
        for i in TN:
            value = TN[i]

        val = 0
        for tempmoney in CartNumber.objects.filter(username=user):
            val += 1
        product = Product.objects.all()
        return render(request, 'vpay/buy.html', {'product':product, 'amount':value, 'val':val})
    else:
        redirect('/signin/')


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        val = 0
        for tempmoney in CartNumber.objects.filter(username=user):
            val += 1    
        money = TempMyOrder.objects.aggregate(Sum('money'))
        value=0
        for rupee in money:
            value = money[rupee]
        allvalue = TempMyOrder.objects.filter(username=user)
        return render(request, 'vpay/cart.html', {'count':val, 'allvalue':allvalue, 'value':value})
    else:
        return redirect('/signin/')


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        val = 0
        for tempmoney in CartNumber.objects.filter(username=user):
            val += 1    
        money = TempMyOrder.objects.aggregate(Sum('money'))
        value=0
        for rupee in money:
            value = money[rupee]
        # allvalue = TempMyOrder.objects.all()
        return render(request, 'vpay/checkout.html', {'count':val, 'amount':value})
    else:
        return redirect('/signin/')

def payment(request, id):
    # import pdb;pdb.set_trace()
    if request.user.is_authenticated:
        user = request.user
        userdata = TempMyOrder.objects.filter(username=user)
        for data in userdata:
            UserData.objects.create(username=data.username, productname=data.productname, money=data.money, transactionid=id)        
            CartNumber.objects.filter(username=user).delete()
            TempMyOrder.objects.filter(username=user).delete()
            TotalNumber.objects.filter(username=user).delete()
        return render(request, 'vpay/successfullpayment.html')
    else:
        return redirect('/signin/')



   




    # for products in Product.objects.all():
                    #     try :
                    #         val = TempMyOrder.objects.filter(username=username).get(products.id)
                    