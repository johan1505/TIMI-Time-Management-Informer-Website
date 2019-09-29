from django.urls import path
from .views import UserSummariesListView, SummaryDetailView, SummaryDeleteView, OAuth, OAuth2CallBack
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home, name='Calendar-home'),
    path('Summaries/', UserSummariesListView.as_view(), name = "Calendar-User-Summaries"),
    path('Summary/<int:pk>', SummaryDetailView.as_view(), name = "Calendar-Summary-Detail"),
    path('Summary/<int:pk>/delete', SummaryDeleteView.as_view(), name = "Calendar-Summary-Delete"),
    path('Summary/new/', csrf_exempt(OAuth.as_view()), name='Calendar-Summary-New'),
    path('Summary/new/callback/', OAuth2CallBack.as_view(), name='Calendar-Summary-New-Callback'),
]