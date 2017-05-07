from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.base import TemplateView, TemplateResponseMixin, ContextMixin
from django.views.generic.detail import DetailView

from models import Book


class BookDetail(DetailView):
    pass


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
