from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from dilapjobs.models import job, logs
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
import geocoder
# Create your views here.

def login_user(request):
    if 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'login.html', {
                    'res': "Not active",
                    'user': username,
                    'pass': password
                })
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {
                'res': "Wrong password/username",
                'user': username,
                'pass': password
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
                'jobs': job.objects.all().order_by('-status', '-timestamp'),
                'logs': logs.objects.all().order_by('-timestamp')
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
            'jobs': job.objects.all().order_by('-status', '-timestamp'),
            'logs': logs.objects.all().order_by('-timestamp')
        })

######################################################################
############################ EDIT JOB ##############################

    if 'finishedit' in request.POST:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM dilapjobs_job WHERE jobnumber = %s", [request.POST['old_jobnumber_e']])
        
        locator = geocoder.google(request.POST['address_e'] + ", Australia")

        neighbours = request.POST['neighbours_e']

        letters = request.POST['letters_e']
        string = letters
        # counter = 0
        # string = ""
        # for l in letters:
        #     string += l + ' '
        #     counter += 1
        #     if (counter % 6 == 0):
        #         string += ';'

        j = job(
            
            jobnumber=request.POST['jobnumber_e'], 
            address=request.POST['address_e'],
            timestamp=timezone.now(),
            client=request.POST['client_e'],
            notes=request.POST['notes_e'],
            councilassets=request.POST['councilassets_e'],
            neighbours=neighbours,
            letters=string,
            latitude=locator.lat,
            longitude=locator.lng,
            postcode=locator.postal,
        )

        j.save()

        return render(request, 'home.html', {
            'jobs': job.objects.all().order_by('-status', '-timestamp'),
            'logs': logs.objects.all().order_by('-timestamp')
        })

######################################################################
############################ DELETE JOB ##############################

    if 'delete_job' in request.POST:
        
        cursor = connection.cursor()

        cursor.execute("DELETE FROM dilapjobs_job WHERE jobnumber = %s", [request.POST['change']])
        
        return render(request, 'home.html', {
            'jobs': job.objects.all().order_by('-status', '-timestamp'),
            'logs': logs.objects.all().order_by('-timestamp')
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
            'logs': logs.objects.all().order_by('-timestamp')
        })

######################################################################
############################ CREATE JOB ##############################

    if 'createjob' in request.POST:
        
        locator = geocoder.google(request.POST['address'] + ", Australia")
        
        neighbours = request.POST.getlist('neighbours[]')
        neighbours = ';'.join(neighbours)

        letters = request.POST.getlist('letters[]')
        counter = 0
        string = ""
        for l in letters:
            string += l + ' '
            counter += 1
            if (counter % 6 == 0):
                string += ';'

        j = job(
            
            jobnumber=request.POST['jobnumber'], 
            address=request.POST['address'],
            timestamp=timezone.now(),
            client=request.POST['client'],
            notes=request.POST['notes'],
            councilassets=request.POST['councilassets'],
            neighbours=neighbours,
            letters=string,
            latitude=locator.lat,
            longitude=locator.lng,
            postcode=locator.postal,
        )

        j.save()

    return render(request, 'home.html', {
            'jobs': job.objects.all().order_by('-status', '-timestamp'),
            'logs': logs.objects.all().order_by('-timestamp')
        })
######################################################################
