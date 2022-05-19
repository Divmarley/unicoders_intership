 
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import redirect, render
# from django.views import View
# from accounts.models import UserProfile 
# from notifications.utilities import create_notification
# from application.forms import *
# from django.template import loader
# from application.models import JobApplication
# from django.contrib.auth.mixins import LoginRequiredMixin

# # creating new job application

# # class StudentJobApplicationView(LoginRequiredMixin,View):
# #     login_url = "account:login"
# #     redirect_field_name = "redirect_to"
# #     form_class = StudentJobApplicationForm
# #     template_name = 'accounts/main/application/students/index.html'
    
# #     def get(self,request):
# #         profile = UserProfile.objects.get(user=request.user.id) 
# #         context = {
# #             "title":"Applications",
# #             "profile":profile ,
# #             'form':self.form_class
# #             }
# #         return render(request, self.template_name, context)
 
# #     def post(self,request): 
# #         form = self.form_class(request.POST, request.FILES)
# #         if form.is_valid():
# #             form.instance.user_id=request.user.id
# #             form.instance.status=1 
# #             content = f"An application has been received from { request.user.email }"
# #             create_notification(request=request, notification_type=3, content=content)
# #             form.save()
# #             message = "success"
# #             return JsonResponse({"message":message})
# #         else:
# #             message = "success"
# #             return JsonResponse({"message":message}) 
     
# # class StudentJobApplicationTableView(LoginRequiredMixin,View):
    
# #     login_url = "accounts:login"
# #     redirect_field_name = "redirect_to"

# #     def get(self, request,  *args, **kwargs):
# #         template = loader.get_template("accounts/main/application/students/table.html") 
# #         student_job_applications = JobApplication.objects.filter(user=request.user.id)
# #         profile = UserProfile.objects.get(user_id=request.user.id) 
# #         context = { 
# #             'student_job_applications': student_job_applications,
# #             "profile":profile ,
# #         }
# #         return HttpResponse(template.render(context, self.request))

# # class DeleteStudentJobApplication(LoginRequiredMixin, View):
# #     login_url = "account:login"
# #     redirect_field_name = "redirect_to"
 
# #     def get(self, request, id, *args, **kwargs): 
# #         JobApplication.objects.get(id=id).delete()
# #         message = "success"
# #         return JsonResponse({"message": message })

# # class ChangeStudentApplicationStatus(LoginRequiredMixin,View):
# #     login_url = "account:login"
# #     redirect_field_name = "redirect_to"
# #     def get(self, request, id):
# #     #     is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
# #     #     if is_ajax:
# #         application = JobApplication.objects.get(id=id)
# #         if application.status == 4:
# #             application.status = 3
# #             content = "Your application has been successfully completed."
# #             create_notification(request, application.user.id, 2, content)
# #             return JsonResponse({"message":"Application status changed to Completed"})
# #         else:
# #             application.status = 4
# #             content = "Your application has been approved. Awaiting placement"
# #             create_notification(request, application.user.id, 2, content)
# #             return JsonResponse({"message":"Application status changed to Awaiting placement"})





# class ChangeEmployerApplicationStatus(LoginRequiredMixin,View):
#     login_url = "account:login"
#     redirect_field_name = "redirect_to"
#     def get(self, request, id):
#         is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
#         if is_ajax:
#             application = EmployerApplication.objects.get(id=id)
#             if application.status == 4:
#                 application.status = 3
#                 content = "Your application has been successfully completed."
#                 create_notification(request, application.user.id, 2, content)
#                 return JsonResponse({"message":"Application status changed to Completed"})
#             else:
#                 application.status = 4
#                 content = "Your application has been approved. Awaiting placement"
#                 create_notification(request, application.user.id, 2, content)
#                 return JsonResponse({"message":"Application status changed to Awaiting placement"})
#         else:
#             return JsonResponse({"message":"Something went wrong"})

# class StudentApplicationDetailView(LoginRequiredMixin,View):
#     login_url = "account:login"
#     redirect_field_name = "redirect_to"
#     def get(self, request, id):
#         template_name='main/application/students/application_detail.html'
#         application = JobApplication.objects.get(id=id)
#         if application.status == 1:
#             application.status = 2

#         context = {
#             "application":application
#         }
#         return render(request, template_name, context)

# class EmployerApplicationDetailView(LoginRequiredMixin,View):
#     login_url = "account:login"
#     redirect_field_name = "redirect_to"
#     def get(self, request, id):
#         template_name='main/application/employers/application_detail.html'
#         application = EmployerApplication.objects.get(id=id)
#         if application.status == 1:
#             application.status = 2

#         context = {
#             "application":application
#         }
#         return render(request, template_name, context)

