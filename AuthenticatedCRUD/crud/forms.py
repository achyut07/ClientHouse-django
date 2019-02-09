from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.conf import settings
from django.contrib.auth import password_validation
from .models import ClientList, User

from django.contrib.auth import (authenticate, get_user_model, login, logout, )


class ClientAddForm(forms.ModelForm):
    class Meta:
        model = ClientList
        fields = '__all__'
        widgets = {
            'client_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter here'}
            ),
            'client_company': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter here'}
            ),
            'company_location': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter here'}
            ),
            'comapany_logo': forms.FileInput(
                attrs={'class': 'form-control', 'placeholder': ''}
            ),
            'contactno': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter here'}
            ),
            'project_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter here'}
            ),
            'tools': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter here'}
            ),
            'offer_date': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter here'}
            ),
            'deadline': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter here'}
            ),

        }



class RegisterForm(forms.ModelForm):
    """
    Form to register a new user
    """
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        strip=False,
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            # 'phonenumber',
            'username',
            'password',
            'confirm_password'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            # 'phonenumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phonenumber'}),

        }

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Password mismatch')
        password_validation.validate_password(confirm_password, self.instance)
        return confirm_password

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        # user.send_confirmation_email()
        return user


class LoginForm(forms.Form):
    """
    Form to login a user
    """
    username = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username or email'}),
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        strip=False,
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # user = None
                # try:
                #     user = User.objects.get(phonenumber=username)
                # except User.DoesNotExist:
                user = None

        if user:
            return user.email
        return None


# class UserLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self, *args, **kwargs):
#         username = self.cleaned_data.get("username")
#         password = self.cleaned_data.get("password")
#         user = authenticate(username=username, password=password)
#         user_qs = User.objects.filter(username=username)
#         if user_qs.count() == 1:
#             user = user_qs.first()
#         if not user:
#             raise forms.ValidationError("This user doesn't exist.")
#         if not user.check_password(password):
#             raise forms.ValidationError("Incorrect Password.")
#         if not user.is_active:
#             raise forms.ValidationError("The user is no longer active.")
#         return super(UserLoginForm, self).clean(*args, **kwargs)


# class UserRegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'password',
#                   'confirm_password', 'phone_number']

#     def clean(self):
#         cleaned_data = super(UserRegisterForm, self).clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#         if password != confirm_password:
#             raise forms.ValidationError(
#                 "password and confirm_password does not match")

# class UserRegisterForm(forms.ModelForm):
#     username = forms.CharField(label=(u'Username'), widget=forms.TextInput())
#     email = forms.EmailField(label=(u'Email Address'))
#     password = forms.CharField(
#         label=(u'Password'), widget=forms.PasswordInput(render_value=False))
#     password1 = forms.CharField(
#         label=(u'Confirm-Password'), widget=forms.PasswordInput(render_value=False))

#     class Meta:
#         model = User
#         fields = ['phone_number', ]

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#             User.objects.get(username=username)
#         except User.DoesNotExist:
#             return username
#         raise forms.ValidationError(
#             "That username is already taken, please select another.")

#     def clean(self):
#         if self.cleaned_data['password'] != self.cleaned_data['password1']:
#             raise forms.ValidationError(
#                 "The passwords did not match.  Please try again.")
#             return self.cleaned_data


# class UserRegisterForm(forms.Form):
    # username = forms.CharField(label=(u'Username'), widget=forms.TextInput())
    # email = forms.EmailField(label=(u'Email Address'))
    # password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    # password1 = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))

#     # class Meta:
#     #     model = User
#     #     field = ['phone_number']
#     #     exclude = ['created']

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#             User.objects.get(username=username)
#         except User.DoesNotExist:
#             return username
#         raise forms.ValidationError("That username is already taken, please select another.")

#     def clean(self):
#         if self.cleaned_data['password'] != self.cleaned_data['password1']:
#             raise forms.ValidationError("The passwords did not match.  Please try again.")
#             return self.cleaned_data


# class UserRegisterForm(forms.ModelForm):
#     # first_name = forms.CharField(required=True, widget=forms.TextInput)
#     # last_name = forms.CharField(required=True, widget=forms.TextInput)
#     # email = forms.EmailField(required=True, widget=forms.TextInput)
#     # contactnum = forms.CharField(required=True, widget=forms.TextInput)
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password=forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = ExtendedUserExample
#         fields = '__all__'
#         widgets = {
#         'phone_number': forms.TextInput(
#                 attrs={'class' : 'form-control', 'placeholder' : '+977-'}
#             ),
#         }

#     def clean(self):
#         cleaned_data = super(UserRegisterForm, self).clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#         if password != confirm_password:
#             raise forms.ValidationError("password and confirm_password does not match")

    # def clean_email(self):
    #     email =self.cleaned_data.get('email')
    #     try:
    #         user = User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         return email

    #     raise forms.ValidationError('This email adress is already in use !.')

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
    #         raise forms.ValidationError(u'Username "%s" is already in use.' % username)
    #     return username
