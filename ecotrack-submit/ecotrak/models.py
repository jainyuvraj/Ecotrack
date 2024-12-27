from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class UserTable(models.Model):
    userID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    email_otp = models.CharField(max_length=6, null=True, blank=True)    


class Staff(models.Model):
    staffID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Phone = models.CharField(max_length=15)

class Feedback(models.Model):
    FeedbackID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100, default='Anonymous')
    email = models.EmailField(default='anonymous@example.com')
    rating = models.IntegerField(default=5)
    feedback = models.TextField(default='No feedback provided')
    DateSubmitted = models.DateTimeField(default=timezone.now)
    ResponseStatus = models.BooleanField(default=False)

class ReportForm(models.Model):
    ReportID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey('UserTable', on_delete=models.CASCADE, related_name='reports')
    Image = models.ImageField(upload_to='waste_images/')
    Description = models.TextField()
    Location = models.CharField(max_length=255)
    Status = models.CharField(max_length=50,default='submitted', choices=[('Submitted', 'Submitted'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved')])

    SubmissionDate = models.DateTimeField(default=timezone.now)
    ResolutionDate = models.DateTimeField(null=True, blank=True)



class WasteReport(models.Model):
    ReportID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='waste_reports/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Report submitted on {self.submitted_at}"