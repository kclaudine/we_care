from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile']


class SellForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['district','sector','action','type','image','price','description']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name','email','phone','therapist_name']