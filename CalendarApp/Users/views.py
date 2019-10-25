from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # Package used to enable user authentication and the use of forms
from django.contrib import messages
import datetime
from datetime import timedelta
from Calendar.models import Summary, Event
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required

def permission_denied(request, exception): # 403 Error view. Instead of showing a 403 text, it will redirect the user to his profile with a message that informs that he/she does not have permissions
    messages.warning(request, f'You do not have permission to access the requested summary')
    return redirect('Calendar-profile')

def register(request):
    if request.method == 'POST': # When the user tries to sign up with a new account a request is created and is checked here 
        form = UserRegisterForm(request.POST )# Form created with the info inputted from the user( username, passwords )
        if form.is_valid(): # If valid then
            form.save() # Actually creates the user          
            messages.success(request, f'Your account has been created! You are able to log in now!')# Create a message
            return redirect('Calendar-login')# Since the account was succesfully created, go to the log in page
    else: 
        form = UserRegisterForm() # When we first go the register page there is no request to create a new account so the request.method != POST
                                  # so just create an empty form
    return render(request, 'users/formBase.html', {'form': form, 'type': 'register'}) # Render register.html and send the empty form previously created
                                                                  # Note: if the request.method == POST and a form with user info was created, but
                                                                  # the info was not valid, then this function will render and send that same form
                                                                  # to the .html file.(Once re-rendered, the previously user info inputted will appear

#def getCurrentSummaries(User):
 #   today = datetime.datetime.today()
  #  endDate = today.isoformat() + 'Z' 
   # beginDate = (today - timedelta(days=21)).isoformat() + 'Z' 
    #currentSummaries = Summary.objects.filter(user = User, startDate__range = (beginDate, endDate)) # Gets summaries from the past 3 week
    #return list(currentSummaries)  

#def getMostFrequentActivities(Summaries):
    #return the activities the user spet the most time on
 #   UniqueActivities = {}
  #  for Summary in Summaries: # Creates a hasTable of unique activities
   #     for activity in Summary.activities:
    #        if activity not in UniqueActivities:
     #           UniqueActivities[activity] = 0
    #print(UniqueActivities)

     
@login_required
def profile(request):
    # Note: Adding the instances parameters will populate the forms with the user's and profile's information respectively
    #currentSummaries = getCurrentSummaries(request.user)
    #getMostFrequentActivities(currentSummaries)

    if request.method == 'POST': # If the request is an update request submition
        u_form = UserUpdateForm(request.POST, instance=request.user) # Extansiate  user update form and pass in the new information from the forms
        if (u_form.is_valid()): # If both forms  are valid then save them, send a success message, and redirect the browser to the profile page
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('Calendar-profile')
    else: # If the request is not an update request submition
        u_form = UserUpdateForm(instance=request.user)# Extansiate user update form with the user's current information

    context = { # Insert forms in a context
        'u_form' : u_form,
       # 'currentSummaries' : currentSummaries,
    }
    return render(request, 'users/profile.html', context)

        