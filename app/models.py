# yourapp/models.py
from django.db import models

class ContactForm(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField()
	phone = models.CharField(max_length=10,null=True) 
	message = models.TextField()

	def __str__(self):
		return self.name
	

	# count

	# models.py
from django.db import models

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    visit_time = models.DateTimeField(auto_now_add=True)

