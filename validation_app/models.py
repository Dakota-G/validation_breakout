from django.db import models
import re, datetime, time

# Create your models here.
class User_Manager(models.Manager):
    def validator(self, POSTdata):
        # Set up a regular expression for emails. Although the front end form does something similar, it is easy for someone to work around
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # Grab today's date and format it for comparison 
        today = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
        # Empty errors dict to collect error messages
        errors = {}
        # Check if username is unique by checking it against Users already in DB
        # Check that a username was actually entered into form
        # Check that username is more than 3 characters
        # Check that username is less than 25 characters
        users = User.objects.filter(username = POSTdata['username'])
        if len(POSTdata['username']) == 0:
            errors['username'] = "You need a username!"
        elif len(POSTdata['username']) < 3:
            errors['username'] = "Your username needs to be more than 2 characters long!"
        elif len(POSTdata['username']) > 25:
            errors['username'] = "Your username needs to be shorter than 25 characters!"      
        elif len(users) > 0:
            errors['username'] = "That username already exists!"

        # Check that email was provided
        # Check email from form against RegEx
        if len(POSTdata['email']) == 0:
            errors['email'] = "How am I supposed to SPAM you without an email?!"
        elif not email_regex.match(POSTdata['email']):
            errors['email'] = "That's not a real email! Did you mess with my form?!"
        
        # Check that a birthdate was provided
        # Check that the birthday is in the past
        # Subtract birthday from today's date and see if the result is less than 18 years (including leap years)
        if len(POSTdata['birthday']) == 0:
            errors['birthday'] = "No birthday? Were you hatched or grown in a lab?"
        birthday = datetime.datetime.strptime(str(POSTdata['birthday']), "%Y-%m-%d")
        timedelta = today - birthday
        if birthday > today: 
            errors['date'] = "Your birthday cannot be in the future? Unless you're a time traveller..."
        elif timedelta.days/365.25 < 18:
            errors['date'] = "You, sir, are a child!"
        
        # Check that a number was provided in form
        # Check that the number is between 1 and 100
        if len(POSTdata['favorite_num']) == 0:
            errors['favorite_num'] = "We need a number!"
        elif int(POSTdata['favorite_num']) < 1 or int(POSTdata['favorite_num']) > 100:
            errors['favorite_num'] = "Can't you read the form? LESS than zero! BIGGER than one hundred!"
        # return the dictionary to the views.process
        return errors

class User(models.Model):
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    birthday = models.DateField()
    favorite_num = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = User_Manager()


