from django.db import models

from users.models import User


class Test(models.Model):
    completed_by = models.ManyToManyField(User, related_name="users_tests", through="UserTests")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=255)


class TestCase(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)


class Answer(models.Model):
    users_answers = models.ManyToManyField(User, related_name="users_answers")
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, null=True)

class UserTests(models.Model):
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)