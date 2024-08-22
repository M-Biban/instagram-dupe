from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, blank=False,
                                validators=[RegexValidator(
                                    regex=r'^[a-zA-Z0-9_-]+$',
                                    message= 'Username must only include alphanumericals, "-" and "_" .')])
    first_name = models.CharField(max_length=50, blank=False,
                                validators=[RegexValidator(
                                    regex=r'^[a-zA-Z]+$',
                                    message = 'Please enter a valid first name'
                                )]
                                  )
    last_name = models.CharField(max_length=50, blank=False,
                                 validators=[RegexValidator(
                                    regex=r'^[a-zA-Z]+$',
                                    message = 'Please enter a valid last name'
                                )])
    email = models.EmailField(unique=True, blank=False)
    friends = models.ManyToManyField("User", blank=True)
    
    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']
        