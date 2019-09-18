from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from .models import Summary
from django.contrib.auth.models import User

def home(request):
    return render(request, 'Calendar\home.html')

#Using a Class view. This class inherits from the class ListView
#THIS SHOULD BE GOOD TO GO....
class UserSummariesListView(ListView):
    model = Summary
    template_name = 'Calendar/user_summaries.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'summaries'
   # ordering = ['-date_posted'] # Order posts from newest to oldest
   # paginate_by = 5 # Will make the home page only display two post per page
    def get_queryset(self):
      #  user = get_object_or_404(User, username=self.kwargs.get('username')) # Get an user that matches the  username passed in by the URL
        return Summary.objects.filter(user=self.request.user).order_by('-startDate') # Filter the query to only get the posts with author = current user


class SummaryDetailView(DetailView):
    model = Summary
    template_name = 'Calendar/summary_detail.html'

class SummaryDeleteView(DeleteView):
    model = Summary
    success_url = "/"