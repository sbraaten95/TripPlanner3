from __future__ import unicode_literals

from django.db import models
from ..login.models import User

# Create your models here.
class Trip(models.Model):
	planner = models.ForeignKey('login.User', models.DO_NOTHING, related_name="planner")
	destination = models.CharField(max_length=255)
	description = models.TextField()
	date_from = models.DateField()
	date_to = models.DateField()
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)

class Companion(models.Model):
	buddy = models.ForeignKey('login.User', models.DO_NOTHING, related_name="Companion")
	trip = models.ForeignKey('Trip', models.DO_NOTHING, related_name="Companion")
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)