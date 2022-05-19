from django.urls import path
from .views import *

app_name = 'job'

urlpatterns = [ 
    path('',JobListView.as_view(),name="index")
 ]