import email
#from socket import fromshare
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from random import choice
from string import ascii_letters


class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    contact = forms.IntegerField()
    credit_card = forms.IntegerField()
    identification_card = forms.CharField()
    passport = forms.CharField()

    def __init__(self, *args, **kargs):
        super(CreateUserForm, self).__init__(*args, **kargs)
        del self.fields['password2']
        # self.fields.pop('username')

    def save(self):
        #random = ''.join([choice(ascii_letters) for i in range(30)])
        #self.instance.username = random
        return super(CreateUserForm, self).save()

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'first_name', 'last_name', 'email', 'contact', 'credit_card', 'identification_card',
                                                 'passport', 'password1')
