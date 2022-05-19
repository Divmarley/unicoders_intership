from django.forms import ModelForm
from application.models import EmployerApplication, JobApplication

class StudentJobApplicationForm(ModelForm): 
    class Meta:
        model = JobApplication
        fields = ['cv','related_field', 'job_type', 'highest_qualification', 'yrs_of_experience', 'status', 'payment_budget', 'location','desciption']

class EmployerJobApplicationForm(ModelForm): 
    class Meta:
        model = EmployerApplication
        fields = ['title', 'related_field', 'job_type', 'yrs_of_experience', 'status', 'location','desciption', 'highest_qualification','location']


