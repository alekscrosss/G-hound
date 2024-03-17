from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import logout

from .forms import RegisterForm

class RegisterViews(View):
    form_class = RegisterForm
    template_name = "users/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="app_ghound:root")
        return super(RegisterViews, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form":self.form_class})
    
    #реєстрація
    def post(self, request):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Вітаю {username}! Ваш акаунт успішно створений ")
            return redirect(to="users:login")
        return render(request, self.template_name, {"form": form})