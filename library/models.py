from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    membership_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=[('user', 'Regular User'), ('admin', 'Administrator')], default='user')
    account_status = models.CharField(max_length=10, choices=[('active', 'Active'), ('suspended', 'Suspended'), ('deleted', 'Deleted')], default='active')
    join_date = models.DateTimeField(auto_now_add=True)
    preferred_language = models.CharField(max_length=10, default='en')
    receive_email_notifications = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    page_count = models.IntegerField()
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']  

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    
    class Meta:
        ordering = ['-borrowed_date']
