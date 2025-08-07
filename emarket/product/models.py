from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class category(models.TextChoices):
  MALE= "male"
  FEMALE= "female" 
  KIDS="kids"
  UNISEX="unisex"

class longevity(models.TextChoices):
  WEAK= "weak"
  MEDIUM= "medium"
  STRONG= "strong"

class sillage(models.TextChoices):
  CLOSE= "close"
  MEDIUM= "medium"
  STRONG= "strong"


class Product(models.Model):
  name= models.CharField( max_length=200, default="",blank=False)
  discription= models.TextField( max_length=1000, default="",blank=False)
  price= models.CharField( max_length=200, default="",blank=False)
  brand= models.CharField( max_length=200, default="",blank=False)
  category= models.CharField( max_length=40,choices=category.choices)
  rating= models.DecimalField(max_digits=3,decimal_places=2,default=0)
  stock= models.IntegerField(db_default=0)
  createdAt=models.DateTimeField(auto_now_add=True)
  user= models.ForeignKey(User,null=True ,on_delete=models.SET_NULL)
  release_year=models.IntegerField(db_default=0)
  perfumer= models.CharField( max_length=200, default="",blank=False)
  concertration= models.TextField( max_length=1000, default="",blank=False)
  top_notes= models.TextField( max_length=1000, default="",blank=False)
  heart_notes= models.TextField( max_length=1000, default="",blank=False)
  base_notes= models.TextField( max_length=1000, default="",blank=False)
  fragrance_family=models.TextField( max_length=1000, default="",blank=False)
  bottle_size= models.IntegerField(db_default=0)
  longevity=models.CharField( max_length=40,choices=longevity.choices,default='Moderate')
  sillage=models.CharField( max_length=40,choices=sillage.choices ,default='Moderate')
  picture =models.TextField( max_length=1000, default="",blank=False)


  def __str__ (self):
    return self.name
   

class Review(models.Model):
  product = models.ForeignKey(Product,null=True ,on_delete=models.CASCADE, related_name='reviews')
  user= models.ForeignKey(User,null=True ,on_delete=models.SET_NULL)
  comment= models.TextField( max_length=200, default="",blank=False)
  rating= models.IntegerField(default=0)
  createdAt=models.DateTimeField(auto_now_add=True)

  def __str__ (self):
    return self.comment
 
