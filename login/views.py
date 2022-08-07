from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.


class UserAuthorization(LoginView):
    form_class = AuthenticationForm
    template_name = 'login/index.html'

    def get_success_url(self):
        return reverse_lazy('home')


def page_login(request):
    return render(request, 'login/index.html')
