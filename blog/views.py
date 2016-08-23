from django.shortcuts import render, redirect
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from .forms import PostForm
from .models import Post


# Fetching a data from relation database like a list
def home(request):
    query = Post.objects.all().order_by('-id')
    context = {
        'query': query
    }

    return render(request, 'blog/home.html', context)


# A simple view for opportunity add posts
def add_post(request):
    form = PostForm(request.POST or None)
    context = {
        'form': form
    }

    if form.is_valid():
        form.save()
        return redirect('blog:home')

    return render(request, 'blog/add_post.html', context)


# By means this view we're showing detailed post with disqus comments.
def details(request, id):
    query = Post.objects.get(pk=id)

    context = {
        'query': query
    }

    return render(request, 'blog/details.html', context)


# RSS feed view
class LatesEnteriesFeed(Feed):
    title = 'Django latest posts'
    link = '/'

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('blog:details', args=[item.pk])
