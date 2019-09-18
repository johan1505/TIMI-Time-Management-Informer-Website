from django.urls import path
from .views import UserSummariesListView, SummaryDetailView, SummaryDeleteView
from . import views
urlpatterns = [
    path('', views.home, name='Calendar-home'),
    path('Summaries/', UserSummariesListView.as_view(), name = "Calendar-User-Summaries"),
    path('Summary/<int:pk>', SummaryDetailView.as_view(), name = "Calendar-Summary-Detail"),
    path('Summary/<int:pk>/delete', SummaryDeleteView.as_view(), name = "Calendar-Summary-Delete"),
]