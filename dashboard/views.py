from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.base import TemplateView, TemplateResponseMixin, ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from models import Book
from forms import BookForm


class MultipleObjectMixin(object):
    def get_object(self, queryset=None, *args, **kwargs):
        slug = self.kwargs.get('slug')
        if slug:
            try:
                obj = self.model.objects.get(slug=slug)
            except self.model.MultipleObjectsReturned:
                obj = self.get_queryset().first()
            except:
                raise Http404
            return obj
        raise Http404


class BookCreateView(SuccessMessageMixin, CreateView):
    # model = Book
    # fields = ['title', 'description']
    # but better to us "form_class" :
    form_class = BookForm
    # success_url = '/book/' # it is not very dynamic, better to us "get_success_url" method
    template_name = 'dashboard/form.html'

    # best practice to do success message with SuccessMessageMixin
    success_message = '%(title)s is created at %(created_at)s'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        valid_form = super(BookCreateView, self).form_valid(form)
        # better to do success alert here
        # messages.success(self.request, 'Book "%s" created!' % self.object.title)
        return valid_form

    def get_success_url(self):
        # you can do success message here
        # messages.success(self.request, 'Book created!')
        return reverse('dashboard:book_list')

    # to costomise success_message data us this method:
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            created_at=self.object.timestamp,
        )


class BookUpdateView(MultipleObjectMixin, UpdateView):
    model = Book
    # fields = ['title', 'description']
    form_class = BookForm
    template_name = 'dashboard/form.html'


class BookDeleteView(DeleteView):
    model = Book

    def get_success_url(self):
        return reverse('dashboard:book_list')


class BookDetailView(MultipleObjectMixin, DetailView):
    model = Book
    # You can do this but not necessary(in template us "object" to get instances of model)
    # def get_context_data(self, *args, **kwargs):
    #     context = super(BookDetail, self).get_context_data(*args, **kwargs)
    #     context['title'] = 'bla'
    #     print context
    #     return context


class BookListView(ListView):
    model = Book
    # In tamplate us "object_list" to get instances of model

    # To us query sets
    def get_queryset(self, *args, **kwargs):
        qs = super(BookListView, self).get_queryset(*args, **kwargs).order_by('-timestamp')
        return qs


class LoginRequiredMixin(object):  # class to login_required - best practice
    # @classmethod
    # def as_view(cls, **kwargs):
    #     view = super(LoginRequiredMixin, cls).as_view(**kwargs)
    #     return login_required(view)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class DashboardTemplateView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'This is about as!'
        return context


class SomeView(LoginRequiredMixin, ContextMixin, TemplateResponseMixin, View):
    template_name = 'about.html'

    # @method_decorator(login_required) # not working with other methods, only GET(bed practice)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        for kwarg in kwargs:
            print kwarg
        context['title'] = 'Hello class-base-views!'
        return self.render_to_response(context)

    # @method_decorator(login_required)  # dispatch required for any other method: POST, GET, PUT...(not bed practice)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(SomeView, self).dispatch(request, *args, **kwargs)
