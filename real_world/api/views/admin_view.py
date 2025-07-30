from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers.user_serializer import UserSerializer

"""Controller handle for API of Admin"""

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_admin_profile(request):
    """GET Admin profile"""
    user = request.user
    return Response({
        "profile": UserSerializer(user).data,
    })
