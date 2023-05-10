from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Order, Contact


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

        self.fields['username'].widget.attrs.update({'placeholder': 'Username*', 'autocomplete': None, 'autofocus': True})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password*'})

class ForgotForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

        self.fields['email'].widget.attrs.update({'placeholder': 'Email*', 'autocomplete': None, 'autofocus': True})

class ConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

        self.fields['new_password1'].widget.attrs.update({'placeholder': 'New Password*', 'autofocus': True})
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'New Password Confirmation*'})

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

        self.fields['username'].widget.attrs.update({'placeholder': 'Username*', 'autocomplete': None})
        self.fields['username'].help_text = None
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Firstname*', 'autocomplete': None})
        self.fields['first_name'].required = True
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Lastname*', 'autocomplete': None})
        self.fields['last_name'].required = True
        self.fields['email'].widget.attrs.update({'placeholder': 'Email*', 'autocomplete': None})
        self.fields['email'].required = True
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password*'})
        self.fields['password1'].help_text = None
        self.fields['password2'].widget.attrs.update({'placeholder': 'Password Confirmation*'})
        self.fields['password2'].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError('This email is already taken.')
        return email
        
class UpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Firstname*', 'autocomplete': None})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Lastname*', 'autocomplete': None})
        self.fields['username'].widget.attrs.update({'placeholder': 'Username*'})
        self.fields['username'].help_text = None
        self.fields['username'].required = False
        self.fields['email'].widget.attrs.update({'placeholder': 'Email*', 'autocomplete': None})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        self.email = self.initial.get('email')
        
        if User.objects.filter(email=email).exclude(email=self.email):
            raise forms.ValidationError('This email is already taken.')
        return email
           
class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Old password*'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'New password*'})
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'New password confirmation*'})

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'transaction_id', 'status', 'created_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

        self.fields['firstname'].widget.attrs.update({'placeholder': 'Firstname*', 'autocomplete': None, 'autofocus': True})
        self.fields['lastname'].widget.attrs.update({'placeholder': 'Lastname*', 'autocomplete': None})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email*', 'autocomplete': None})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Phone Number*', 'autocomplete': None})
        self.fields['address'].widget.attrs.update({'placeholder': 'Address*', 'autocomplete': None})
        self.fields['city'].widget.attrs.update({'placeholder': 'City*', 'autocomplete': None})
        self.fields['zipcode'].widget.attrs.update({'placeholder': 'Zipcode*', 'autocomplete': None})
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

        self.fields['firstname'].widget.attrs.update({'placeholder': 'Firstname*', 'autocomplete': None, 'autofocus': True})
        self.fields['lastname'].widget.attrs.update({'placeholder': 'Lastname*', 'autocomplete': None})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Phone Number*', 'autocomplete': None})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email*', 'autocomplete': None})
        self.fields['message'].widget.attrs.update({'placeholder': 'Type your message*'})
