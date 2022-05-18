from django.urls import path
from .views import *

app_name='community'

urlpatterns = [ 
    path('',CommounityView.as_view(), name= "index"),
    path('<str:slug>/',CommounityDetailView.as_view(), name= "detail"),
    path('community-follower', FollowCommunity.as_view(), name= "community-follower"),
    path('community-posts', Posts.as_view(), name= "community-posts"),
]
