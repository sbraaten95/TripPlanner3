from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from ..login.models import User
from .models import Trip, Companion
import datetime

# Create your views here.
def dashboard(request):
	context = {
		'user': User.objects.get(username=request.session['user']),
		'trips': Trip.objects.all(),
		'companions': Companion.objects.all(),
		'owntrips': Trip.objects.all().filter(planner=User.objects.get(username=request.session['user'])),
		'othertrips': Trip.objects.all().exclude(planner=User.objects.get(username=request.session['user'])).exclude(Companion__buddy=User.objects.get(username=request.session['user']))
	}
	return render(request, 'trips/dashboard.html', context)

def add(request):
	return render(request, 'trips/add.html')

def submit(request):
	if len(request.POST['destination']) < 0:
		return render(request, 'trips/add.html', {'error': 'No empty values!'})
	if len(request.POST['description']) < 0:
		return render(request, 'trips/add.html', {'error': 'No empty values!'})
	if len(request.POST['from']) < 0:
		return render(request, 'trips/add.html', {'error': 'No empty values!'})
	if len(request.POST['to']) < 0:
		return render(request, 'trips/add.html', {'error': 'No empty values!'})

	try:
		fromDate = datetime.datetime.strptime(request.POST['from'], "%Y-%m-%d").strftime('%Y-%m-%d')
		toDate = datetime.datetime.strptime(request.POST['to'], "%Y-%m-%d").strftime('%Y-%m-%d')
	except ValueError:
		return render(request, 'trips/add.html', {'error': 'Incorrect date format!'})

	if datetime.datetime.strptime(fromDate, "%Y-%m-%d") < datetime.datetime.now():
		return render(request, 'trips/add.html', {'error': 'Future date required!'})
	if datetime.datetime.strptime(toDate, "%Y-%m-%d") < datetime.datetime.now():
		return render(request, 'trips/add.html', {'error': 'Future date required!'})

	if datetime.datetime.strptime(fromDate, "%Y-%m-%d") > datetime.datetime.strptime(toDate, "%Y-%m-%d"):
		return render(request, 'trips/add.html', {'error': 'From must be before To!'})

	Trip.objects.create(planner=User.objects.get(username=request.session['user']), destination=request.POST['destination'], description=request.POST['description'], date_from=fromDate, date_to=toDate)
	return redirect(reverse('trips:dashboard'))

def show(request, id):
	context = {
		'trip': Trip.objects.get(id=id),
		'users': User.objects.all(),
		'companions': Companion.objects.all()
	}

	return render(request, 'trips/show.html', context)

def join(request, id):
	Companion.objects.create(buddy=User.objects.get(username=request.session['user']), trip=Trip.objects.get(id=id))
	return redirect(reverse('trips:dashboard'))