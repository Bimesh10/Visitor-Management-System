from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Define roles as constants
ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Gatekeeper', 'Gatekeeper'),
    ('Visitor', 'Visitor'),
]

# Model to represent a contact person
class Contact(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[('Active', 'Active'), ('Inactive', 'Inactive')],
        default='Active'
    )

    def __str__(self):
        return self.name

# Model to represent a visitor
class Visitor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_visit = models.DateField()
    purpose = models.TextField(default="No purpose specified")
    
    # Foreign Key to Contact (added with a default value to avoid errors during migrations)
    contact = models.ForeignKey(
        'Contact',
        on_delete=models.CASCADE,
        default=1  # Replace 1 with an actual contact ID or create a default contact in the database
    )

    # New fields to track meeting time
    meeting_start_time = models.DateTimeField(null=True, blank=True)
    meeting_end_time = models.DateTimeField(null=True, blank=True)

    # New field to track the appointment status (whether the meeting is completed or not)
    status = models.CharField(
        max_length=20, 
        choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Scheduled'
    )

    def __str__(self):
        return self.name

    def release_slot(self):
        """
        This function will be used to release the meeting slot when the meeting is over.
        It will set the status to 'Completed' and reset the meeting times.
        """
        self.status = 'Completed'
        self.meeting_end_time = datetime.now()
        self.save()

# UserProfile model to manage roles (Admin, Gatekeeper, Visitor)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Visitor')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    # Convenience methods to check roles
    def is_admin(self):
        return self.role == 'Admin'

    def is_gatekeeper(self):
        return self.role == 'Gatekeeper'

    def is_visitor(self):
        return self.role == 'Visitor'

# Automatically create and update UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
