from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User
import bcrypt

def index(request):
	return render(request, 'login/index.html')

def register(request):
	errors = User.objects.register(request)

	if len(errors) > 0:
		context = {
			'errors': errors
		}
		return render(request, 'login/index.html', context)

	else:
		password = request.POST['password'].encode()
		newpass = bcrypt.hashpw(password, bcrypt.gensalt())
		User.objects.create(name=request.POST['name'], username=request.POST['username'], password=newpass)
		request.session['user'] = request.POST['username']
		context = {
			'user': User.objects.get(username=request.session['user'])
		}
		return redirect(reverse('trips:dashboard'))

def login(request):
	errors = User.objects.login(request)

	if len(errors) > 0:
		context = {
			'errors': errors
		}
		return render(request, 'login/index.html', context)

	else:
		request.session['user'] = request.POST['username']
		context = {
			'user': User.objects.get(username=request.session['user'])
		}
		return redirect(reverse('trips:dashboard'))