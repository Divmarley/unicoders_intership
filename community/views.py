from email.mime import image
from django.http import Http404, JsonResponse
from django.shortcuts import render 
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import UserProfile
from .forms import CommunityForm, EditCommounityProfileForm, PostForm
from .models import Community, CommunityFollower, Post, PostComment

class CommounityView(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    form_class = CommunityForm
    def get(self,request):
        template_name='accounts/main/community/index.html'
        community = Community.objects.all()
        profile = UserProfile.objects.get(user_id=request.user.id)  
        context={ 
            'profile':profile,
            "title":"Community",
            "form":self.form_class,
            "community_list":community
        }
        return render(request,template_name,context)

    def post(self,request):
        message = ""
        if request.user.user_type != 'Admin' or request.user.user_type != 'Staff':
            raise Http404({"message":"Unauthorized"})
            # return JsonResponse({"message":"Unauthorized"})
            
        # is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        # if is_ajax:
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.created_by=request.user
            form.save()
            message = "success"
            return JsonResponse({"message":message})
        message = form.errors
        return JsonResponse({"message":message})

class EditCommounityProfile(LoginRequiredMixin,View):
    login_url = "account:login"
    redirect_field_name = "redirect_to"
    form_class = EditCommounityProfileForm

    def post(self, request, id, *args, **kwargs):
        message = "" 
        community = Community.objects.get(id=id)
        data = {"name": community.name}
        form = self.form_class(request.POST, initial=data)
        if form.is_valid(): 
            change_community = form.save(commit=False)
            name = form.cleaned_data['name']
            image = form.cleaned_data['image']

            if form.has_changed():
                community.name = name
                community.image = image
                community.save() 
                message = "success"
                return JsonResponse({"message": message})
            else:
                message = form.errors
            return JsonResponse({"message": message})
        else:
            message = form.errors 
            return JsonResponse({"message":message})

class CommounityDetailView(View):
    def get(self,request, *args, slug, **kwargs):
        template_name="accounts/main/community/detail.html" 
        commounity = Community.objects.get(slug=slug)
        posts=Post.objects.filter(community=commounity)
        community_followers =CommunityFollower.objects.filter(community__slug=slug).count()
        profile = UserProfile.objects.get(user_id=request.user.id)
        l=[]  

        for p in posts:
            d={ 
                "obj":p,
                "count": PostComment.objects.filter(post__id=p.id).count(), 
            }
            l.append(d) 
        context={ 
            'profile':profile,
            'commounity':commounity,
            "title":f'{commounity.name} Community',
            "post":l,
            "community_followers":community_followers,
            # "comment_count":comment
            }
        return render(request,template_name,context)

class FollowCommunity(View):
    #get all followers of community
    def get(self, request, comm_id):
        template_name = 'accounts/main/community/community_followers'
        followers = CommunityFollower.objects.filter(community=comm_id)
        context = {
            'followers': followers
        }
        return render(request, template_name, context)


    def post(self, request, comm_id):
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if is_ajax:
            try:
                follower = CommunityFollower.objects.get(user=request.user, community=comm_id)
                if follower:
                    follower.delete()
                    return JsonResponse({"message":"unfollowed successfully"})
            except CommunityFollower.DoesNotExist:
                    CommunityFollower.objects.create(
                        community=comm_id,
                        user=request.user,
                    )
                    return JsonResponse({"message": "followed successfully"})

class Posts(View):
    form_class = PostForm
    #get all followers of community
    def get(self, request, comm_id):
        template_name = 'accounts/main/community/post'
        posts = Post.objects.filter(community=comm_id)
        context = {
            'posts': posts,
            'form': self.form_class
        }
        return render(request, template_name, context)


    def post(self, request, comm_id):
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if is_ajax:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.instance.created_by=request.user
                form.instance.community = comm_id
                form.save()
                return JsonResponse({"message":"Post created successfully"})
            return JsonResponse({"message":"Something went wrong"})
