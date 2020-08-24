from django.db import models

from users.models import User


class Test(models.Model):
    completed_by = models.ManyToManyField(User, related_name="users_tests", through="UserTests", blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def calculate_result(self, user: User):
        score = 0
        for test_case in self.testcase_set.all():
            correct_answers = test_case.answer_set.filter(is_correct=True)
            user_answers = user.users_answers.filter(test_case=test_case)

            if user_answers and correct_answers:
                coef = correct_answers.count() / user_answers.count()
                if coef > 1:
                    coef = 1
                score_per_answer = float(test_case.score / correct_answers.count()) * coef
                if coef > 0.6:
                    score += user_answers.filter(is_correct=True).count() * score_per_answer
        return score

    def get_warnings(self):
        if self.testcase_set.all().count() < 5:
            return ["there are few test cases in the test"]


class TestCase(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=255, null=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, null=True)


class Answer(models.Model):
    users_answers = models.ManyToManyField(User, related_name="users_answers")
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, null=True)
    is_correct = models.BooleanField(default=False)
    # score = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, null=True)


class UserTests(models.Model):
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
