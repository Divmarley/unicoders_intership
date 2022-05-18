 
from django.urls import path

from students.views import *  
app_name = 'student'
urlpatterns = [ 
    path('',StudentJobApplicationView.as_view(),name="job-application"),
    path('job-table',StudentJobApplicationTableView.as_view(),name="get-job-table"),
    path('<int:id>/delete', DeleteStudentJobApplication.as_view(), name='student-application-delete'),
    path("student-application-status-change", ChangeStudentApplicationStatus.as_view(), name="student-application-status-change"),
]  