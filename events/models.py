from django.db import models
from django.utils.text import slugify

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    start = models.DateTimeField()
    description = models.TextField()
    time = models.TimeField()
    venue = models.CharField(max_length=255) 
    price = models.FloatField()
    image = models.ImageField(upload_to="events", null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title