from config.settings import JWT_SECRET_KEY
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer , UserProfileSerializer
from .models import User, UserProfile
import jwt , datetime


# Create your views here.
class Hello(APIView):
    # permission_classes = (IsAuthenticated)
    def get(self, request):
        
        return Response({'message': 'just getting started'})

class RegisterView(APIView):
    #  view used to register users account
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        registered_user = serializer.data
        registered_email =registered_user['email']
        return Response(registered_email)

class CreateProfileView(APIView):
    #  view used to register users account
    def post(self,request):
        serializer = UserProfileSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    #  view used to login users account
    def post(self,request):
        email    = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('user not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')

        payload = {
              'id' : user.id,
              'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
              'iat': datetime.datetime.utcnow()
                     }
        #   generating a token for Authentication
        token = jwt.encode(payload,JWT_SECRET_KEY ,algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt',value=token,httponly=True)

        response.data ={
            'jwt' : token
        }

        return response
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('not authenticated')
        
        try:
           payload = jwt.decode(token,JWT_SECRET_KEY,algorithms="HS256")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('no payload')
        user_id = payload['id']
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)

        return Response({
            # 'token' : token,
             "user" : serializer.data
        })

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie(key='jwt')

        response.data = {
            "message" :"loged out successfull"
        } 

        return response


class UserProfiles(APIView):
    def get(self, request):
        # userprofiles = UserProfiles.objects.all()
        # serializer = UserProfileSerializer(userprofiles)
        return Response('hello')
