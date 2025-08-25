from rest_framework import serializers
from .models import Product ,Review

class ProductSerializer(serializers.ModelSerializer):
   reviews = serializers.SerializerMethodField(method_name='get_reviews', read_only= True)
   class  Meta:
        model= Product
        fields= '__all__'
        
   def get_reviews( self, obj):
      reviews =obj.reviews.all()
      serializers =ReviewSerializer(reviews , many =True)
      return serializers.data 

class ReviewSerializer(serializers.ModelSerializer):

    class  Meta:
        
        model= Review 
        fields= '__all__'
        
