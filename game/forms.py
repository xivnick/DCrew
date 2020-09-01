from django import forms
from .models import Game
from django.forms import Select


class GuideSelect(Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = 'disabled'

        return option


class CreateGameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ['mode']

        widgets = {
            'mode': GuideSelect(attrs={
                'class': 'no-margin',
                'v-model': "mode",
                'v-on:change': "sendSetting",
            }),
        }