# Django
import django_tables2 as tables
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import *
# Models
from .models import *
from .scripts.biotable import *
from .scripts.googlelogin import *

# Python

# Create your views here.


# Add Google API Keys for Google login
GOOGLE_API_APP_ID = ''
GOOGLE_API_APP_SECRET = ''

getGoogle = GoogleLogin(GOOGLE_API_APP_ID, GOOGLE_API_APP_SECRET)
profile_track = None

def index(request):
    print("index: " + str(request.user))
    if str(request.user) == "AnonymousUser":
        profile_track = None
    if not request.user.is_active:
        if request.GET.items():
            if profile_track == 'google':
                code = request.GET['code']
                state = request.GET['state']
                getGoogle.get_access_token(code, state)
                userInfo = getGoogle.get_user_info()
                username = userInfo['given_name'] + userInfo['family_name']

                try:
                    user = User.objects.get(username=username + '_google')
                except User.DoesNotExist:
                    new_user = User.objects.create_user(username + '_google', username + '@madewithgoogleplus',
                                                        'password')
                    new_user.save()

                    try:
                        profle = GoogleProfile.objects.get(user=new_user.id)
                        profile.access_token = getGoogle.access_token
                    except:
                        profile = GoogleProfile()
                        profile.user = new_user
                        profile.google_user_id = userInfo['id']
                        profile.access_token = getGoogle.access_token
                        profile.profile_url = userInfo['link']
                    profile.save()
                user = authenticate(username=username + '_google', password='password')
                login(request, user)
    else:
        if request.GET.items():
            user = User.objects.get(username=request.user.username)

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
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request,
                  'dashboard/register.html',
                  {'user_form': user_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your Dashboard account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
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


def active(request):
    if str(request.user) == "AnonymousUser":
        profile_track = None
    if not request.user.is_active:
        if request.GET.items():
            if profile_track == 'google':
                code = request.GET['code']
                state = request.GET['state']
                getGoogle.get_access_token(code, state)
                userInfo = getGoogle.get_user_info()
                username = userInfo['given_name'] + userInfo['family_name']

                try:
                    user = User.objects.get(username=username + '_google')
                except User.DoesNotExist:
                    new_user = User.objects.create_user(username + '_google', username + '@madewithgoogleplus',
                                                        'password')
                    new_user.save()

                    try:
                        profile = GoogleProfile.objects.get(user=new_user.id)
                        profile.access_token = getGoogle.access_token
                    except:
                        profile = GoogleProfile()
                        profile.user = new_user
                        profile.google_user_id = userInfo['id']
                        profile.access_token = getGoogle.access_token
                        profile.profile_url = userInfo['link']
                    profile.save()
                user = authenticate(username=username + '_google', password='password')
                login(request, user)
    else:
        created = True
        table = False
        json = False
        if request.GET.items():
            user = User.objects.get(username=request.user.username)
        if request.method == 'POST':
            input_form = InputDataForm(data=request.POST)
            input_form.fields['ams'].choices = [(x, x) for x in ANTIMICROBIALS]
            input_form.fields['site'].choices = [(x, x) for x in SITES]
            input_form.fields['col'].choices = [(x, x) for x in COLLTYPES]
            input_form.fields['org'].choices = [(x, x) for x in ORGANISMS]
            if input_form.is_valid():
                if not input_form.cleaned_data['ams']:
                    input_form.cleaned_data['ams'] = ANTIMICROBIALS
                if not input_form.cleaned_data['site']:
                    input_form.cleaned_data['site'] = SITES
                if not input_form.cleaned_data['col']:
                    input_form.cleaned_data['col'] = COLLTYPES
                if not input_form.cleaned_data['org']:
                    input_form.cleaned_data['org'] = ORGANISMS
                if not input_form.cleaned_data['startdate']:
                    input_form.cleaned_data['startdate'] = '01-01-1900'
                if not input_form.cleaned_data['enddate']:
                    input_form.cleaned_data['enddate'] = '01-01-2100'
                print(input_form.cleaned_data['ams'])
                print(input_form.cleaned_data['site'])
                print(input_form.cleaned_data['col'])
                print(input_form.cleaned_data['org'])
                print(input_form.cleaned_data['startdate'])
                print(input_form.cleaned_data['enddate'])
                table = generate_anitbiogram(ams=input_form.cleaned_data['ams'], organisms=input_form.cleaned_data['org'],
                                     colltypes=input_form.cleaned_data['col'], sites=input_form.cleaned_data['site'],
                                     startdate=input_form.cleaned_data['startdate'], enddate=input_form.cleaned_data['enddate'])
                # print(table)
                # table.to_csv('data.csv')
                json = table.to_json(orient="split")
                tablehtml = table.to_html()
                # json = table.to_json(orient="split")
                # csv = pd.read_csv("bargraph.csv").to_json()
                return render(request, 'dashboard/active.html',
                              {'form': input_form, 'registered': created, 'table': tablehtml, 'json':json})

            else:
                print(input_form.errors)
        else:
            input_form = InputDataForm()
            input_form.fields['ams'].choices = [(x, x) for x in ANTIMICROBIALS]
            input_form.fields['site'].choices = [(x, x) for x in SITES]
            input_form.fields['col'].choices = [(x, x) for x in COLLTYPES]
            input_form.fields['org'].choices = [(x, x) for x in ORGANISMS]

    return render(request, 'dashboard/active.html', {'form': input_form, 'registered': created, 'table': table,'json':json})


def pathtestcreate(request):
    created = False
    if request.method == 'POST':
        path_form = PathTestForm(data=request.POST)
        if path_form.is_valid():
            path = path_form.save()
            created = True
            return HttpResponseRedirect('/dashboard/addpath/')
        else:
            print(path_form.errors)
    else:
        path_form = PathTestForm()

    return render(request, 'dashboard/addpath.html', {'form': path_form, 'registered': created})


def view_data_raw(request):
    df = getdatatable()
    df['date'] = pd.to_datetime(df['date'])
    fields = ['testid', 'collsite', 'sampletype', 'organism'] + ANTIMICROBIALS
    df = df[df.organism.isin(ORGANISMS) & df.sampletype.isin(COLLTYPES) & df.collsite.isin(SITES)][fields]
    gb = df.groupby(['organism', 'sampletype', 'collsite'])
    tdf = gb.apply(lambda _df: _df.sort_values(by=['testid']))
    print(tdf)
    return HttpResponse(tdf.to_html())


def complete_antibiogram(request):
    df = getdatatable()
    df['date'] = pd.to_datetime(df['date'])
    fields = ['testid', 'collsite', 'sampletype', 'organism'] + ANTIMICROBIALS
    df = df[df.organism.isin(ORGANISMS) & df.sampletype.isin(COLLTYPES) & df.collsite.isin(SITES)][fields]
    tdf = df.groupby(['organism'])
    # tdf = tdf.apply(lambda _tdf: _tdf.sort_values(by=['testid']))
    # tdf = tdf[ANTIMICROBIALS]
    # # tdf = tdf.apply(pd.value_counts)
    abg = pd.DataFrame(index=ORGANISMS, columns=ANTIMICROBIALS)
    abg = abg.fillna('?')
    for amr in ANTIMICROBIALS:
        cdf = tdf[amr].value_counts().unstack(fill_value=0)
        for org in cdf.index.values:
            # print(amr, org)
            abg.at[org, amr] = getcdfat(cdf, org, 1) / (
                        getcdfat(cdf, org, 1) + getcdfat(cdf, org, 0) + getcdfat(cdf, org, 2))
    abg = abg.fillna('?')
    print(abg)
    tdf = tdf.apply(lambda _tdf: _tdf.sort_values(by=['testid']))
    return HttpResponse(abg)


def generate_anitbiogram(organisms, colltypes, sites, ams, startdate, enddate):
    df = getdatatable()
    df['date'] = pd.to_datetime(df['date'])
    fields = ['testid', 'collsite', 'sampletype', 'organism'] + ams
    df = df[df.organism.isin(organisms) & df.sampletype.isin(colltypes) & df.collsite.isin(sites) & (
            (df['date'] > startdate) & (df['date'] <= enddate))][fields]
    tdf = df.groupby(['organism'])
    # tdf = tdf.apply(lambda _tdf: _tdf.sort_values(by=['testid']))
    # tdf = tdf[ANTIMICROBIALS]
    # # tdf = tdf.apply(pd.value_counts)
    abg = pd.DataFrame(index=organisms, columns=ams)
    abg = abg.fillna('null')
    for amr in ams:
        cdf = tdf[amr].value_counts().unstack(fill_value=0)
        for org in cdf.index.values:
            # print(amr, org)
            try:
                abg.at[org, amr] = getcdfat(cdf, org, 1) / (
                    getcdfat(cdf, org, 1) + getcdfat(cdf, org, 0) + getcdfat(cdf, org, 2))*100.0
            except ZeroDivisionError:
                abg.at[org, amr] = 'null'
    abg = abg.fillna('null')
    tdf = tdf.apply(lambda _tdf: _tdf.sort_values(by=['testid']))
    return (abg)


def view_data(request):
    return render(request, 'dashboard/viewdata.html')


def getcdfat(cdf, a, b):
    try:
        return cdf.at[a, b]
    except KeyError:
        return 0
