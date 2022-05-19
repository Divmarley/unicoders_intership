from django.urls import path
from .views import *

app_name = 'employers'

urlpatterns = [
    path('', EmployerJobApplicationView.as_view(), name='employer-job-application'),
    path("job-application-table", EmployerJobApplicationTableView.as_view(), name="get-job-application-table"),
    path('<int:id>/delete', DeleteEmployerJobApplication.as_view(), name='employer-job-application-delete'),
    path("employer-application-status-change/<int:id>", ChangeEmployerApplicationStatus.as_view(), name="employer-application-status-change"),
]
