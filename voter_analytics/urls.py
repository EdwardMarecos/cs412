#  voter_analytics/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter_detail'),
    path('graphs/', VoterGraphsView.as_view(), name='graphs'),

]