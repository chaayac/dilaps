from django.shortcuts import render
from django.http import HttpResponse
from dilapjobs.models import job, logs
from django.utils import timezone
from django.db import connection
import geocoder
# Create your views here.
def index(request):
    
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

    if 'edit_job' in request.POST:
    
        #do some stuff -- pop up a modal to edit stuff?
        
        return render(request, 'home.html', {
            'jobs': job.objects.all().order_by('-status', '-timestamp'),
            'logs': logs.objects.all().order_by('-timestamp')
        })

    if 'delete_job' in request.POST:
        
        cursor = connection.cursor()

        cursor.execute("DELETE FROM dilapjobs_job WHERE jobnumber = %s", [request.POST['change']])
        
        return render(request, 'home.html', {
            'jobs': job.objects.all().order_by('-status', '-timestamp'),
            'logs': logs.objects.all().order_by('-timestamp')
        })

    if 'search_val' in request.POST:
        cursor = connection.cursor()
        query = "SELECT * FROM dilapjobs_job WHERE UPPER(jobnumber) LIKE \'%%%s%%\' OR UPPER(address) LIKE \'%%%s%%\' OR UPPER(notes) LIKE \'%%%s%%\' OR UPPER(letters) LIKE \'%%%s%%\' OR UPPER(neighbours) LIKE \'%%%s%%\' OR UPPER(councilassets) LIKE \'%%%s%%\' OR UPPER(client) LIKE \'%%%s%%\'" % (request.POST['search_val'].upper(), request.POST['search_val'].upper(), request.POST['search_val'].upper(), request.POST['search_val'].upper(), request.POST['search_val'].upper(), request.POST['search_val'].upper(), request.POST['search_val'].upper())
        cursor.execute(query)
        rows = cursor.fetchall()
        results = []
        for row in rows:
            d = {
                    'jobnumber': row[1],
                    'address': row[2],
                    'timestamp': row[3],
                    'client': row[4],
                    'councilassets': row[5],
                    'neighbours': row[6],
                    'notes': row[7],
                    'letters': row[8],
                    'latitude': row[9],
                    'latitude': row[10],
                    'longitude': row[11],
                    'postcode': row[12],
                    'status': row[13]
                }
            results.append(d)

        return render(request, 'home.html', {
            'jobs': results,
            'logs': logs.objects.all().order_by('-timestamp')
        })


    if 'createjob' in request.POST:
        
        locator = geocoder.google(request.POST['address'] + ", Australia")

        j = job(
            
            jobnumber=request.POST['jobnumber'], 
            address=request.POST['address'],
            timestamp=timezone.now(),
            client=request.POST['client'],
            notes=request.POST['notes'],
            councilassets=request.POST['councilassets'],
            neighbours=request.POST['neighbours'],
            letters=request.POST['letters'],
            latitude=locator.lat,
            longitude=locator.lng,
            postcode=locator.postal,
        )

        j.save()

    return render(request, 'home.html', {
            'jobs': job.objects.all().order_by('-status', '-timestamp'),
            'logs': logs.objects.all().order_by('-timestamp')
        })