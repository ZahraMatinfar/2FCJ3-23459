from django.contrib.auth import get_user_model, authenticate
from apps.account.serializers import RegisterSerializer, LoginSerializer
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiExample
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from drf_spectacular.types import OpenApiTypes


# Create your views here.

User = get_user_model()


class AuthViewSet(viewsets.ViewSet):
    
    # @extend_schema(
    #     summary="Register a new user",
    #     request=RegisterSerializer,
    #     responses={
    #         201: OpenApiResponse(description="User registered successfully with token"),
    #         400: OpenApiResponse(description="Invalid data"),
    #     }
    # )
    @extend_schema(
        summary="Register a new user",
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="User registered successfully",
                examples=[
                OpenApiExample(
                    "Successful registration",
                    value={
                        "user": {
                            "email": "testuser@example.com"
                        },
                    }
                )
            ],
            ),
            400: OpenApiResponse(description="Invalid data")
        }
    )
    @action(detail=False, methods=['post'], url_path='register', url_name='register')
    def register(self, request):
        
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        user = serializer.save()
        Token.objects.get_or_create(user=user)
        return Response(
            {"user": serializer.data}, 
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Login a user with email and password",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Successful login"),
            400: OpenApiResponse(description="Invalid credentials")
        }
    )
    @action(detail=False, methods=['post'], url_path='login', url_name="login")
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate user using email as the 'username'
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Generate or get authentication token
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            # Return error if authentication fails
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
