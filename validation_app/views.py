from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# render functions
def index(request):
    return render(request, 'form.html')

def success(request, user_id):
    context = {
        "user": User.objects.get(id=user_id),
        "all_users": User.objects.all()
    }
    return render(request, "success.html", context)

# process functions
def process_form(request):
    # This will set the variable 'errors' to the dict returned from the validator function
    errors = User.objects.validator(request.POST)
    # Check if dict 'errors' is empty
    if len(errors) > 0:
        # Go through dict 'errors' and add custom error messages to the messages.error to display on front end
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        # There are errors! Redirect back to the front page!
        return redirect('/')
    # If the dict is empty, there are no errors! Create a new user!
    else:
        user = User.objects.create(username = request.POST['username'], 
                                email = request.POST['email'],
                                birthday = request.POST['birthday'],
                                favorite_num = request.POST['favorite_num'])
    return redirect(f'/success/{user.id}')

