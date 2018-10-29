from django import forms        
from .models import post, category      


class CreateForm(forms.ModelForm):
    class Meta:
        model = post            
        fields = [               
            'post_title',
            'slug',
            'post_body',
            'post_image',
            'post_category',
        ]

class categoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = [
            'name'
        ]
