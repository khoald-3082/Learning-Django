from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	email = models.EmailField(max_length=256, unique=True)
	username = models.CharField(max_length=256, unique=True)
	password = models.CharField(max_length=256)
	first_name = models.CharField(max_length=256, blank=True)
	last_name = models.CharField(max_length=256, blank=True)
	is_staff = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.first_name} {self.last_name}"
