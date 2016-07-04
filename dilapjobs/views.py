from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from dilapjobs.models import job, logs
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.core.mail import EmailMessage
import geocoder
import string, re, json
import datetime
# Create your views here.

def login_user(request):
    if 'login' not in request.POST:
        return render(request, 'login.html')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'login.html', {
                    'res': "Your account is disabled.",
                })
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {
                'res': "Wrong password/username",
                })
    else:
        return render(request, 'login.html')


@login_required
def index(request):
############################ LOG OUT USER ###############################
    if 'logout' in request.POST:
        logout(request)
        return render(request, 'login.html')
#####################################################################

############################ ADD LOG ###############################
    if 'add_log' in request.POST:
        l = logs(
        
            logtext=request.POST['logtext'],
            timestamp=timezone.now()
        )

        l.save()

        return render(request, 'home.html', {
                'incomplete_jobs': job.objects.all().filter(status = 'Incomplete').order_by('-status', '-created'),
                'complete_jobs': job.objects.all().filter(status = 'Complete').order_by('-status', '-timestamp'),
                'logs': logs.objects.all().order_by('-timestamp'),
                'outdated': getOutdatedLetters()
            })
######################################################################
############################ COMPLETE JOB ##############################

    if 'complete_job' in request.POST:
        cursor = connection.cursor()

        cursor.execute("UPDATE dilapjobs_job SET timestamp = %s WHERE jobnumber = %s", [timezone.now(), request.POST['change']])

        cursor.execute("SELECT * FROM dilapjobs_job WHERE jobnumber = %s", [request.POST['change']])
        rows = cursor.fetchall()
        
        for row in rows:
            if row[13] == 'Complete':
                cursor.execute("UPDATE dilapjobs_job SET status = 'Incomplete' WHERE jobnumber = %s", [request.POST['change']])
            else:
                cursor.execute("UPDATE dilapjobs_job SET status = 'Complete' WHERE jobnumber = %s", [request.POST['change']])            
        
        return render(request, 'home.html', {
            'incomplete_jobs': job.objects.all().filter(status = 'Incomplete').order_by('-status', '-created'),
            'complete_jobs': job.objects.all().filter(status = 'Complete').order_by('-status', '-timestamp'),
            'logs': logs.objects.all().order_by('-timestamp'),
            'outdated': getOutdatedLetters()
        })

######################################################################
############################ EDIT JOB ##############################

    if 'old_jobnumber_e' in request.POST:

        old_jobnumber = request.POST['old_jobnumber_e']
        
        jobnumber = request.POST['jobnumber_e'].replace(" ", "")

        # get all jobs with number = edited number, and exclude all in that list where number = old job number (should be 0 if old=new, 
        # else 0 if no duplicates and 1 if there is a duplicate)
        num_results = job.objects.filter(jobnumber__iexact = jobnumber).exclude(jobnumber__iexact = old_jobnumber).count()

        if (num_results != 0):
            return render(request, 'home.html', {
                'incomplete_jobs': job.objects.all().filter(status = 'Incomplete').order_by('-status', '-created'),
                'complete_jobs': job.objects.all().filter(status = 'Complete').order_by('-status', '-timestamp'),
                'logs': logs.objects.all().order_by('-created'),
                'error': "This job already exists. Try again with a different job number.",
                'outdated': getOutdatedLetters()
                })

        locator = geocoder.google(request.POST['address_e'] + ", Australia")

        councilassets = request.POST.getlist('councilassets_e[]')
        council = '|'.join(councilassets)

        neighbours = request.POST.getlist('neighbours_e[]')
        n_string = '|'.join(neighbours)

        letters = request.POST.getlist('letters_e[]')
        counter = 0
        stringb = ""
        for l in letters:
            stringb += l + ' '
            counter += 1
            if (counter % 6 == 0):
                stringb += '|'

        stringb = stringb[:-1]

        j = job.objects.get(jobnumber__iexact = old_jobnumber)

        j.jobnumber=jobnumber
        j.address=string.capwords(request.POST['address_e'])
        j.timestamp=timezone.now()
        j.client=string.capwords(request.POST['client_e'])
        j.notes=request.user.first_name + '|' + request.POST['notes_e']
        j.councilassets=string.capwords(council)
        j.neighbours=string.capwords(n_string)
        j.letters=stringb
        j.latitude=locator.lat
        j.longitude=locator.lng
        j.postcode=locator.postal
        j.save()

        return render(request, 'home.html', {
            'incomplete_jobs': job.objects.all().filter(status = 'Incomplete').order_by('-status', '-created'),
            'complete_jobs': job.objects.all().filter(status = 'Complete').order_by('-status', '-timestamp'),
            'logs': logs.objects.all().order_by('-timestamp'),
            'outdated': getOutdatedLetters()
        })

######################################################################
############################ DELETE JOB ##############################

    if 'delete_job' in request.POST:
        
        cursor = connection.cursor()

        cursor.execute("DELETE FROM dilapjobs_job WHERE jobnumber = %s", [request.POST['change']])
        
        return render(request, 'home.html', {
            'incomplete_jobs': job.objects.all().filter(status = 'Incomplete').order_by('-status', '-created'),
            'complete_jobs': job.objects.all().filter(status = 'Complete').order_by('-status', '-timestamp'),
            'logs': logs.objects.all().order_by('-timestamp'),
            'outdated': getOutdatedLetters()
        })
