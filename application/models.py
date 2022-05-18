from calendar import c
from django.db import models

from accounts.models import User, UserProfile

job_title = (
    (1, 'Software Developer'),
    (2, 'Hardware'),
    (3, 'Web Developer'),
    (4, 'Graphics'),
)

status = (
    (1, 'Received'),#recevied for placement
    (2, 'Awaiting Placement'),#recevied for placement
    (3, 'Placed'), #Completed for placement
)


job_type = (
    (1, 'Full-time'),
    (2, 'Part-time'), 
    (3, 'Internship'), 
)
related_fields = (
    ('computer science','computer science'),
    ('information technology','information Technology'), 
    ('networking','Networking'),
    ('fashion','Fashion'),
    ('hardware','Hardware'),
    ('graphic design','Graphic Design'),
    ('graph','Graphic Design'),
)
  
class BaseApplication(models.Model):
    related_field =  models.CharField(max_length=255,choices=related_fields )
    job_type =  models.IntegerField(choices=job_type,null=True)
    highest_qualification = models.CharField(max_length=250, null=True, blank=True)
    yrs_of_experience = models.IntegerField(default=0,null=True, blank=True)
    status = models.IntegerField(choices=status, null=True, blank=True)
    payment_budget = models.CharField(max_length=255,null=True,blank=True)
    location=  models.CharField(max_length=255, null=True, blank=True)
    desciption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_btn_color(self):
        if self.status ==1:
            return 'btn-info'
        elif self.status ==2:
            return 'btn-success'
        elif self.status ==3:
            return 'btn-success'
    class Meta:
        abstract = True
    


class EmployerApplication(BaseApplication):
    user = models.ForeignKey(UserProfile, related_name="user_em_application", on_delete=models.CASCADE, null=True)
    title= models.CharField(max_length=255, blank=False, null=True)

    class Meta:
        db_table = 'employer_application'
        ordering = ['-created_at']
    
    def owner(self):
        return f"{self.title}"

    def __str__(self):
        return self.owner()

class JobApplication(BaseApplication):
    user = models.ForeignKey(UserProfile, related_name="user_job_application", on_delete=models.CASCADE, null=True)
    cv = models.FileField(upload_to='cv/')

    class Meta:
        db_table = 'job_application'
        ordering = ['-created_at']

    def owner(self):
        return f"{self.user}" 

    def __str__(self):
        return self.owner()

