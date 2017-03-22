from django.contrib import admin

# Register your models here.
from .models import SignUp
from .forms import SignUpForm


class SignUpAdmin(admin.ModelAdmin):
    list_display = ['email', 'timestamp', 'updated']
    form = SignUpForm


admin.site.register(SignUp, SignUpAdmin)
