from django.db import models
from cloudinary.models import CloudinaryField
import re
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
)
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


def validate_plain_text(value):
    if not value:
        return
    value = value.strip()
    if strip_tags(value) != value:
        raise ValidationError(
            "HTML tags and scripts are not allowed."
        )
    if '<' in value or '>' in value:
        raise ValidationError(
            "HTML or script content is not allowed."
        )

    if re.search(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', value):
        raise ValidationError(
            "Invalid characters are not allowed."
        )


def validate_name(value):
    validate_plain_text(value)

    if not re.fullmatch(r"[A-Za-z\s.'-]+", value.strip()):
        raise ValidationError(
            "Name can contain only letters, spaces, dots, apostrophes and hyphens."
        )

def validate_subject(value):
    validate_plain_text(value)

def validate_message(value):
    validate_plain_text(value)

phone_validator = RegexValidator(
    regex=r'^\+?[0-9]{10,13}$',
    message="Enter a valid phone number with 10 to 13 digits."
)

def validate_enquiry_name(value):
    validate_plain_text(value)

    if not re.fullmatch(r"[A-Za-z\s.'-]+", value.strip()):
        raise ValidationError(
            "Name can contain only letters, spaces, dots, apostrophes and hyphens."
        )


def validate_enquiry_phone(value):
    if not re.fullmatch(r'^\+?[0-9]{10,13}$', value):
        raise ValidationError(
            "Enter a valid phone number with 10 to 13 digits."
        )

# Create your models here.
class Post(models.Model):
    image = CloudinaryField('image', folder="nmeapp_blogs/",blank=True, null=True) 
    card_head = models.CharField(max_length=100,null=True, blank=True)
    modal_head = models.CharField(max_length=100,null=True, blank=True)
    date = models.CharField(max_length=100,null=True, blank=True)
    card_paragraph = models.TextField(null=True, blank=True)
    modal_paragraph = models.TextField(null=True, blank=True)
    keyword = models.CharField(max_length=100,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.keyword
    
# class Contact(models.Model):
#     name = models.CharField(max_length=100)
#     subject = models.CharField(max_length=100)
#     email = models.EmailField()
#     message = models.TextField()
#     phone = models.CharField(max_length=15, blank=True, null=True)

#     def __str__(self):
#         return self.name



class Contact(models.Model):

    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            validate_name
        ]
    )

    subject = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
            validate_subject
        ]
    )

    email = models.EmailField(
        max_length=254
    )

    message = models.TextField(
        validators=[
            MinLengthValidator(3),
            validate_message
        ]
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[phone_validator]
    )

    def clean(self):
        super().clean()

        if self.name:
            self.name = self.name.strip()

        if self.subject:
            self.subject = self.subject.strip()

        if self.email:
            self.email = self.email.strip().lower()

        if self.message:
            self.message = self.message.strip()

        if self.phone is not None:
            self.phone = self.phone.strip()

            if not self.phone:
                self.phone = None
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Login(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # plain text
    rate_limit = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    photo = CloudinaryField('image', folder="nmeapp_members/", blank=True, null=True)
    sentence = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="testimonials/")
    rating = models.PositiveSmallIntegerField(default=5)  # 1-5
    opinion = models.TextField()

    def __str__(self):
        return self.name
    

class Enquiry(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    business_name = models.CharField(max_length=200)
    business_category = models.CharField(max_length=150)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class AdminNotification(models.Model):

    NOTIFICATION_TYPES = (
        ("contact", "Contact"),
        ("enquiry", "Enquiry"),
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    object_id = models.PositiveIntegerField()

    title = models.CharField(max_length=200)

    message = models.CharField(max_length=300)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


