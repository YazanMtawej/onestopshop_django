from django.urls import path
from . import views
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import MyTokenObtainPairView
from .views import charge_user_points
from .views import my_balance
from .views import get_points_history

urlpatterns =[
    
   path('register/', views.register, name='register'),
   path('userinfo/', views.current_user, name='user_info'),
   path('userinfo/update/', views.update_user, name='update_user'),
   path('forgot_password/', views.forgot_password, name='forgot_password'),
   path('reset_password/<str:token>/', views.reset_password, name='reset_password'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # تجديد التوكن
   path('logout/', views.LogoutView.as_view(), name='logout'),                   # تسجيل الخروج
   path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('charge-user/', charge_user_points, name='charge-points'),
   path('get-profile/', views.get_user_profile),
   path('my-balance/', my_balance),
   path('pay-points/', views.pay_with_points),
   path('points-history/', get_points_history, name='points-history'),
]
