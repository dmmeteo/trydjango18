from django.shortcuts import render


def add(request):
    return render(request, 'filters/add.html', {})


def conf(request):
    return render(request, 'filters/filters_config.html', {})
