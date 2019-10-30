# Django
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings

from .forms import *
# Models
from .models import *
from .scripts.biotable import *
from .scripts.googlelogin import *
from .scripts.viewmethods import *
from .scripts.bokeh import *

from bokeh.embed import components
import pandas as pd
import pandas_bokeh


# Python

# Create your views here.


# Add Google API Keys for Google login
GOOGLE_API_APP_ID = '110416131256-56k6c0uh1pap9fn4f92f4m0mffkeb6ge.apps.googleusercontent.com'
GOOGLE_API_APP_SECRET = '02aelsX-ew-_15ZJt7cR7G8b'

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
    return HttpResponseRedirect(REDIRECT_URL)


def active(request):
    input_form = False
    created = True
    table = False
    json = False
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
                table = generate_anitbiogram(ams=input_form.cleaned_data['ams'],
                                             organisms=input_form.cleaned_data['org'],
                                             colltypes=input_form.cleaned_data['col'],
                                             sites=input_form.cleaned_data['site'],
                                             startdate=input_form.cleaned_data['startdate'],
                                             enddate=input_form.cleaned_data['enddate'])
                # print(table)
                table.to_csv('data.csv')
                json = table.to_json(orient="split")
                tablehtml = table.to_html()
                # json = table.to_json(orient="split")
                csv = pd.read_csv("bargraph.csv").to_json(orient='records')
                return render(request, 'dashboard/active2.html',
                              {'form': input_form, 'registered': created, 'table': tablehtml, 'json': json, 'csv': csv})

            else:
                print(input_form.errors)
        else:
            input_form = InputDataForm()
            input_form.fields['ams'].choices = [(x, x) for x in ANTIMICROBIALS]
            input_form.fields['site'].choices = [(x, x) for x in SITES]
            input_form.fields['col'].choices = [(x, x) for x in COLLTYPES]
            input_form.fields['org'].choices = [(x, x) for x in ORGANISMS]

    return render(request, 'dashboard/active.html',
                  {'form': input_form, 'registered': created, 'table': table, 'json': json})


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


def exploraotry_analysis(request):
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
        tsv = False
        table = False
        if request.GET.items():
            user = User.objects.get(username=request.user.username)
        if request.method == 'POST':
            input_form = InputDataForm(data=request.POST)
            input_form.fields['ams'].choices = [(x, x) for x in ANTIMICROBIALS]
            input_form.fields['org'].choices = [(x, x) for x in ORGANISMS]
            if input_form.is_valid():
                if not input_form.cleaned_data['ams']:
                    input_form.cleaned_data['ams'] = ANTIMICROBIALS
                if not input_form.cleaned_data['org']:
                    input_form.cleaned_data['org'] = ORGANISMS
                print(input_form.cleaned_data['ams'])
                print(input_form.cleaned_data['org'])
                graph = generate_graph(organisms=input_form.cleaned_data['org'], ams=input_form.cleaned_data['ams'], )
                print(graph)
                print(settings.FILE_DIR)
                graph.to_csv(settings.FILE_DIR+'/linegraph.tsv', sep='\t')
                table = graph.to_html()
                json = graph.to_json(orient='records',date_format='iso')
                return render(request, 'dashboard/explore2.html',
                              {'form': input_form, 'registered': created, 'table':table, 'json': json})

            else:
                print(input_form.errors)
        else:
            input_form = InputDataForm()
            input_form.fields['ams'].choices = [(x, x) for x in ANTIMICROBIALS]
            input_form.fields['site'].choices = [(x, x) for x in SITES]
            input_form.fields['col'].choices = [(x, x) for x in COLLTYPES]
            input_form.fields['org'].choices = [(x, x) for x in ORGANISMS]

        return render(request, 'dashboard/explore.html',
                      {'form': input_form, 'registered': created, 'table': table})


def view_data(request):
    return render(request, 'dashboard/viewdata.html')



def bokeh(request):
    input_form = False
    created = True
    table = False
    json = False
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
                dfr,dfs,dfi = get_rsi(ams=input_form.cleaned_data['ams'],
                                             organisms=input_form.cleaned_data['org'],
                                             colltypes=input_form.cleaned_data['col'],
                                             sites=input_form.cleaned_data['site'],
                                             startdate=input_form.cleaned_data['startdate'],
                                             enddate=input_form.cleaned_data['enddate'])

                # create a new plot
                dft = dfi + dfr + dfs
                dff = dfs / (dft) * 100
                dff = dff.replace(np.nan, 'Data Not Available')


                dfb = dff[' All Antimicrobials']

                hmap = heatmap(dff,dft, s_z="Sensivity")

                pie2 = dfs.copy()
                pie1 = pie2.transpose()
                pie1 = pie1.drop(' All Antimicrobials')
                pie2 = pie2.drop(' All Organisms')
                pie1.to_csv('pie1.csv')
                pie1 = pd.read_csv('pie1.csv')
                p1 = pie1.plot_bokeh.pie(
                            x="antimicrobials",
                            # y=" All Antimicrobials",
                            title="Organisms vs Sensitive Drugs",
                            show_figure=False,
                            # return_html=True,
                            figsize=(1200,800),
                            zooming = True,
                        )

                pie2.to_csv('pie2.csv')
                pie2 = pd.read_csv('pie2.csv')
                p2 = pie2.plot_bokeh.pie(
                    x="organism",
                    # y=" All Antimicrobials",
                    title="Drugs vs Organisms",
                    show_figure=False,
                    # return_html=True,
                    figsize=(1200, 800),
                    zooming=True,
                )

                script1, div1 = components(hmap)
                script2, div2 = components(p1)
                script3, div3 = components(p2)

                return render(request, 'dashboard/bokeh.html',
                              {'table': div1+'</br>'+div2+'</br>'+div3, 'script': script1+script2+script3})

            else:
                print(input_form.errors)
        else:
            input_form = InputDataForm()
            input_form.fields['ams'].choices = [(x, x) for x in ANTIMICROBIALS]
            input_form.fields['site'].choices = [(x, x) for x in SITES]
            input_form.fields['col'].choices = [(x, x) for x in COLLTYPES]
            input_form.fields['org'].choices = [(x, x) for x in ORGANISMS]

    return render(request, 'dashboard/active.html',
                  {'form': input_form, 'registered': created, 'table': table, 'json': json})

def getcdfat(cdf, a, b):
    try:
        return cdf.at[a, b]
    except KeyError:
        return 0

def rcount(series):
    print(series)
    return (series.values == 1).sum()

def ml_analysis(request):
    return HttpResponse('<h1>wiseR access is locked for this user</h1><h2>For more details about wiseR visit <a href="https://github.com/SAFE-ICU/wiseR/">wiseR github</a>')

