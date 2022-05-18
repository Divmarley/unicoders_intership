from django.db import models
from accounts.models import User, UserProfile
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True ,unique=True)
    community = models.ForeignKey('Community', related_name='posts', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(UserProfile, related_name="posts", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  self.description

    def __unicode__(self):
        return  self.description

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_by = models.ForeignKey(UserProfile, related_name="poster", on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Community(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True ,unique=True)
    slug = models.SlugField()
    created_by = models.ForeignKey(UserProfile, related_name="community", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Community, self).save(*args, **kwargs)


    class Meta:
        verbose_name = "Community"
        verbose_name_plural = "Communities"
        db_table= 'community'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("Community_detail", kwargs={"pk": self.pk})


class CommunityFollower(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.OneToOneField(UserProfile, related_name="follower", on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  self.name

    def __unicode__(self):
        return  self.name