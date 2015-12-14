from django.shortcuts import render
from django.http import HttpResponse
from dilapjobs.models import job
from django.utils import timezone
from django.db import connection
import geocoder
# Create your views here.
def index(request):
    
    if 'delete_job' in request.POST:
        
        cursor = connection.cursor()

        cursor.execute("DELETE FROM dilapjobs_job WHERE jobnumber = %s", [request.POST['delete']])
        
        return render(request, 'home.html', {
            'jobs': job.objects.all().order_by('-timestamp')
        })

    if 'search_val' in request.POST:
        cursor = connection.cursor()
        query = "SELECT * FROM dilapjobs_job WHERE jobnumber LIKE \'%%%s%%\' OR address LIKE \'%%%s%%\' OR notes LIKE \'%%%s%%\' OR letters LIKE \'%%%s%%\' OR neighbours LIKE \'%%%s%%\' OR councilassets LIKE \'%%%s%%\' OR client LIKE \'%%%s%%\'" % (request.POST['search_val'], request.POST['search_val'], request.POST['search_val'], request.POST['search_val'], request.POST['search_val'], request.POST['search_val'], request.POST['search_val'])
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
                    'postcode': row[12]
                }
            results.append(d)

        return render(request, 'home.html', {
            'jobs': results
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
        'jobs': job.objects.all().order_by('-timestamp')
        })