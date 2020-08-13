from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput

from tests.models import Test, TestCase


class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = [
            "title", "description"
        ]


class TestCaseForm(forms.ModelForm):

    class Meta:
        model = TestCase
        fields = ["content",]



class AnswerForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = "__all__"


