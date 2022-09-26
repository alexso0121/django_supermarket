from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from web.models import newuser
from django.forms import ModelForm


class NewUserForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user


def formnew(Modelforms):
    purchase_history = forms.CharField(max_length=10000)

    class Meta:
        model = newuser
        field = '__all__'


class numform(forms.Form):
    quality = forms.IntegerField(max_value=200)
