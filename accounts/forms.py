from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


# ================================
# REGISTER FORM
# ================================
class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder":"Password",
            "id":"password1"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder":"Confirm Password",
            "id":"password2"
        })
    )
    class Meta:
        model = User
        fields = ["username","email"]

        widgets = {
            "username":forms.TextInput(attrs={"placeholder":"Username"}),
            "email":forms.EmailInput(attrs={"placeholder":"Email"}),
        }

    # ❌ Duplicate Username Check
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

    # ❌ Duplicate Email Check
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered")
        return email

    # 🔐 Password Rules Validation
    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 != p2:
            raise ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# ================================
# LOGIN FORM
# ================================
class LoginForm(forms.Form):

    login = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Email or Username",
            "class": "form-control"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": "form-control"
        })
    )