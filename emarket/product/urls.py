from django.urls import path
from . import views





urlpatterns = [
    path('',views.get_all_products,name='products'),
    path('<str:pk>/',views.get_by_id_product,name='get_by_id_product'),
    path('new',views.new_product,name='new_products'),
    path('update/<str:pk>/',views.update_product,name='update_product'),
    path('delete/<str:pk>/',views.delete_product,name='delete_product'),
    path('<str:pk>/reviews', views.create_review, name='create_review'),
    path('<str:pk>/reviews/delete', views.delete_review, name='delete_review'),
]


