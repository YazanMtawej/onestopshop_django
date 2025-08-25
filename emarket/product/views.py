from django.shortcuts import  get_object_or_404, render

from rest_framework.decorators import api_view , permission_classes 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser 
from .filtters import ProductsFilter
from rest_framework import status

from.models import Product, Review
from .serializers import ProductSerializer 
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg
# Create your views here.

@api_view(['GET'])
def get_all_products(request):
    filterset= ProductsFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    count= filterset.qs.count()
    respage=14
    paginator= PageNumberPagination() 
    paginator.page_size = respage
    
    qeryset=  paginator.paginate_queryset(filterset.qs,request)

    serializer= ProductSerializer(qeryset,many=True)
 
    return Response({" Products": serializer.data,'per page':respage,'count':count})
       
@api_view(['GET'])

def get_by_id_product(request,pk):
       products= get_object_or_404(Product,id=pk)
       serializer= ProductSerializer( products,many=False)
       print(products)
       return Response({" Product": serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated , IsAdminUser ])

def new_product(request):
       data = request.data
       serializer= ProductSerializer(data = data)
       if serializer.is_valid():
             product = Product.objects.create(**data , user = request.user)
             res = ProductSerializer(product , many = False)

             return Response({" Product": res.data})
       else:
             return Response(serializer.errors)
       
@api_view(['PUT'])
@permission_classes([IsAuthenticated , IsAdminUser ])

def update_product(request,pk):
       product= get_object_or_404(Product,id=pk)
     
       if product.user != request.user:
              return Response({" Error": "Sorry you can not update this product"}
                              ,status= status.HTTP_403_FORBIDDEN)
       
       product.name = request.data ['name']
       product.discription = request.data ['discription']
       product.price= request.data ['price']
       product.brand = request.data ['brand']
       product.category = request.data ['category']
       product.ratings = request.data ['ratings']
       product.stock = request.data ['stock']
       product.perfumer= request.data ['perfumer']
       product.concertration= request.data ['concertration']
       product.top_notes= request.data ['top_notes']
       product.heart_notes= request.data ['heart_notes']
       product.base_notes= request.data ['base_notes']
       product.fragrance_family = request.data ['fragrance_family']
       product.bottle_size= request.data ['bottle_size']
       product.longevity= request.data ['longevity']
       product.sillage= request.data ['sillage']
       product.createdAt= request.data.get('createdAt', product.createdAt)
       product.release_year= request.data ['release_year']

       product.save()
       serializer = ProductSerializer(product , many =False)
       return Response({" Product": serializer.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated , IsAdminUser ])

def delete_product(request,pk):
       product= get_object_or_404(Product,id=pk)
     
       if product.user != request.user:
              return Response({" Error": "Sorry you can not update this product"}
                              ,status= status.HTTP_403_FORBIDDEN)
     
       product.delete()
     
       return Response({" details": "Delete action is done "}
                       ,status= status.HTTP_200_OK)
                   
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def create_review(request,pk):
       user = request.user
       product= get_object_or_404(Product, id=pk)
       data = request.data
       review = product.reviews.filter(user=user) 
      
       if data['rating']<=0 or  data['rating']> 5 :
             
           
             return Response({"Error ": ' Please select between  1 to 5 only '} 
                             , status= status.HTTP_400_BAD_REQUEST)
       

       elif review.exists():
             new_review = {'rating' :data['rating'] , 'comment': data['comment']}
             review.update(**new_review)

             rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
             product.rating = rating['avg_ratings']
             product.save()

             return Response({'details':'product review update'}) 
       else:
             Review.objects.create(
                   user = user,
                   product =product ,
                   rating = data['rating'],
                   comment = data['comment']
             )          

             rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
             product.rating = rating['avg_ratings']
             product.save()
             return Response({'details':'product review created'}) 

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def delete_review(request,pk):
       user= request.user
       product= get_object_or_404(Product,id=pk)

       review = product.reviews.filter(user=user)
     
       if review.exists():
              review.delete()
              rating = product.reviews.aggregate (avg_ratings = Avg('rating'))
              if rating ['avg_ratings'] is None:
                    rating['avg_ratings'] = 0
                    product.ratings = rating['avg_ratings']
                    product.save()
                    return Response({" details": "product review deleted "})
              else:
      
                  return Response({" Error": "Review not found"}
                              ,status= status.HTTP_404_NOT_FOUND)