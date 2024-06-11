# yourapp/models.py
from django.db import models

class ContactForm(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField()
	phone = models.CharField(max_length=10,null=True) 
	message = models.TextField()

	def __str__(self):
		return self.name

# models.py
from django.db import models

class Donation(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    payment_id = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Donation of {self.amount} by {self.name}"
