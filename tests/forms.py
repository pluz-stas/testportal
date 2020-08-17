from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput

from tests.models import Test, TestCase, Answer, Comment


class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = [
            "title", "description"
        ]


class TestCaseForm(forms.ModelForm):

    class Meta:
        model = TestCase
        fields = ["content", "score"]


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ["content", "is_correct",]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]


