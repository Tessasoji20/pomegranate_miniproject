from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)   # CSE, CSBS, AIDS, etc
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code

class Semester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()  # 1 to 8

    class Meta:
        unique_together = ('course', 'number')
        ordering = ['number']

    def __str__(self):
        return f"{self.course.code} - Sem {self.number}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    semester = models.ForeignKey(Semester, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Module(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()   # 1,2,3,4,5

    class Meta:
        unique_together = ('subject', 'number')
        ordering = ['number']

    def __str__(self):
        return f"{self.subject.name} - Module {self.number}"

class UserSubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'subject')
