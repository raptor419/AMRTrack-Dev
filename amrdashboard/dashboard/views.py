# Django 
from django.shortcuts import render
from django.contrib.auth import logout
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Python
import oauth2 as oauth

# Models
from dashboard.models import *
from dashboard.forms import UserForm
# Create your views here.

def index(request):
    print ("index: " + str(request.user))

    context = {'hello': 'world'}
    return render(request, 'dashboard/index.html', context)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            return HttpResponseRedirect('/dashboard/login/')
        else:
            print (user_form.errors)
    else:
        user_form = UserForm()


    return render(request,
            'dashboard/register.html',
            {'user_form': user_form, 'registered': registered} )

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/active/')
            else:
                return HttpResponse("Your Dashboard account is disabled.")
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'dashboard/login.html', {})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/dashboard/login/')