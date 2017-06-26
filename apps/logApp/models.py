from __future__ import unicode_literals

from django.db import models
import re
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg(self, firstName, lastName, email, password, passconfirm):
        
        errors = []
        if User.objects.filter(email = email):
            errors.append("Email already registered!!")
        if len(firstName) < 2:
            errors.append("First Name Too $hort")
        if len(lastName) < 2:
            errors.append("Last Name Too $hort")
        if not EMAIL_REGEX.match(email):
            errors.append("Email Not Valid")
        if len(password) < 8:
            errors.append("Password Too $hort")
        if len(password) != len(passconfirm):
            errors.append("Passwords Not Matching")

        if not errors:
            user = User.objects.create(firstName=firstName, lastName=lastName, email=email, password=password)
            return {"status":True, "data":user}
        else:
            return{"status":False, "data":errors}

    def login(self, email, password):
        errors = False
        user_list = User.objects.filter(email=email)

        if len(user_list) < 1:
            errors = True
        elif user_list[0].password != password:
            errors = True
        
        if not errors:
            return {"status":True, "data":user_list[0]}
        else:
            return{"status":False}

class User(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    passconfirm = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects=UserManager()