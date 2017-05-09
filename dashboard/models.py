from django.conf import settings
from django.core.urlresolvers import reverse

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify



class Book(models.Model):
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='book_add')
    last_edit_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='book_edit')
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField()
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-timestamp', '-updated']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('dashboard:book_detail', kwargs={'slug': self.slug})


def pre_save_book(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instance.slug = slug

pre_save.connect(pre_save_book, sender=Book)

