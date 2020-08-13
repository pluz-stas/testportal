from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput

from tests.models import Test


class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = [
            "title", "description"
        ]


class TestCase(forms.ModelForm):

    class Meta:
        model = Test
        fields = "__all__"


class Answer(forms.ModelForm):

    class Meta:
        model = Test
        fields = "__all__"


