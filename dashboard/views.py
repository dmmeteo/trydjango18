from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateView, TemplateResponseMixin, ContextMixin


class DashboardTemplateView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'This is about as!'
        return context


class SomeView(ContextMixin, TemplateResponseMixin, View):
    template_name = 'about.html'
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        for kwarg in kwargs:
            print kwarg
        # context['title'] = 'Hello class-base-views!'
        return self.render_to_response(context)
