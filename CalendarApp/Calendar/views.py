import datetime
import httplib2
import json
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, DeleteView, View
from .models import Event, Summary
from django.contrib.auth.models import User
from datetime import timedelta, date


def home(request):
    return render(request, 'Calendar\home.html')

# Helper function
def setTimes():
    todaysWeekDay = datetime.datetime.today().weekday() # Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
    today = datetime.datetime.utcnow()
    startDate = None
    endDate = None
    if (todaysWeekDay == 0):   # Monday
        startDate = today - timedelta(days=1)
        endDate = today + timedelta(days=5)
    elif (todaysWeekDay == 1): # Tuesday
        startDate = today - timedelta(days=2)
        endDate = today + timedelta(days=4)
    elif (todaysWeekDay == 2): # Wednesday
        startDate = today - timedelta(days=3)
        endDate = today + timedelta(days=3)
    elif (todaysWeekDay == 3): # Thursday
        startDate = today - timedelta(days=4)
        endDate = today + timedelta(days=2)
    elif (todaysWeekDay == 4): # Friday
        startDate = today - timedelta(days=5)
        endDate = today + timedelta(days=1)
    elif (todaysWeekDay == 5): # Saturday
        startDate = today - timedelta(days=6)
        endDate = today
    else:                      # Sunday
        startDate = today
        endDate = today + timedelta(days=6)

    # Make both startDate and endDate begin from 0 times
    #startDate = datetime.datetime.combine(startDate, startDate.min.time()) 
    #endDate = datetime.datetime.combine(endDate, endDate.max.time())
    # Stores the nearest Monday from today
    startDate = startDate.isoformat() + 'Z'
    endDate = endDate.isoformat() + 'Z'
    # Stores the nearest Sunday from today
    return (startDate, endDate)
    
class BuildFlow:
    def __init__(self):        
        self.flow = OAuth2WebServerFlow(settings.CLIENT_ID,                
                                        settings.CLIENT_SECRET,
                                        scope='https://www.googleapis.com/auth/calendar.readonly',
                                        redirect_uri=settings.REDIRECT_URI)

#Note: 
#The step1_get_authroize_url() here is an internal method of OAuth2WebServerFlow which generates the url based on scope,client_id and client secret.
class OAuth(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Build the flow
        build_flow = BuildFlow()   
        # Get the authorization url                               
        generated_url = build_flow.flow.step1_get_authorize_url() 
        # Redirect the user to the authorization url
        return HttpResponseRedirect(generated_url)                

# Note:
# A Credentials object holds refresh and access tokens that authorize access to a single user's data. 
# These objects are applied to httplib2.Http objects to authorize access. They only need to be applied once and can be stored. 
# THIS VIEW SHOULD ONLY GET REQUESTS!
class OAuth2CallBack(View):
    def get(self, request, *args, **kwargs):
        # Get the code 
        code = request.GET.get('code', False)
        # If there is no code then the user most likely declined permission
        if not code:
            messages.warning(request, f'CalendarCalc was denied access to your Google calendars')
            return redirect('Calendar-User-Summaries')
        # Build a flow
        oauth2 = BuildFlow()
        # Exchanges a code for OAuth2Credentials. Returns An OAuth2Credentials object that can be used to authorize requests.
        credentials = oauth2.flow.step2_exchange(code)
        http = httplib2.Http()
        # Authorize credentials
        http = credentials.authorize(http)          
        # Creates a json file from the credentials
        credentials_js = json.loads(credentials.to_json())
         # Store the access token in case we need it again!
        access_token = credentials_js['access_token']     
        request.session['access_token'] = access_token
        # Create a service TO USE GOOGLE CALENDAR API calls
        service = build('calendar', 'v3', credentials=credentials)
        times = setTimes()
        startDate = times[0] # Closest Monday 
        endDate = times[1]   # Closest Sunday
        # create an event result with timeMin and timeMax
        #PROBLEM: RETURNS A LIST OF EVENTS THAT IS NOT ACCURATE.
        events_result = service.events().list(calendarId='primary', timeMin=startDate, timeMax=endDate, singleEvents=True, orderBy='startTime').execute() 
        # events is a list of dictionaries. Each dictionary contains information of an event
        events = events_result.get('items', [])    
        # Creates an empty summary for the current user logged in
        userSummary = Summary(user = self.request.user, startDate = startDate, endDate = endDate)
        # HashTable for events found
        eventsFound = {}                                 

        if not events:
            messages.warning(request, f'The Google account provided has no calendars for this week!')
            return redirect('Calendar-User-Summaries')
        else :
            for event in events: 
                startTime = datetime.datetime.strptime(event['start'].get('dateTime'), '%Y-%m-%dT%H:%M:%S%z')
                endTime = datetime.datetime.strptime(event['end'].get('dateTime'), '%Y-%m-%dT%H:%M:%S%z')
                timeSpentInEvent = endTime - startTime    
                if event['summary'] in eventsFound:
                    # Add the time of the evend already found
                    eventsFound[event['summary']] = eventsFound[event['summary']] + timeSpentInEvent 
                else :     
                    # Gets how long the event lasts = set it equal to the time the event lasted
                    eventsFound[event['summary']] = timeSpentInEvent 

            userSummary.save()
            for event in eventsFound:                  
                currentEvent = Event(eventTitle = event, durationTime = eventsFound[event])
                currentEvent.save()
                userSummary.events.add(currentEvent)
            userSummary.save() 
            events = userSummary.events.all()
        return HttpResponseRedirect(reverse('Calendar-User-Summaries'))

class UserSummariesListView(LoginRequiredMixin, ListView):
    model = Summary
    template_name = 'Calendar/user_summaries.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'summaries'
   # ordering = ['-date_posted'] # Order posts from newest to oldest
   # paginate_by = 5 # Will make the home page only display two post per page
    def get_queryset(self):
      # user = get_object_or_404(User, username=self.kwargs.get('username')) # Get an user that matches the  username passed in by the URL
        return Summary.objects.filter(user=self.request.user).order_by('-startDate') # Filter the query to only get the posts with author = current user

class SummaryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Summary
    template_name = 'Calendar/summary_detail.html'
    def test_func(self):  
        # Get the summary that is being accessed       
        summary = self.get_object() 
        # If the current user is the creater of the summary then allow him/her to have access to
        if self.request.user == summary.user: 
            return True
        return False
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['events'] = self.get_object().events.all().order_by('-durationTime')
        return context

class SummaryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Summary
    success_url = "/Summaries"
    def test_func(self):       
        # Get the summary that is being deleted     
        summary = self.get_object()
        # If the current user is the creater of the summary then allow him/her to delete it
        if self.request.user == summary.user:
            return True
        return False

