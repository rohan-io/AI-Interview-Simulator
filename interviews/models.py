from django.db import models
from django.contrib.auth.models import User


class InterviewSession(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    tech_stack = models.CharField(max_length=50)   # 👈 ADD THIS
    difficulty = models.CharField(max_length=50)
    overall_score = models.FloatField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Question(models.Model):
    ROLE_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('data', 'Data Analyst'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    question_text = models.TextField()
    expected_keywords = models.JSONField()

    def __str__(self):
        return self.question_text[:50]


class Answer(models.Model):

    session = models.ForeignKey(
        InterviewSession,
        on_delete=models.CASCADE
    )

    user_answer = models.TextField()

    score = models.FloatField()

    strengths = models.TextField(null=True, blank=True)
    weaknesses = models.TextField(null=True, blank=True)
    improvement = models.TextField(null=True, blank=True)
