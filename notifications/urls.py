from django.urls import path
from .views import *

app_name='notification'

urlpatterns = [ 
    path('change_notification/<int:id>',ChangeNotificationStatusView.as_view(), name= "change_notification"),
]