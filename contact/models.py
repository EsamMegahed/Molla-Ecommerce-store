from django.db import models

# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.message
