from django import forms         #জ্যাঙ্গোর বিল্ট ইন ফরম ইম্পোর্ট করা হয়েছে
from .models import post, author, category       # মডেলের যে ফিল্ডকে ফরমে আনা হবে সেই ফিল্ড ইম্পোর্ট করা হয়েছে
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateForm(forms.ModelForm):
    class Meta:
        model = post            #  মডেলের নাম উল্লেখ করে দেওয়া হয়েছে
        fields = [               #  মডেলের যেই ফিল্ড গুলো আনা হবে সেগুলো এখানে উল্লেখ করে দিতে হবে
            'post_title',
            'slug',
            'post_body',
            'post_image',
            'post_category',
        ]

class registerUser(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        ]

class createAuthor(forms.ModelForm):
    class Meta:
        model = author
        fields =[
            'auth_image',
            'auth_details',
        ]

class categoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = [
            'name'
        ]
