from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import *
from ..serializers import *

# GET Admin profile
class AdminProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        return self.request.user
