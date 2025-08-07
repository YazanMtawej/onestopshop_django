from django.db import models
from operator import mod
from django.contrib.auth.models import User
from product.models import Product 

# Create your models here.


class OrderStatus(models.TextChoices):
       PROCESSING='processing'
       SHIPPED='shipped'
       DELIVERED='delivered'      
 



class PaymentStatus(models.TextChoices):
         PAID='paid'
         UNPADE='unpaid'     
         


class PaymentMode(models.TextChoices):
         COD='cod'
         CARD='card'      


class Order(models.Model):

       city=models.CharField(max_length=400,default="",blank=False)
       zip_code=models.CharField(max_length=100,default="",blank=False)
       street=models.CharField(max_length=500,default="",blank=False)
       state=models.CharField(max_length=500,default="",blank=False)     
       country=models.CharField(max_length=100,default="",blank=False)
       phone_no=models.CharField(max_length=400,default="",blank=False) 
       total_amount=models.IntegerField(default=0)
       payment_status=models.CharField(max_length=30,choices=PaymentStatus.choices,default=PaymentStatus.UNPADE)
       payment_mode=models.CharField(max_length=30,choices=PaymentMode.choices,default=PaymentMode.COD)  
       status=models.CharField(max_length=60,choices=OrderStatus.choices,default=OrderStatus.PROCESSING)
       user=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
       createAt=models.DateTimeField(auto_now_add=True)
       
       def _str_(self):
           return str(self.id) 


class OrderItem(models.Model):
       product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
       order=models.ForeignKey(Order,null=True,on_delete=models.CASCADE,related_name='orderitems')
       name=models.CharField(max_length=200,default="",blank=False)
       quantity=models.IntegerField(default=1)  
       price=models.DecimalField(max_digits=7,decimal_places=2,blank=False)
       
       def _str_(self):
           return str(self.name) 