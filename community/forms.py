from django.forms import ModelForm

from community.models import Community, Post


class CommunityForm(ModelForm):
    class Meta:
        model = Community
        fields = ['name']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['description']