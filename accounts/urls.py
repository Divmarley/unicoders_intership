from django.urls import path 
from accounts.views import * 
app_name='account'
urlpatterns = [ 
    path('', IndexView.as_view(),name ='index'),
    path('signup', CreateAccountView.as_view(),name ='signup'),
    path('login', LoginView.as_view(),name ='login'),
    path('dashboard', DashboardView.as_view(),name ='dashboard'),
    path('logout', LogoutView.as_view(),name ='logout'),
    path('profile', ProfileView.as_view(),name ='profile'), 
    path('create-profile', CreateProfileView.as_view(),name ='profile_create'),
    path('profile-edit/<int:id>', ProfleUpdateView.as_view(),name ='profile-edit'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('create-social-link', CreateSocialMediaLinkView.as_view(), name='create-social-link'),
    path('profile/<int:id>/change-profile-image', CreateProfileImgae.as_view(), name="change-profile-image"),
    path('message/', UserMessage.as_view(), name="messages"),
]

 