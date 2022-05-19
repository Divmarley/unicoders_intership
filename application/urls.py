from django.urls import path
from .views import *

app_name = 'application'

urlpatterns = [
    
    # path('', StudentJobApplicationView.as_view(), name='student-job-application'),
    # path("student-job-application-table", StudentJobApplicationTableView.as_view(), name="get-student-job-application-table"),
    # path("delete/student-job-application/<int:id>", DeleteStudentJobApplication.as_view(), name="delete-student-application"),
    # path('employer-for-staff', EmployerJobApplicationStaffView.as_view(), name='employer-for-staff'),
    # path('employer-table-for-staff', EmployerJobApplicationStaffTableView.as_view(), name='get-employer-for-staff-table'),
    # path("student-application-details", StudentApplicationDetailView.as_view(), name="student-application-details"),
    # path("employer-application-details", EmployerApplicationDetailView.as_view(), name="employer-application-details"), 
    # path("admin-job-application-table/<int:index>", AdminJobApplicationTableView.as_view(), name="get-admin-job-application-table"),
    # path('admin', AdminJobApplicationView.as_view(), name='admin-job-application'),


    # path('employer', EmployerJobApplicationView.as_view(), name='employer-job-application'),
    # path("employer-job-application-table", EmployerJobApplicationTableView.as_view(), name="get-employer-job-application-table"),
    # path('employer-delete/<int:id>', DeleteEmployerJobApplication.as_view(), name='employer-job-application-delete'),
 ]