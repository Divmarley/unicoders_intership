from django.shortcuts import render
from django.views import View
from django.template import loader
from django.http import HttpResponse, JsonResponse
from accounts.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from application.forms import StudentJobApplicationForm
from application.models import JobApplication
from notifications.utilities import create_notification
# Create your views here.
class StudentJobApplicationView(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    form_class = StudentJobApplicationForm
    template_name = 'accounts/main/student/application/index.html'
    
    def get(self,request): 
        profile = UserProfile.objects.get(user_id=request.user.id)  
        context = {
            "title":"Student Applications",
            'form':self.form_class, 
            'profile':profile
        }
        return render(request, self.template_name,context)
   
    def post(self,request): 
        profile = UserProfile.objects.get(user_id=request.user.id)  
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid(): 
            form.instance.user=profile
            form.instance.status=1 
            form.save()
            content = f"An application has been received from {request.user.email}"
            create_notification(request=request, notification_type=2, content=content)
            message = "success"
            return JsonResponse({"message":message})
        else:
            print(form.errors)
            message = form.errors
            return JsonResponse({"message":message})  

class StudentJobApplicationTableView(LoginRequiredMixin,View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request,  *args, **kwargs):
        template = loader.get_template("accounts/main/student/application/table.html") 
        Student_job_applications = JobApplication.objects.all()
        context = { 
            'students_job_applications': Student_job_applications
        }
        return HttpResponse(template.render(context, self.request))

class DeleteStudentJobApplication(LoginRequiredMixin, View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
 
    def get(self, request, id, *args, **kwargs): 
        JobApplication.objects.get(id=id).delete()
        message = "success"
        return JsonResponse({"message": message })

class ChangeStudentApplicationStatus(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    def get(self, request, id):
        application = JobApplication.objects.get(id=id)
        if application.status == 1:
            application.status = 2
            application.save()
            content = "Your application is awaiting placement."
            create_notification(request, application.user.id, 1, content)
            return JsonResponse({"message":"Application status changed to Completed"})
        elif application.status == 2:
            application.status = 3
            application.save()
            content = "Your application has been approved."
            create_notification(request, application.user.id, 1, content)
            return JsonResponse({"message":"You have been placed sucessfully"})
        elif application.status == 3:
            application.status = 3
            application.save()
