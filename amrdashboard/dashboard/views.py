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
import datetime

# Models
from dashboard.models import *
from dashboard.forms import UserForm

from .scripts.googlelogin import *
# Create your views here.


# Add Google API Keys for Google login
GOOGLE_API_APP_ID=''
GOOGLE_API_APP_SECRET=''


getGoogle = GoogleLogin(GOOGLE_API_APP_ID, GOOGLE_API_APP_SECRET)
profile_track = None

def index(request):
    print ("index: " + str(request.user))
    if str(request.user)=="AnonymousUser":
    	profile_track=None
    if not request.user.is_active:       
	    if request.GET.items():
	            if profile_track == 'google':
	                code = request.GET['code']
	                state = request.GET['state']
	                getGoogle.get_access_token(code, state)
	                userInfo = getGoogle.get_user_info()
	                username = userInfo['given_name'] + userInfo['family_name']

	                try:
	                    user = User.objects.get(username=username+'_google')
	                except User.DoesNotExist:
	                    new_user = User.objects.create_user(username+'_google', username+'@madewithgoogleplus', 'password')
	                    new_user.save()

	                    try:
	                        profle = GoogleProfile.objects.get(user = new_user.id)
	                        profile.access_token = getGoogle.access_token
	                    except:
	                        profile = GoogleProfile()
	                        profile.user = new_user
	                        profile.google_user_id = userInfo['id']
	                        profile.access_token = getGoogle.access_token
	                        profile.profile_url = userInfo['link']
	                    profile.save()
	                user = authenticate(username=username+'_google', password='password')
	                login(request, user)
    else:
        if request.GET.items():
            user = User.objects.get(username = request.user.username)


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

def google_login(request):
    global profile_track
    profile_track = 'google'
    google_url = getGoogle.get_authorize_url()
    return HttpResponseRedirect(google_url)