# # admin applications view
# class AdminJobApplicationView(LoginRequiredMixin,View):
#     login_url = "account:login"
#     redirect_field_name = "redirect_to"
#     # form_class = AdminJobApplicationForm
#     template_name = 'accounts/main/application/admin/index.html'
    
#     def get(self,request):
#         profile = UserProfile.objects.get(user_id=request.user.id)    
#         context = {
#             "title":"Applications",
#             "profile":profile ,
#             # 'form':self.form_class
#             }
#         return render(request, self.template_name, context)
    
#     def post(self,request):
#         # is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
#         # if is_ajax:
#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             form.instance.created_by=request.user
#             form.instance.status=1
#             content = f"An application has been received from {request.user.email}"
#             create_notification(request=request, notification_type=3, content=content)
#             form.save()
#             return JsonResponse({"message":"success"})
#         return JsonResponse({"message":form.errors})
 
# class AdminJobApplicationTableView(LoginRequiredMixin,View):
    
#     login_url = "accounts:login"
#     redirect_field_name = "redirect_to"

#     def get(self, request,  *args,index, **kwargs):
#         template = loader.get_template("accounts/main/application/admin/all_student_applications_table.html") 
        
#         profile = UserProfile.objects.get(user_id=request.user.id) 

#         if index == 3:
#             # branches = Branch.objects.filter(business_id=self.request.user.business_id,business_type=self.request.user.business_type )
#             # # title = "All Branches" 
#             student_job_applications = JobApplication.objects.all()
#         elif index == 4:
            
#             print("hi")

#         context = { 
#             'applications': student_job_applications,
#             "profile":profile ,
#             "index":index
#         }
#         return HttpResponse(template.render(context, self.request))

# class EmployerJobApplicationStaffView(LoginRequiredMixin, View):
#     login_url = "accounts:login"
#     redirect_field_name = "redirect_to"

#     def get(self, request,  *args, **kwargs):
#         template = loader.get_template("accounts/main/application/admin/employers/index.html")
#         profile = UserProfile.objects.get(user_id=request.user.id) 
#         # employer_job_applications = EmployerApplication.objects.all()
#         context = { 
#             'title': "Employer Applications",
#             'profile':profile,
#             # 'employee_applications': employer_job_applications
#         }
#         return HttpResponse(template.render(context, self.request))

# class EmployerJobApplicationStaffTableView(LoginRequiredMixin,View):
#     login_url = "accounts:login"
#     redirect_field_name = "redirect_to"

#     def get(self, request,  *args, **kwargs):
#         template = loader.get_template("accounts/main/application/admin/employers/table.html") 
#         employer_job_applications = EmployerApplication.objects.filter(user=request.user)
#         profile = UserProfile.objects.get(user_id=request.user.id) 
#         context = { 
#             'employer_job_applications': employer_job_applications,
#             "profile":profile ,
#         }
#         return HttpResponse(template.render(context, self.request))








# #Employers
# # class EmployerJobApplicationView(LoginRequiredMixin,View):
# #     login_url = "account:login"
# #     redirect_field_name = "redirect_to"
# #     form_class = EmployerJobApplicationForm
# #     template_name = 'accounts/main/application/employers/index.html'
    
# #     def get(self,request): 
# #         profile = UserProfile.objects.get(user_id=request.user.id)  
# #         context = {
# #             "title":"Employer Applications",
# #             'form':self.form_class, 
# #             'profile':profile
# #         }
# #         return render(request, self.template_name,context)
   
# #     def post(self,request): 
# #         profile = UserProfile.objects.get(user_id=request.user.id)  
# #         form = self.form_class(request.POST)
# #         if form.is_valid(): 
# #             form.instance.user=profile
# #             form.instance.status=1 
# #             content = f"An application has been received from {request.user.email}"
# #             create_notification(request=request, notification_type=3, content=content)
# #             form.save()
# #             message = "success"
# #             return JsonResponse({"message":message})
# #         else:
# #             message = form.errors
# #             return JsonResponse({"message":message})  

# # class EmployerJobApplicationTableView(LoginRequiredMixin,View):
# #     login_url = "accounts:login"
# #     redirect_field_name = "redirect_to"

# #     def get(self, request,  *args, **kwargs):
# #         template = loader.get_template("accounts/main/application/employers/table.html") 
# #         employer_job_applications = EmployerApplication.objects.all()
# #         context = { 
# #             'employers_job_applications': employer_job_applications
# #         }
# #         return HttpResponse(template.render(context, self.request))

# # class DeleteEmployerJobApplication(LoginRequiredMixin, View):
# #     login_url = "account:login"
# #     redirect_field_name = "redirect_to"
 
# #     def get(self, request, id, *args, **kwargs): 
# #         EmployerApplication.objects.get(id=id).delete()
# #         message = "success"
# #         return JsonResponse({"message": message })
  