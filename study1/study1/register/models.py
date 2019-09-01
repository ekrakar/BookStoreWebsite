from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
# Create your models here.


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    student_ID = models.CharField(max_length = 10)
    mailing_Address = models.CharField(max_length = 200, blank=True)
    billing_Address = models.CharField(max_length = 200, blank=True)
    choice = [("1","Visa"), ("2", "MasterCard"), ("3", "Discover"), ("4", "American Express")]
    credit_Card_Type = models.CharField(max_length = 50, choices=choice, blank=True)
    credit_Card_Number = models.CharField(max_length = 20, blank=True)
    expiration_Date = models.DateField(blank=True)

    def __str__(self):
        return self.user.username

def create_info(sender, **kwargs):
    if kwargs['created']:
        user_info = UserInfo.objects.create(user=kwargs['instance'])

post_save.connect(create_info, sender=User)