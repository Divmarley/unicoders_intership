from django.urls import path
from .views import *

app_name = 'staff'

urlpatterns = [
    path('students', AdminListStudentJobApplicationView.as_view(),name ='student-jp-index'), 
    path("students-table", AdminListStudentJobApplicationTableView.as_view(), name="get-jp-table"),


    path('employer', EmployerJobApplicationStaffView.as_view(),name ='employer-jp-index'), 
    path("employers-table", EmployerJobApplicationStaffTableView.as_view(), name="get-employer-jp-table"),

 ]