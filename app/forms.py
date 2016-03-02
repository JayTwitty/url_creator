
from django import forms

from app.models import URL

class URLForm(forms.ModelForm):

    class Meta:
        model = URL
        exclude = ['output_url', 'user']