######################################################################
############################ SEARCH JOB ##############################

    if 'search_val' in request.POST:
        cursor = connection.cursor()
        org_term = request.POST['search_val']
        term = '%' + org_term + '%'
        term = term.upper()
        results = job.objects.raw("SELECT * FROM dilapjobs_job WHERE UPPER(jobnumber) LIKE %s OR UPPER(address) LIKE %s OR UPPER(notes) LIKE %s OR UPPER(letters) LIKE %s OR UPPER(neighbours) LIKE %s OR UPPER(councilassets) LIKE %s OR UPPER(client) LIKE %s", [term, term, term, term, term, term, term])

        return render(request, 'home.html', {
            'search': org_term,
            'jobs': results,
            'logs': logs.objects.all().order_by('-timestamp'),
            'outdated': getOutdatedLetters()
        })

######################################################################
############################ CREATE JOB ##############################

    if 'jobnumber' in request.POST:
        
        num_results = job.objects.filter(jobnumber__iexact = request.POST['jobnumber']).count()
        jobnumber = request.POST['jobnumber'].replace(" ", "")
        if (num_results != 0):
            return render(request, 'home.html', {
                'incomplete_jobs': job.objects.all().filter(status = 'Incomplete').order_by('-status', '-created'),
                'complete_jobs': job.objects.all().filter(status = 'Complete').order_by('-status', '-timestamp'),
                'logs': logs.objects.all().order_by('-timestamp'),
                'error': "This job already exists. Try again with a different job number.",
                'outdated': getOutdatedLetters()
                })
       
        locator = geocoder.google(request.POST['address'] + ", Australia")
        
        councilassets = request.POST.getlist('councilassets[]')
        council = '|'.join(councilassets)

        neighbours = request.POST.getlist('neighbours[]')
        neighbours = '|'.join(neighbours)

        letters = request.POST.getlist('letters[]')
        counter = 0
        stringb = ""
        for l in letters:
            stringb += l + ' '
            counter += 1
            if (counter % 6 == 0):
                stringb += '|'

        stringb = stringb[:-1]

        j = job(

            jobnumber=jobnumber, 
            address=string.capwords(request.POST['address']),
            timestamp=timezone.now(),
            client=string.capwords(request.POST['client']),
            notes=request.user.first_name + '|' + request.POST['notes'],
            councilassets=string.capwords(council),
            neighbours=string.capwords(neighbours),
            letters=stringb,
            latitude=locator.lat,
            longitude=locator.lng,
            postcode=locator.postal,
            created=timezone.now()
        )

        j.save()

    # else
    return render(request, 'home.html', {
            'incomplete_jobs': job.objects.all().filter(status = 'Incomplete').order_by('-status', '-created'),
            'complete_jobs': job.objects.all().filter(status = 'Complete').order_by('-status', '-timestamp'),
            'logs': logs.objects.all().order_by('-timestamp'),
            'outdated': getOutdatedLetters()
        })
######################################################################

def getOutdatedLetters():
    outdated = []
    format = re.compile('(\d+/\d+/\d+)')
    today = datetime.datetime.now()
    jobs = job.objects.all()
    for j in jobs:
        if j.status != 'Complete':
            neighbour_counter = 0
            letters_per_neighbour = j.letters.split('|')
            if '(done)' not in j.neighbours.split('|')[neighbour_counter]:
                for l in letters_per_neighbour:
                    if 'replied' not in l:
                        letter_dates = format.findall(l)
                        if len(letter_dates) == 1:
                            day_month_year = letter_dates[0]
                            date = datetime.datetime.strptime(day_month_year, '%d/%m/%Y')
                            if date + datetime.timedelta(days=14) < today:
                                outdated.append({
                                    'jobnumber': j.jobnumber,
                                    'neighbour': j.neighbours.split('|')[neighbour_counter],
                                    'letter': 2
                                    })
                        elif len(letter_dates) == 2:
                            day_month_year = letter_dates[1]
                            date = datetime.datetime.strptime(day_month_year, '%d/%m/%Y')
                            if date + datetime.timedelta(days=10) < today:
                                outdated.append({
                                    'jobnumber': j.jobnumber,
                                    'neighbour': j.neighbours.split('|')[neighbour_counter],
                                    'letter': 3
                                    })
                    neighbour_counter += 1
    return outdated

def getJobs(request):
    id = request.GET.get('id', '')
    
    if id == '':
        jobs = job.objects.all()
    else:
        jobs = job.objects.all().filter(jobnumber=id)
    
    toreturn = []
    for j in jobs:
        if j.status != 'Complete':
            l=[]
            for i in j.letters.split('|'):
                arr = i.split(" ") # looks like [date, type, date, type, date, type, '']
                del arr[-1]
                l.append(arr)

            j = {
                'letters': l,
                'councilassets': [string.capwords(i) for i in j.councilassets.split('|')], ##
                'jobnumber': j.jobnumber, 
                'address': string.capwords(j.address),
                'timestamp': (j.timestamp),
                'client': string.capwords(j.client),
                'notes': request.user.first_name + '|' + j.notes,
                'neighbours': [string.capwords(i) for i in j.neighbours.split('|')], ##
                'latitude': j.latitude,
                'longitude': j.longitude,
                'postcode': j.postcode,
            }
            
            toreturn.append(j)
    response = JsonResponse(toreturn, safe=False)
    return response
