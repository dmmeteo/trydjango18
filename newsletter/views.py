from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from forms import ContactForm, SignUpForm
from models import SignUp


# Create your views here.
def home(request):
    title = 'Welcome!'
    form = SignUpForm(request.POST or None)
    context = {
        'template_title': title,
        'form': form
    }

    if request.user.is_authenticated():
        title = 'Hi, %s!' % request.user

    if form.is_valid():
        # print request.POST['email'] # not recommended
        instance = form.save(commit=False)

        full_name = form.cleaned_data.get('full_name')
        if not full_name:
            full_name = request.user
        instance.full_name = full_name
        instance.save()
        context['template_title'] = 'Thank you!'

    return render(request, 'home.html', context)


def contact(request):
    form = ContactForm(request.POST or None)
    title = 'Contact Us'
    title_center = True

    if form.is_valid():
        # for key, value in form.cleaned_data.iteritems():
        #     print key, value
        #     print form.cleaned_data.get(key)
        form_email = form.cleaned_data.get('email')
        form_message = form.cleaned_data.get('message')
        form_full_name = form.cleaned_data.get('full_name')

        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'dmmeteo@yandex.ru']
        contact_message = '%s: %s via %s' % (form_full_name,
                                             form_message,
                                             form_email)
        send_mail(subject,
                  contact_message,
                  from_email,
                  to_email,
                  fail_silently=False)

    context = {
        'form': form,
        'title': title,
        'title_center': title_center,
    }
    return render(request, 'forms.html', context)


def about(request):
    queryset = None
    if request.user.is_authenticated and request.user.is_staff:
        queryset = SignUp.objects.all().order_by('-timestamp')

    return render(request, 'about.html', {'queryset': queryset})
