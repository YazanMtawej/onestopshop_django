from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SingUpSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser
from .serializers import CustomTokenObtainPairSerializer
from .models import Profile, UserPoints
from decimal import Decimal

@api_view(['POST'])
def register(request):
    data = request.data
    serializer = SingUpSerializer(data=data)

    if serializer.is_valid():
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create(
                username=data['username'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                password=make_password(data['password']),
            )
            return Response({'detail': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Username already exists!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    try:
        required_fields = ['first_name', 'last_name', 'username']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return Response({f'{field}': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.username = data['username']

        if 'password' in data and data['password'].strip():
            user.password = make_password(data['password'])

        user.save()

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_current_host(request):
    protocol = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    return f"{protocol}://{host}/"

@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User, username=data['username'])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()
    return Response({'details': 'Reset token generated successfully', 'token': token})

@api_view(['POST'])
def reset_password(request, token):
    data = request.data
    
    user = get_object_or_404(User, username=data['username'], profile__reset_password_token=token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)

    if data['password'] != data['confirmPassword']:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()
    return Response({'details': 'Password reset successful'})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out successfully."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([IsAdminUser])
def charge_user_points(request):
    username = request.data.get('username')
    amount = request.data.get('amount')

    if not username or not amount:
        return Response({'error': 'Username and amount are required.'}, status=400)

    try:
        user = User.objects.get(username=username)
        profile = user.profile
        amount = Decimal(amount)

        profile.points += amount
        profile.save()

        UserPoints.objects.create(
            user=user,
            points=amount,
            action_type='charge',
            description=f"{amount} points charged by admin"
        )

        return Response({'message': f'{amount} points have been charged to user {username}'})

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except Exception as e:
        print("🔥 ERROR:", e)
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    profile = request.user.profile
    return Response({
        "username": request.user.username,
        "points": float(profile.points),
        "balance": float(profile.balance),
        "is_admin": profile.is_admin,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_balance(request):
    profile = request.user.profile
    return Response({'points': float(profile.points)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_with_points(request):
    try:
        user = request.user
        amount = request.data.get("amount")

        if amount is None:
            return Response({"error": "Amount is required."}, status=status.HTTP_400_BAD_REQUEST)

        amount = Decimal(amount)
        profile = Profile.objects.get(user=user)

        if profile.points < amount:
            return Response({"error": "Insufficient points."}, status=status.HTTP_400_BAD_REQUEST)

        profile.points -= amount
        profile.save()

        UserPoints.objects.create(
            user=user,
            points=-amount,
            action_type='purchase',
            description='Purchase with points'
        )

        return Response({"message": "Payment completed."}, status=status.HTTP_200_OK)

    except Exception as e:
        print("❌ Server Exception:", str(e))
        return Response({"error": f"Server error: {str(e)}"}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_points_history(request):
    user = request.user
    history = UserPoints.objects.filter(user=user).order_by('-timestamp')

    data = [
        {
            'points': str(entry.points),
            'action_type': entry.action_type,
            'description': entry.description,
            'date': entry.timestamp.strftime('%Y-%m-%d %H:%M'),
        }
        for entry in history
    ]

    return Response({'history': data})
