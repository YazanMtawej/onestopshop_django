from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save 
from decimal import Decimal



# Create your models here.


class Profile(models.Model):
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    reset_password_token=models.CharField(max_length=50,default="",blank=True) 
    reset_password_expire=models.DateTimeField(null=True,blank=True)
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # المستخدم
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # رصيد المشرف
 
@receiver(post_save,sender=User)
def save_profile(sender ,instance,created, **kwargs):
    
   print ('instance',instance)
   user=instance
    
   if created :
        profile=Profile(user=user)
        profile.save() 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)        

class UserPoints(models.Model):
    ACTION_CHOICES = [
        ('charge', 'Charge'),
        ('purchase', 'Purchase'),
    
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.DecimalField(max_digits=10, decimal_places=2)
    action_type = models.CharField(max_length=20, choices=[('charge', 'Charge'), ('purchase', 'Purchase')], default='charge')
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.points}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

    
    if instance.is_superuser:
        profile = instance.profile
        profile.points = 1000000  
        profile.balance = 1000000
        profile.save()