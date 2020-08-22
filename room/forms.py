from django import forms
from .models import Room
from django.forms import Select


class GuideSelect(Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = 'disabled'

        return option


class CreateRoomForm(forms.ModelForm):

    class Meta:
        model = Room

        fields = ['title', 'capacity']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': '방 제목',
            }),
            'capacity': GuideSelect(attrs={
            }),
        }
