from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import RegisterForm,LoginForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth import logout

User = get_user_model()


# ===========================
# REGISTER
# ===========================

def register_view(request):

    form = RegisterForm()

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data['password1']
            )
            user.save()

            messages.success(
                request,
                "Account created successfully!"
            )

            return redirect("login")

    return render(
        request,
        "accounts/register.html",
        {"form":form}
    )



# ===========================
# LOGIN
# ===========================
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib import messages

def login_view(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            login_input = form.cleaned_data.get("login")
            password = form.cleaned_data.get("password")

            user = authenticate(
                request,
                username=login_input,
                password=password
            )

            if user is not None:

                login(request, user)
                return redirect("interview_home")

            else:
                messages.error(request, "Invalid Credentials")

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")

def activate_account(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        return render(request, "accounts/activation_invalid.html")