from django.core.urlresolvers import reverse
from django.db import models


# Define a post model.
class Post(models.Model):
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField('Publication date', auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    content = models.TextField(max_length=10000)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:details', args=[str(self.id)])
