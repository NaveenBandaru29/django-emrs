# from django import forms
# # from django.contrib.auth.models import User
# from .models import UserForm


# class RegisterForm(forms.Form):
#     email = forms.EmailField(required=True)
#     username = forms.CharField(max_length = 30)
#     password = forms.CharField(max_length=30, widget=forms.PasswordInput)
#     language = forms.CharField(max_length=80)
#     artist = forms.CharField(max_length=80)
#     gender = forms.CharField(max_length = 30, widget=forms.Select)

#     class Meta:
#         fields = ("username", "email", "password", "language", "gender", "artist")

#     def save(self):
#         data = self.cleaned_data
#         userProfile = UserForm(username=data['username'],gender=data['genger'],email=data['email'],
#                                 language=data['language'],artist=data['artist'],password=data['password'])
#         userProfile.save()
