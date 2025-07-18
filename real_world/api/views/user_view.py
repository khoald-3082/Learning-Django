from rest_framework.views import APIView
from rest_framework.response import Response

class UserView(APIView):
    """Controller handle for API of User"""

    def get(self, request):
        """GET user profile"""
        return Response({"message": "User profile details"})

    def post(self, request):
        """POST create user profile"""
        return Response({"message": "User profile created"})
