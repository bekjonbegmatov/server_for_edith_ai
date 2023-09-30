from django.db import models

# Create your models here.

class User(models.Model):

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField( max_length=50)

    is_email_auth = models.BooleanField(default=False)
    email_code = models.CharField(max_length=50 , blank=True)

    def __str__(self):
        return self.username

 