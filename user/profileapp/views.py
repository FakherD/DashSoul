from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ProfileSerializer
from .models import Profile
import jwt
from datetime import datetime, timedelta
from .middleware import UserNotFoundException, IncorrectPasswordException

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        emailaddress = request.data['emailaddress']
        password = request.data['password']

        profile = Profile.objects.filter(emailaddress=emailaddress).first()

        if not profile:
            raise UserNotFoundException()

        if not profile.check_password(password):
            raise IncorrectPasswordException()

        payload = {
            'id': profile.id,
            'exp': datetime.utcnow() + timedelta(minutes=60), 
            'iat': datetime.utcnow()  
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        if isinstance(token, bytes):
            token = token.decode('utf-8')  # Adjusted for compatibility

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}

        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        profile = Profile.objects.filter(id=payload['id']).first()
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'success'}
        return response
