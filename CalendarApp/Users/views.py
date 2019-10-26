from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # Package used to enable user authentication and the use of forms
from django.contrib import messages
import datetime
from datetime import timedelta
from Calendar.models import Summary, Event
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required

 # 403 Error view. Instead of showing a 403 text, it will redirect the user to his profile with a message that informs that he/she does not have permissions
def permission_denied(request, exception):
    messages.warning(request, f'You do not have permission to access the requested summary')
    return redirect('Calendar-profile')

def register(request):
    # When the user tries to sign up with a new account a request is created and is checked here
    if request.method == 'POST': 
        # Form created with the info inputted from the user(username, passwords)
        form = UserRegisterForm(request.POST )
        if form.is_valid():
            form.save()       
            messages.success(request, f'Your account has been created! You are able to log in now!')
            # Since the account was succesfully created, go to the log in page
            return redirect('Calendar-login')
    else: 
        # When we first go the register page there is no request to create a new account so the request.method != POST, so just create an empty form
        form = UserRegisterForm()
                                  
    return render(request, 'users/formBase.html', {'form': form, 'type': 'register'}) 

def getCurrentSummaries(User):
    today = datetime.datetime.today()
    endDate = today.isoformat() + 'Z' 
    # startDate will be 3 weeks before today
    startDate = (today - timedelta(days=21)).isoformat() + 'Z' 
    currentSummaries = Summary.objects.filter(user = User, startDate__range = (startDate, endDate))
    return list(currentSummaries)  

def getMostFrequentEvents(Summaries):
    UniqueEvents = {}
    #Identify all unique events and their duration times
    for Summary in Summaries:
        for event in Summary.events.all():
            if event.eventTitle not in UniqueEvents:
                UniqueEvents[event.eventTitle] = event.durationTime
            else:
                UniqueEvents[event.eventTitle] = UniqueEvents[event.eventTitle] + event.durationTime
    frequentEvents = []
  
    # Get the 5 most frequent events
    for i in range(0, 5):  
        frequentEvent = ("" , timedelta(days=0))
        for event in UniqueEvents:      
            if UniqueEvents[event] > frequentEvent[1]: 
                tempEventKey = event
                frequentEvent = (event, UniqueEvents[event])
        UniqueEvents.pop(tempEventKey)
        frequentEvents.append(frequentEvent)
    
    return frequentEvents

     
@login_required
def profile(request):
    currentSummaries = getCurrentSummaries(request.user)
    frequentEvents = getMostFrequentEvents(currentSummaries)

    # Note: Adding the instances parameters will populate the forms with the user's and profile's information respectively 
    if request.method == 'POST': 
         # Extansiate  user update form and pass in the new information from the forms
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if (u_form.is_valid()):
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('Calendar-profile')
    else:
        # Extansiate user update form with the user's current information
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form' : u_form,
        'frequentEvents' : frequentEvents,
    }
    return render(request, 'users/profile.html', context)

        