from django import forms
from django.core.validators import URLValidator


class UrlForm(forms.Form):
    url = forms.URLField(label='Address',
                         max_length=300,
                         widget=forms.TextInput(
                             attrs={'autofocus': True,
                                    'placeholder': "https://wazny-adres.com/",
                                    'input_type': 'url'}),
                         validators=[URLValidator], )
